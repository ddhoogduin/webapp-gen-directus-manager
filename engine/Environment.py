import os
from prettytable import PrettyTable

from utils import GeneralHelper, ModuleFileSystem
from engine.Environments import Environments
from engine.Database import db
from engine.Migration import Migration
from engine.DirectusController import DirectusController
from engine.Project import Project


class Environment:
    active = None

    def __init__(self, ref_name, name=None, path=None, db_user=None, db_pw=None):
        self.ref_name = ref_name
        self.name = name
        self.path = path
        self.db_user = db_user
        self.db_pw = db_pw

        Environment.active = self.ref_name
        self.projects = []
        self.envs = Environments()

        if not name and not path:
            self.load()

    def load(self):
        self.envs.load()
        index = GeneralHelper.get_index_on_dict_value(
            collection=self.envs.items,
            key='ref',
            value=self.ref_name
        )
        if index >= 0:
            self.name = self.envs.items[index]['name']
            self.path = self.envs.items[index]['path']
            self.db_user = self.envs.items[index]['db_user']
            self.db_pw = self.envs.items[index]['db_pw']
            self.load_projects()
        else:
            raise SystemError('Unknown environment reference:', self.ref_name)

    def ouput(self):
        x = PrettyTable()
        x.field_names = ["#", "Reference Name", "Database", "Name"]
        for i in range(len(self.projects)):
            item = self.projects[i]
            x.add_row([i+1, item['ref'], item['database'], item['name']])
        return x

    def load_projects(self):
        self.projects = []
        for line in open("data/envs/{ref_name}.txt".format(ref_name=self.ref_name)).readlines():
            if line:
                try:
                    item = {}
                    data = line.split('\t')
                    item['ref'] = data[0]
                    item['database'] = GeneralHelper.prepare_string(data[1])
                    item['name'] = GeneralHelper.prepare_string(data[2])
                    self.projects.append(item)
                except KeyError:
                    pass

    def write(self):
        with open("data/envs/{ref_name}.txt".format(ref_name=self.ref_name), 'w') as fp:
            for item in self.projects:
                line = "\t".join(item.values())
                line = line.replace('\n', ' ').replace('\r', '')
                fp.write(line+"\n")

        template_file = open('assets/formats/config-format.txt')
        template = template_file.read()
        template_file.close()

        config_content = ""
        with open("{path}public/admin/config.js".format(path=self.path.replace(' ', '')), 'w') as fp:
            for i in range(len(self.projects)):
                if i+1 == len(self.projects):
                    tmpl = '\n"{path}":"{name}"'
                else:
                    tmpl = '\n"{path}":"{name}",'
                config_content += tmpl.format(
                    path="../"+self.projects[i]['ref'],
                    name=self.projects[i]['name']
                )
            fp.write(template.format(content=config_content))

    def get_project(self, ref_name):
        index = GeneralHelper.get_index_on_dict_value(
            collection=self.projects,
            key='ref',
            value=ref_name
        )
        return self.projects[index]

    def init_env_project_file(self):
        ModuleFileSystem.check_files(['data/envs/{ref_name}.txt'.format(
            ref_name=self.ref_name
        )])

    def delete_project(self, project, keep_db):
        index = GeneralHelper.get_index_on_dict_value(
            collection=self.projects,
            key='ref',
            value=project.ref_name
        )
        self.projects.pop(index)
        DirectusController.delete_config(
            path=self.path,
            pj_name=project.ref_name
        )
        if not keep_db:
            env_db = db(self.db_user, self.db_pw)
            env_db.drop_db(project.ref_name)

        self.write()

    def add_project(self, project, migration_file):
        env_db = db(self.db_user, self.db_pw)
        env_db.add_db(project.ref_name)
        DirectusController.install_config(
            path=self.path,
            db_name=project.ref_name,
            db_user=self.db_user,
            db_pw=self.db_pw,
            pj_name=project.ref_name
        )
        DirectusController.install_database(
            path=self.path,
            pj_name=project.ref_name
        )
        if migration_file:
            Migration(
                username=self.db_user,
                password=self.db_pw,
                database=project.ref_name,
                name=project.ref_name
            ).migrate(migration_file)

        DirectusController.init_user(
            path=self.path,
            pj_name=project.name
        )
        self.write_new_projects(project=project)

    def write_new_projects(self, project):
        database = project.database if project.database else project.ref_name
        print(database)
        self.projects.append(dict(
            ref=GeneralHelper.prepare_string(project.ref_name),
            database=GeneralHelper.prepare_string(database),
            name=GeneralHelper.prepare_string(project.name)
        ))
        self.write()

    def templatify_project(self, project):
        migration = Migration(
            username=self.db_user,
            password=self.db_pw,
            name=project.ref_name,
            database=project.database
        )
        migration.create_db_migration()

    def list_dbs(self):
        db_env = db(username=self.db_user, password=self.db_pw)
        return list(map(lambda d: d[0], db_env.get_db_databases()))

    def link_project(self, project, db_name):
        DirectusController.install_config(
            path=self.path,
            db_name=db_name,
            db_user=self.db_user,
            db_pw=self.db_pw,
            pj_name=project.ref_name
        )
        self.write_new_projects(project=project)

    def delete(self, keep_db):
        for project in self.projects:
            project = Project(
                ref=project['ref'],
                name=project['name']
            )
            self.delete_project(
                project=project,
                keep_db=keep_db
            )
