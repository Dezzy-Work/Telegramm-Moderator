import psycopg2
from config import host, user, password, db_name

class BotBD:

    def __init__(self):
        self.connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        # Checking the user in the database
        self.cursor.execute("SELECT id FROM users WHERE username = '%s';", (user_id,))
        return bool(len(self.cursor.fetchall()))

    def add_user(self, user_id):
        #
        # Adding a person to the database
        try:
            self.cursor.execute("INSERT INTO users(username) VALUES (%s);", (user_id,))
        except Exception:
            self.cursor.execute("rollback")
            self.cursor.execute("INSERT INTO users(username) VALUES (%s);", (user_id,))

        self.connection.commit()
