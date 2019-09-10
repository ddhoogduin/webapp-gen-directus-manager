from engine.Database import db
from prettytable import PrettyTable


class Project:

    def __init__(self, ref, name=None, database=None):
        self.ref_name = ref
        self.name = name
        self.database = database
