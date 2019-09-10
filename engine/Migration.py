import os
import subprocess
from engine.Database import db
from datetime import datetime

from utils import GeneralHelper


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
        fnull = open(os.devnull, 'w')
        os.system('mysqldump -u {username} --password="{password}" {database} {tables} '
                  '> data/migrations/{filename}.sql &> ./tmp/null'.format(
                    username=self.username,
                    password=self.password,
                    database=self.database,
                    tables= " ".join(clean_tables),
                    filename=file_name
        ))

