
from prettytable import PrettyTable
import os.path
from utils import ModuleFileSystem, GeneralHelper
from engine.DirectusController import DirectusController

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
        self.init_directus_env(environment)
        self.write()

    def init_directus_env(self, environment):
        if not ModuleFileSystem.check_file(environment.path+'config/api.php'):
            DirectusController.init_directus(environment.path)


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
        self.items = []
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

    def clear_env(self, ref_name):
        index = GeneralHelper.get_index_on_dict_value(
            collection=self.items,
            key='ref',
            value=ref_name
        )
        self.items.pop(index)
        self.write()
        os.system('rm data/envs/{ref}.txt'.format(ref=ref_name))

    def reset(self):
        os.system('rm -r data')