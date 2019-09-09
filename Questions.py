from engine.Validations import EnvValidations, PjValidations


class EnvQuestions:

    introduction = [
        {
            'type': 'list',
            'name': 'task',
            'message': 'Select a environment option to continue:',
            'choices': []
        }
    ]
    load = [
        {
            'type': 'list',
            'name': 'env_ref',
            'message': 'Select a Directus environment:',
            'choices': []
        }
    ]
    create = [
        {
            'type': 'input',
            'name': 'install_name',
            'message': 'Enter a unique name for the Directus environment:',
            'validate': EnvValidations.validate_unique_name
        }
    ]
    env_db = [
        {
            'type': 'input',
            'name': 'username',
            'message': 'Enter the database username for the local env:'
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'Enter the database password for the local env:'
        }
    ]


class PjQuestions:
    introduction = [
        {
            'type': 'list',
            'name': 'task',
            'message': 'Select a project option to continue:',
            'choices': ['create', 'project settings', 'link']
        }
    ]
    create = [
        {
            'type': 'input',
            'name': 'install_ref',
            'message': 'Enter a unique reference for the project:',
            'validate': PjValidations.validate_unique_ref
        },
        {
            'type': 'input',
            'name': 'install_name',
            'message': 'Enter a unique name for the project:',
            'validate': PjValidations.validate_unique_name
        }
    ]