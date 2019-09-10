
from prettytable import PrettyTable
import os.path
from utils import ModuleFileSystem, GeneralHelper


class Environments:

    def __init__(self):
        self.items = []
        ModuleFileSystem.check_dirs(['data/envs', 'data/migrations','data/tmp/dev'])
        ModuleFileSystem.check_files(['data/envs.txt','data/tmp/dev/null'])
        self.load()

    def add(self, environment):
        item = {
            'ref': GeneralHelper.prepare_string(environment.ref_name),
            'name': GeneralHelper.prepare_string(environment.name),
            'path': environment.path,
            'db_user': GeneralHelper.prepare_string(environment.db_user),
            'db_password': GeneralHelper.prepare_string(environment.db_pw)
        }
        self.items.append(item)
        environment.init_env_project_file()
        self.write()

    def write(self):
        with open('data/envs.txt', 'w') as fp:
            for item in self.items:
                line = "\t".join(item.values())
                line = line.replace('\n', ' ').replace('\r', '')
                fp.write(line+'\n')

    def get(self):
        x = PrettyTable()
        x.field_names = ["#", "Reference Name", "Name", "Path"]
        for i in range(len(self.items)):
            item = self.items[i]
            x.add_row([i+1, item['ref'], item['name'], item['path']])
        return x

    def load(self):
        for line in open("data/envs.txt").readlines():
            if line:
                try:
                    item = {}
                    data = line.split('\t')
                    item['ref'] = data[0]
                    item['name'] = data[1]
                    item['path'] = data[2]
                    item['db_user'] = data[3]
                    item['db_pw'] = data[4].replace('\n', '')
                    self.items.append(item)
                except KeyError:
                    pass

