import os


class ModuleFileSystem:
    @staticmethod
    def check_dirs(dir_paths):
        for path in dir_paths:
            if not os.path.exists(path):
                os.makedirs(path)

    @staticmethod
    def check_files(file_paths):
        for path in file_paths:
            if not os.path.exists(path):
                open(path, 'w').close()


class GeneralHelper:

    @staticmethod
    def get_index_on_dict_value(collection, key, value):
        for i in range(len(collection)):
            if collection[i][key] == value:
                return i
        return False


