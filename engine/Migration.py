import os
import subprocess
from engine.Database import db
from datetime import datetime
import glob

from utils import GeneralHelper
from zipfile import ZipFile

class Migration(db):

    directus__blacklist_tables = [
        'directus_activity', 'directus_activity_seen',
        'directus_files', 'directus_folders', 'directus_migrations',
        ''
    ]

    def __init__(self, username, password, database, name):
        super().__init__(username, password)
        self.database = database
        self.name = name

    def migrate(self, migration_file):
        os.system('mysql -u {username} --password="{password}" {database}'
                  '< data/migrations/{filename} &> data/tmp/null'.format(
                    username=self.username,
                    password=self.password,
                    database=self.database,
                    filename=migration_file
        ))

    def remove_blacklist(self, tables):
        clean_tables = []
        for table in tables:
            if table not in self.directus__blacklist_tables:
                clean_tables.append(table)
        return clean_tables

    def create_db_migration(self):
        raw_tables = self.get_db_tables()
        tables = list(map(lambda d: d[0], raw_tables))
        clean_tables = self.remove_blacklist(tables)
        file_name ="{pj_ref}-{db}-{timestamp}".format(
                        pj_ref=self.name,
                        db=self.database,
                        timestamp=GeneralHelper.prepare_string(str(datetime.now()))
                    )
        os.system('mysqldump -u {username} --password="{password}" {database} {tables} '
                  '> data/migrations/{filename}.sql &> data/tmp/null'.format(
                    username=self.username,
                    password=self.password,
                    database=self.database,
                    tables= " ".join(clean_tables),
                    filename=file_name
        ))

    @staticmethod
    def get_migrations():
        return [file_name.split('/')[2] for file_name in glob.glob("data/migrations/*.sql")]

    @staticmethod
    def download_migrations(out_dir):
        zip_obj = ZipFile('{path}/wg-migrations.zip'.format(path=out_dir), 'w')
        for migration in Migration.get_migrations():
            zip_obj.write('{path}/{file}'.format(path='data/migrations/', file=migration))
        zip_obj.close()
        return True



