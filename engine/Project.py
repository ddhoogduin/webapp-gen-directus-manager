from engine.Database import db
from prettytable import PrettyTable
from utils import GeneralHelper


class Project:

    def __init__(self, ref, name=None, database=None):
        self.ref_name = GeneralHelper.prepare_string(ref)
        if name:
            self.name = GeneralHelper.prepare_name(name)
        self.name = name
        self.database = database
