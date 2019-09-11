import os
import re

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

    @staticmethod
    def prepare_string(str_value):
        return re.sub(r"\W", "", str_value)

    @staticmethod
    def prepare_path(str_value):
        str_value = str_value.replace('\n', ' ').replace('\r', '')
        str_value = str_value.replace(' ', '')
        if str_value.endswith('/'):
            str_value = str_value[:-1]
        return str_value
