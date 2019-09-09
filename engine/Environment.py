import os

from utils import GeneralHelper
from engine.Environments import Environments
from engine.Database import db


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

    def load_projects(self):
        for line in open("data/envs/{ref_name}.txt".format(ref_name=self.ref_name)).readlines():
            if line:
                try:
                    item = {}
                    data = line.split('\t')
                    item['ref'] = data[0]
                    item['name'] = data[1]
                    self.projects.append(item)
                except KeyError:
                    pass

    def write(self):
        with open("data/envs/{ref_name}.txt".format(ref_name=self.ref_name), 'w') as fp:
            for item in self.projects:
                line = "\t".join(item.values())
                line = line.replace('\n', ' ').replace('\r', '')
                fp.write(line+"\n")

        template_file = open('assets/config-format.txt')
        template = template_file.read()
        template_file.close()

        config_content = ""
        with open("{path}public/admin/config.js".format(path=self.path.replace(' ', '')), 'w') as fp:
            for i in range(len(self.projects)):
                if i+1 == len(self.projects):
                    tmpl = '"{path}":"{name}"\n'
                else:
                    tmpl = '"{path}":"{name}",\n'
                config_content += tmpl.format(
                    path="../"+self.projects[i]['ref'],
                    name=self.projects[i]['name']
                )
            fp.writelines(template.format(content=config_content))


    def add_project(self, project):
        env_db = db(self.db_user, self.db_pw)
        env_db.connect()
        env_db.connection.execute('CREATE DATABASE {name}'.format(name=project.ref_name))
        os.system("cd {path} && php bin/directus install:config"
                  " -h localhost"
                  " -n {db_name}"
                  " -u {db_user}"
                  " -p {db_password}"
                  " -N {pj_name}".format(
                    path=self.path.replace(' ', ''),
                    db_name=project.ref_name,
                    db_user=self.db_user,
                    db_password=self.db_pw,
                    pj_name=project.ref_name))

        os.system("cd {path} && php bin/directus install:database -N {pj_name}".format(
                    path=self.path.replace(' ', ''),
                    pj_name=project.ref_name))

        os.system("cd {path} && php bin/directus install:install"
                  " -e {name}@example.com "
                  " -p password"
                  " -N {name}".format(
                    path=self.path.replace(' ', ''),
                    name=project.ref_name))

        self.projects.append(dict(ref=project.ref_name, name=project.name))
        self.write()
