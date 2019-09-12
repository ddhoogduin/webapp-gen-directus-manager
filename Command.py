from __future__ import print_function, unicode_literals
from PyInquirer import prompt
import subprocess
import sys, os
import re
from Questions import EnvQuestions, PjQuestions
from engine.Validations import EnvValidations
from engine.Validations import ValidationHelper
from engine.Environments import Environments
from engine.Environment import Environment
from engine.Project import Project
from engine.Migration import Migration
from utils import GeneralHelper
module_options = ['<== BACK']


class CommandEnv:

    def __init__(self):
        self.envs = None
        self.env = None
        self.main()

    def main(self):
        self.envs = Environments()
        self.envs.load()
        if len(self.envs.items) > 0:
            options = ['load', 'create', 'delete', 'reset']
            if Migration.get_migrations():
                options = options + ['download migrations']
            options = options + ['cancel']
            EnvQuestions.introduction[0]['choices'] = options

        task_data = prompt(EnvQuestions.introduction)
        try:
            self.interface(task_data)
        except KeyboardInterrupt:
            print('\n')
            close_data = prompt(EnvQuestions.close)
            try:
                ValidationHelper.check_answers(close_data)
                action = close_data['close_action']
                print(action)
                if action == 'back to main options':
                    return self.main()
                else:
                    sys.exit(1)
            except KeyboardInterrupt:
                sys.exit(1)

    def interface(self, task_data):
        if not task_data:
            raise KeyboardInterrupt
        task = task_data['task']
        if task == 'load':
            self.load()
            CommandPj(Environment(self.env))
        elif task == 'create':
            self.create()
            CommandPj(Environment(self.env))
        elif task == 'delete':
            self.delete()
        elif task == 'reset':
            self.reset()
        elif task == 'download migrations':
            self.download_migrations()
        else:
            sys.exit(1)

    def load(self):
        print(self.envs.get())
        if len(self.envs.items) > 0:
            options = map(lambda d: d['ref'], self.envs.items)
            EnvQuestions.load[0]['choices'] = list(options) + [module_options[0]]
            load_data = prompt(EnvQuestions.load)
            ValidationHelper.check_answers(load_data)
            if load_data['env_ref'] == module_options[0]:
                return self.main()
            self.env = load_data['env_ref']

    def create(self):
        path = self.check_directus_dir()
        install_data = prompt(EnvQuestions.create)
        ValidationHelper.check_answers(install_data)
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

    def delete(self):
        q = EnvQuestions.delete
        q[0]['choices'] = [item['ref'] for item in self.envs.items] + [module_options[0]]
        ref_name = prompt(q[0])['ref_name']
        if ref_name == module_options[0]:
            return self.main()
        delete_data = prompt([q[1], q[2]])
        if delete_data['confirmation']:
            env = Environment(ref_name=ref_name)
            env.delete(keep_db=delete_data['keep_db'])
            self.envs.clear_env(ref_name=ref_name)
        return self.main()

    def reset(self):
        reset_data = prompt(EnvQuestions.reset)
        if reset_data['confirmation']:
            for item in self.envs.items:
                env = Environment(ref_name=item['ref'])
                env.delete(keep_db=reset_data['keep_db'])
                self.envs.clear_env(ref_name=item['ref'])
            self.envs.reset()
            self.__init__()

    def download_migrations(self):
        path = GeneralHelper.prepare_path(self.check_output_dir())
        Migration.download_migrations(out_dir=path)

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
            os.system("bash shell/directoryFinder.sh")
            path = GeneralHelper.prepare_path(open("data/tmp/directusEnv.txt").read())
            os.remove("data/tmp/directusEnv.txt")
            if EnvValidations.validate_unique_path(path):
                break
            else:
                print("\nX Path not unique, try again...")
        return path

    @staticmethod
    def check_output_dir():
        while True:
            subprocess.run("bash shell/outputFinder.sh", shell=True)
            path = open("data/tmp/outPath.txt").read()
            os.remove("data/tmp/outPath.txt")
            if EnvValidations.validate_unique_path(path):
                break
            else:
                print("\nX Path not unique, try again...")
        return path

class CommandPj:

    def __init__(self, env):
        self.env = env
        self.pj = None
        self.main()

    def main(self):
        print(self.env.ouput())
        self.env.load_projects()
        choices = ['create project', 'link project to database']
        if len(self.env.projects) > 0:
            choices = ['create project', 'project settings','link project to database']
        PjQuestions.introduction[0]['choices'] = choices + [module_options[0]]
        intro_data = prompt(PjQuestions.introduction)
        try:
            ValidationHelper.check_answers(intro_data)
            self.interface(intro_data)
        except KeyboardInterrupt:
            print('\n')
            close_data = prompt(PjQuestions.close)
            try:
                ValidationHelper.check_answers(close_data)
                action = close_data['close_action']
                print(action)
                if action == 'back to environment options':
                    return self.main()
                else:
                    sys.exit(1)
            except KeyboardInterrupt:
                sys.exit(1)

    def interface(self, intro_data):
        if intro_data['task'] == module_options[0]:
            return CommandEnv()
        elif intro_data['task'] == 'create project':
            self.create()
        elif intro_data['task'] == 'project settings':
            self.project_settings()
        elif intro_data['task'] == 'link project to database':
            self.link_project()

    def create(self):
        migration_file=None
        if len(Migration.get_migrations()) > 0:
            migration_data = prompt(PjQuestions.migrations[0])
            ValidationHelper.check_answers(migration_data)
            if migration_data['use_migration']:
                PjQuestions.migrations[1]['choices'] = Migration.get_migrations()
                migration_file = prompt(PjQuestions.migrations[1])['migration_file']
        install_data = prompt(PjQuestions.create)
        ValidationHelper.check_answers(install_data)
        self.pj = Project(
            ref=install_data['install_ref'],
            name=install_data['install_name']
        )
        self.env.add_project(
            project=self.pj,
            migration_file=migration_file
        )
        self.main()

    def project_settings(self):
        PjQuestions.select_project[0]['choices'] = map(lambda d: d['ref'], self.env.projects)
        ref_data = prompt(PjQuestions.select_project)
        ValidationHelper.check_answers(ref_data)

        self.pj = Project(ref=ref_data['pj_ref'])
        pj_task = prompt(PjQuestions.project_task)['pj_task']
        ValidationHelper.check_answers(pj_task)
        if pj_task == 'delete project':
            self.delete()
        elif pj_task == 'templatify project database':
            self.templatify()

    def link_project(self):
        databases = self.env.list_dbs()
        PjQuestions.link[0]['choices'] = databases
        link_data = prompt(PjQuestions.link)
        ValidationHelper.check_answers(link_data)
        self.env.link_project(
            project=Project(
                    ref=link_data['install_ref'],
                    name=link_data['install_name'],
                    database=link_data['database_name'])
                )
        self.main()

    def delete(self):
        delete_tasks = prompt(PjQuestions.delete)
        ValidationHelper.check_answers(delete_tasks)
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
        print(pj_data)
        ValidationHelper.check_answers(pj_data)
        self.pj = Project(
            ref=pj_data['ref'],
            name=pj_data['name'],
            database=pj_data['database']
        )
        self.env.templatify_project(self.pj)
        self.main()



if __name__ == '__main__':
    CommandEnv()
    # CommandPj(Environment('testenv'))
