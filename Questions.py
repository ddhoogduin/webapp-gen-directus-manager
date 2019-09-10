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
            'message': 'Environment tasks:',
            'choices': ['create project', 'project settings', 'link project to database']
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
            'choices': ['Templatify project database', 'Delete project']
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