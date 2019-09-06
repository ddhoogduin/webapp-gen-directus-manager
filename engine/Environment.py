
from prettytable import PrettyTable


class Environment:
    env_list = []

    def __init__(self, ref_name, name, path):
        Environment.load_list()
        self.ref_name = ref_name
        self.name = name
        self.path = path

    def create(self):
        item = {
            'ref': self.ref_name,
            'name': self.name,
            'path': self.path
        }
        Environment.env_list.append(item)
        Environment.write_envs()

    def load(self, id):
        pass

    def delete(self, id):
        pass

    @staticmethod
    def write_envs():
        with open('data/envs.txt', 'w') as fp:
            for item in Environment.env_list:
                fp.writelines("\t".join(item.values()))

    @staticmethod
    def get_envs():
        x = PrettyTable()
        x.field_names = ["#", "Reference Name", "Name", "Path"]
        for i in range(len(Environment.env_list)):
            item = Environment.env_list[i]
            x.add_row([i+1, item['ref'], item['name'], item['path']])
        return x

    @staticmethod
    def load_list():
        Environment.env_list = []
        for line in open("data/envs.txt").readlines():
            if line:
                try:
                    item = {}
                    data = line.split('\t')
                    item['ref'] = data[0]
                    item['name'] = data[1]
                    item['path'] = data[2]
                    Environment.env_list.append(item)
                except KeyError:
                    pass

