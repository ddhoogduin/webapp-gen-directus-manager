from engine.Validations import EnvValidations, PjValidations


class EnvQuestions:

    introduction = [
        {
            'type': 'list',
            'name': 'task',
            'message': 'Select a environment option to continue:',
            'choices': ['create']
        }
    ]
    load = [
        {
            'type': 'list',
            'name': 'env_ref',
            'message': 'Select a Directus environment:',
            'choices': ['<- back']
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
    delete = [

        {
            'type': 'list',
            'name': 'ref_name',
            'message': 'Select a Directus environment:',
            'choices': []
        },
        {
            'type': 'confirm',
            'name': 'keep_db',
            'message': 'Do you also want to keep all env related databases?:'
        },
        {
            'type': 'confirm',
            'name': 'confirmation',
            'message': 'Are you sure you want to completely delete the environment?:'
        }

    ]
    reset = [
        {
            'type': 'confirm',
            'name': 'confirmation',
            'message': 'Are you sure you want to completely delete ALL environments and migrations?:'
        },

        {
            'type': 'confirm',
            'name': 'keep_db',
            'message': 'Do you also want to keep all related databases?:'
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
    close = [
        {
            'type': 'list',
            'name': 'close_action',
            'message': 'Cancelling action, select an option:',
            'choices': ['back to main options', 'exit module']
        }
    ]

class PjQuestions:
    introduction = [
        {
            'type': 'list',
            'name': 'task',
            'message': 'Environment tasks:',
            'choices': []
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
    select_project = [
        {
            'type': 'list',
            'name': 'pj_ref',
            'message': 'Projects in environment:',
            'choices': []
        }
    ]
    project_task = [
        {
            'type': 'list',
            'name': 'pj_task',
            'message': 'Project tasks:',
            'choices': ['templatify project database', 'delete project']
        }
    ]
    delete = [
        {
            'type': 'confirm',
            'name': 'keep_db',
            'message': 'Do you want to keep the project database :'
        },
        {
            'type': 'confirm',
            'name': 'confirmation',
            'message': 'Are you sure you want to delete this project? :'
        }
    ]
    link = [
        {
            'type': 'list',
            'name': 'database_name',
            'message': 'Select a database:',
            'choices': []
        },
        {
            'type': 'input',
            'name': 'install_ref',
            'message': 'Enter a unique reference for the project:',
            'validate': PjValidations.validate_unique_ref_name
        },
        create[1]
    ]
    migrations = [
        {
            'type': 'confirm',
            'name': 'use_migration',
            'message': 'Do you want to use a database template?:'
        },
        {
            'type': 'list',
            'name': 'migration_file',
            'message': 'Select a migration file:',
            'choices': ['test']
        }
    ]
    close = [
        {
            'type': 'list',
            'name': 'close_action',
            'message': 'Cancelling action, select an option:',
            'choices': ['back to environment options', 'exit module']
        }
    ]