import os


class DirectusController:

    @staticmethod
    def install_config(path, db_name, db_user, db_pw, pj_name):
        os.system("cd {path} && php bin/directus install:config"
                  " -h localhost"
                  " -n {db_name}"
                  " -u {db_user}"
                  " -p {db_pw}"
                  " -N {pj_name} -f".format(
                    path=path,
                    db_name=db_name,
                    db_user=db_user,
                    db_pw=db_pw,
                    pj_name=pj_name))

    @staticmethod
    def init_directus(path):
        os.system('cd {path} && bin/directus install:config -n filler -u filler -p filler'.format(
            path=path
        ))


    @staticmethod
    def delete_config(path, pj_name):
        os.system('cd {path} && rm ./config/api.{ref_name}.php'.format(
            path=path,
            ref_name=pj_name
        ))

    @staticmethod
    def install_database(path, pj_name):
        os.system("cd {path} && php bin/directus install:database -N {pj_name}".format(
                    path=path,
                    pj_name=pj_name))

    @staticmethod
    def init_user(path, pj_name):
        os.system("cd {path} && php bin/directus install:install -e {pj_name}@example.com"
                  " -p password"
                  " -N {pj_name}".format(
                    path=path,
                    pj_name=pj_name))
