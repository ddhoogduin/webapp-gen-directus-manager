from sqlalchemy import create_engine


class db:
    def __init__(self, username, password):
        self.dialect = 'mysql'
        self.driver = 'pymysql'
        self.host = 'localhost'
        self.username = username
        self.password = password

        self.connection = None

    def connect(self):
        engine = create_engine('{dialect}+{driver}://{user}:{password}@{host}'.format(
            dialect=self.dialect,
            driver=self.driver,
            user=self.username,
            password=self.password,
            host=self.host
        ))
        try:
            connection = engine.connect()
            self.connection = connection
            return True
        except Exception as error:
            print("\nDatabase connection failed\nTry again...\n")
            return False

    def check_name_unique(self, name):
        existing_databases = self.connection.execute("SHOW DATABASES;")
        return True if name in [d[0] for d in existing_databases] else False