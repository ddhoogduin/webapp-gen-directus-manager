
from prettytable import PrettyTable
import os.path
from utils import ModuleFileSystem


class Environments:

    def __init__(self):
        self.items = []
        ModuleFileSystem.check_dirs(['data/envs'])
        ModuleFileSystem.check_files(['data/envs.txt'])
        self.load()

    def add(self, Envirionment):
        item = {
            'ref': Envirionment.ref_name,
            'name': Envirionment.name,
            'path': Envirionment.path,
            'db_user':Envirionment.db_user,
            'db_password':Envirionment.db_pw
        }
        self.items.append(item)
        Envirionment.init_env_project_file()
        self.write()

    def write(self):
        with open('data/envs.txt', 'w') as fp:
            for item in self.items:
                line = "\t".join(item.values())
                line = line.replace('\n', ' ').replace('\r', '')
                fp.writelines(line)

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
                    item['db_pw'] = data[4]
                    self.items.append(item)
                except KeyError:
                    pass

