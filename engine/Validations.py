import re
from engine.Database import db
from engine.Environments import Environments
from engine.Environment import Environment


class ValidationHelper:
    @staticmethod
    def check_unique_from_dict(data, key, value):
        for pj in data:
            if pj[key] == value:
                return False
        return True


class EnvValidations:

    @staticmethod
    def validate_unique_path(value):
        envs = Environments()
        return ValidationHelper.check_unique_from_dict(
            data=envs.items,
            key='path',
            value=value
        )

    @staticmethod
    def validate_unique_name(value):
        ref_name = re.sub('[\W_]+', '', value)
        envs = Environments()
        valid = ValidationHelper.check_unique_from_dict(
            data=envs.items,
            key='name',
            value=ref_name
        )
        to_small = True if len(ref_name) < 3 else False
        return "not unique or to small (min. 3 char)" if not valid or to_small else True

    @staticmethod
    def validate_db_connection(username, password):
        return db(username=username, password=password).connect()


class PjValidations:

    @staticmethod
    def validate_db_name_unique(username, password, name):
        env_db = db(
            username=username,
            password=password
        )
        env_db.connect()
        return env_db.check_name_unique(name)

    @staticmethod
    def validate_unique_ref(value):
        ref_name = re.sub('[\W_]+', '', value)
        env = Environment(Environment.active)
        name_unique = ValidationHelper.check_unique_from_dict(
            data=env.projects,
            key='ref',
            value=ref_name
        )
        to_small = True if len(ref_name) < 3 else False
        if not name_unique or to_small:
            return "not unique or to small (min. 3 char)"
        db_exist = PjValidations.validate_db_name_unique(
            username=env.db_user,
            password=env.db_pw,
            name=ref_name
        )
        if db_exist:
            return "Database ealready in exist"
        return True

    @staticmethod
    def validate_unique_name(value):
        env = Environment(Environment.active)
        valid = ValidationHelper.check_unique_from_dict(
            data=env.projects,
            key='name',
            value=value
        )
        to_small = True if len(value) < 3 else False
        return "not unique or to small (min. 3 char)" if not valid or to_small else True