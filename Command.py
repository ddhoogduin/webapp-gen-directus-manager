from __future__ import print_function, unicode_literals
from PyInquirer import prompt
import subprocess
import sys, os
import re
from Questions import EnvQuestions, PjQuestions
from engine.Validations import EnvValidations
from engine.Environments import Environments
from engine.Environment import Environment
from engine.Project import Project


class CommandEnv:

    def __init__(self):
        self.envs = Environments()
        self.env = None

        if len(self.envs.items) > 0:
            options = ['load', 'create', 'reset', 'delete']
        else:
            options = ['create']
        EnvQuestions.introduction[0]['choices'] = options

        intro_data = prompt(EnvQuestions.introduction)
        if intro_data['task'] == 'load':
            self.load()
            CommandPj(Environment(self.env))
        elif intro_data['task'] == 'create':
            self.create()
            CommandPj(Environment(self.env))

    def load(self):
        print(self.envs.get())
        if len(self.envs.items) > 0:
            options = map(lambda d: d['ref'], self.envs.items)
            EnvQuestions.load[0]['choices'] = options
            load_data = prompt(EnvQuestions.load)
            self.env = load_data['env_ref']

    def create(self):
        path = self.check_directus_dir()
        install_data = prompt(EnvQuestions.create)
        db_user, db_pw = self.get_db_details()
        ref_name = re.sub('[\W_]+', '', install_data['install_name'])
        env = Environment(
            ref_name=ref_name,
            name=install_data['install_name'],
            path=path,
            db_user=db_user,
            db_pw=db_pw
        )
        self.envs.add(env)
        self.env = ref_name

    @staticmethod
    def get_db_details():
        while True:
            db_data = prompt(EnvQuestions.env_db)
            if EnvValidations.validate_db_connection(
                username=db_data['username'],
                password=db_data['password']
            ):
                break
        return db_data['username'], db_data['password']

    @staticmethod
    def check_directus_dir():
        while True:
            try:
                subprocess.run("bash shell/directoryFinder.sh", shell=True)
                path = open("data/tmp/directusEnv.txt").read()
                os.remove("data/tmp/directusEnv.txt")
                if EnvValidations.validate_unique_path(path):
                    break
                else:
                    print("\nX Path not unique, try again...")
            except KeyboardInterrupt:
                print("interrupt")
                sys.exit(0)
        return path


class CommandPj:

    def __init__(self, env):
        self.env = env
        self.pj = None
        self.main()

    def main(self):
        print(self.env.ouput())
        if not len(self.env.projects) > 0:
            PjQuestions.introduction[0]['choices'] = ['create project']
        intro_data = prompt(PjQuestions.introduction)
        if intro_data['task'] == 'create project':
            self.create()
        elif intro_data['task'] == 'project settings':
            self.project_settings()
        elif intro_data['task'] == 'link project to database':
            self.link_project()

    def create(self):
        install_data = prompt(PjQuestions.create)
        self.pj = Project(
            ref=install_data['install_ref'],
            name=install_data['install_name']
        )
        self.env.add_project(self.pj)
        self.main()

    def project_settings(self):
        PjQuestions.select_project[0]['choices'] = map(lambda d: d['ref'], self.env.projects)

        self.pj = Project(ref=prompt(PjQuestions.select_project)['pj_ref'])
        pj_task = prompt(PjQuestions.project_task)['pj_task']

        if pj_task == 'Delete project':
            self.delete()
        elif pj_task == 'Templatify project database':
            self.templatify()

    def link_project(self):
        databases = self.env.list_dbs()
        PjQuestions.link[0]['choices'] = databases
        link_data = prompt(PjQuestions.link)
        self.env.link_project(
            project=Project(
                    ref=link_data['install_ref'],
                    name=link_data['install_name']),
            db_name=link_data['database_name']
        )
        self.main()

    def delete(self):
        delete_tasks = prompt(PjQuestions.delete)
        keep_db = delete_tasks['keep_db']
        confirmation = delete_tasks['confirmation']
        if confirmation:
            self.env.delete_project(
                project=self.pj,
                keep_db=keep_db
            )
        self.main()

    def templatify(self):
        pj_data = self.env.get_project(self.pj.ref_name)
        self.pj = Project(
            ref=pj_data['ref'],
            name=pj_data['name'],
            database=pj_data['database']
        )
        self.env.templatify_project(self.pj)




if __name__ == '__main__':
    CommandPj(Environment('testenv'))
