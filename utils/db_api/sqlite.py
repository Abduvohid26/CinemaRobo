import sqlite3

from pydantic.v1.validators import anystr_strip_whitespace


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db
    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)
    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    # Create table
    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname varchar(255),
            telegram_id varchar(20) UNIQUE,
            language varchar(3)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, fullname: str, telegram_id: str = None, language: str = 'uz'):

        sql = """
        INSERT INTO Users(fullname,telegram_id, language) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(fullname, telegram_id, language), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)
    
    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)
    
    def update_user_fullname(self, email, telegram_id):

        sql = f"""
        UPDATE Users SET fullname=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(telegram_id, id), commit=True)
    
    
    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


    def create_cinema_table(self):
        sql = """
             CREATE TABLE Cinema(
                id str,
                main_id int,
                post_id int
             );
        """
        self.execute(sql, commit=True)

    def add_cinema(self, id: str, main_id: int, post_id: int):
        sql = """
         INSERT INTO Cinema(id, main_id, post_id) VALUES(?,?,?)
        """
        self.execute(sql, parameters=(id, main_id, post_id), commit=True)

    def select_all_cinema(self, main_id):
        sql = """
            SELECT * FROM Cinema Where main_id = ?
        """
        return self.execute(sql, parameters=(main_id, ), fetchall=True)


    # def select_all_users(self):
    #     sql = """
    #     SELECT * FROM Users
    #     """
    #     return self.execute(sql, fetchall=True)
    #
    def select_cinema(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Cinema WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)


#     def create_table_users(self):
#         sql = """
#         CREATE TABLE Channels (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             channel_id INTEGER UNIQUE NOT NULL
#             );
# """
#         self.execute(sql, commit=True)


    def create_table_channel_ids(self):
            sql = """
            CREATE TABLE IF NOT EXISTS Channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id VARCHAR(25) UNIQUE NOT NULL
                );
    """
            self.execute(sql, commit=True)

    def select_all_channels(self):
        sql = """
        SELECT * FROM Channels
        """
        return self.execute(sql, fetchall=True)

    def channel_delete(self, channel_id):
        sql = """
        DELETE FROM Channels WHERE channel_id = ?
        """
        self.execute(sql, (channel_id,), commit=True)

    def add_channel(self, channel_id: str):
        sql = """
        INSERT OR IGNORE INTO Channels (channel_id) VALUES (?)
        """
        self.execute(sql, parameters=(channel_id,), commit=True)

    def select_channel(self, **kwargs):
        sql = "SELECT * FROM Channels WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)
