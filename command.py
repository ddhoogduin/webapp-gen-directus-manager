from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
import subprocess
import sys, os
import readline, glob
import re
from engine.Validations import EnvValidations
from engine.Environment import Environment


class Questions:

    introduction = [
        {
            'type': 'list',
            'name': 'task',
            'message': 'Select a environment option to continue:',
            'choices': ['load', 'create', 'reset', 'delete']
        }
    ]
    load = [
        {
            'type': 'list',
            'name': 'env_ref',
            'message': 'Select a Directus environment:',
            'choices': []
        }
    ]
    create = [
        {
            'type': 'input',
            'name': 'install_name',
            'message': 'Enter a unique name for the Directus environment:',
            'validate': EnvValidations.validate_unique_name
        }
    ]


class CommandEnv:

    def __init__(self):
        self.env = None
        Environment.load_list()
        intro_data = prompt(Questions.introduction)
        if intro_data['task'] == 'load':
            self.load()
        elif intro_data['task'] == 'create':
            self.create()

    def load(self):
        print(Environment.get_envs())
        options = map(lambda d: d['ref'], Environment.env_list)
        Questions.load[0]['choices'] = options
        load_data = prompt(Questions.load)
        self.env = load_data['env_ref']

    def create(self):
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
        install_data = prompt(Questions.create)
        ref_name = re.sub('[\W_]+', '', install_data['install_name'])
        env = Environment(
            ref_name=ref_name,
            name=install_data['install_name'],
            path=path
        )
        env.create()
        self.env = ref_name



class CommandPj:

    def __init__(self, env_ref_name):
        self.env_ref_name = env_ref_name

    def load_projects(self):



if __name__ == '__main__':
    CommandEnv()
