
import sqlite3
from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self._id = id
        self.name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if hasattr(self, '_name'):
            print("Name cannot be changed once set.")
            return
        if isinstance(value, str) and len(value) > 0:
            self._name = value
        else:
            print("Name must be a non-empty string.")

    def __repr__(self):
        return f'<Author {self.name}>'

    @classmethod
    def create(cls, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (name,))
        conn.commit()
        author_id = cursor.lastrowid
        conn.close()
        return cls(author_id, name)

    @classmethod
    def get_by_id(cls, author_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (author_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row['id'], row['name'])

    @classmethod
    def delete(cls, author_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM authors WHERE id = ?', (author_id,))
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            print(f"No author found with ID {author_id}")

    def articles(self):
        from models.article import Article  # Local import to avoid circular dependency
        # Fetch all articles by the author using SQL JOIN
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
        ''', (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(row['id'], row['title'], row['content'], row['author_id'], row['magazine_id']) for row in rows]

    def magazines(self):
        from models.magazine import Magazine  # Local import to avoid circular dependency
        # Fetch all magazines associated with the author using SQL JOIN
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.id, magazines.name, magazines.category
            FROM articles
            JOIN authors ON articles.author_id = authors.id
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE authors.id = ?
        ''', (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(row['id'], row['name'], row['category']) for row in rows]
