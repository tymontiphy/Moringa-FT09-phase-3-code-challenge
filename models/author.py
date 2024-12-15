from database.connection import Connection

class Author:
    def __init__(self, id, name):
        self._validate_init_params(id, name)
        self._id = id
        self._name = name

    @staticmethod
    def _validate_init_params(id, name):
        if not isinstance(id, int):
            raise ValueError("ID must be an integer.")
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string.")

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Cannot change name after initialization.")

    def articles(self):
        query = "SELECT * FROM articles WHERE author_id = ?;"
        return Connection.get_db_connection().execute(query, (self.id,)).fetchall()

    def magazines(self):
        query = """
            SELECT DISTINCT m.* 
            FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?;
        """
        return Connection.get_db_connection().execute(query, (self.id,)).fetchall()
