import re
from engine.Environment import Environment

class ValidationHelper():

    @staticmethod
    def check_unique_from_dict(data, key, value):
        for pj in data:
            if pj[key] == value:
                return False
        return True


class EnvValidations():

    @staticmethod
    def validate_unique_path(value):
        return ValidationHelper.check_unique_from_dict(
            data=Environment.env_list,
            key='path',
            value=value
        )

    @staticmethod
    def validate_unique_name(value):
        ref_name = re.sub('[\W_]+', '', value)
        valid = ValidationHelper.check_unique_from_dict(
            data=Environment.env_list,
            key='name',
            value=ref_name
        )
        to_small = True if len(ref_name) < 3 else False
        return "not unique or to small (min. 3 char)" if not valid or to_small else True
