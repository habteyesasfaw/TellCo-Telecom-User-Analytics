import pandas as pd
import psycopg2

class PostgresConnection:
    def __init__(self, dbname='telecom', user='postgres', password='root', host='localhost', port='5432'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Connected to PostgreSQL Database!")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def execute_query(self, query, fetch=False):
        try:
            if self.conn:
                with self.conn.cursor() as cursor:
                    cursor.execute(query)
                    if fetch:
                        return cursor.fetchall()
                    self.conn.commit()
            else:
                print("No connection found.")
        except Exception as e:
            print(f"Error executing query: {e}")

    def fetch_data(self, query):
        """Fetch data from the database and return as a DataFrame."""
        try:
            if self.conn:
                return pd.read_sql_query(query, self.conn)
            else:
                print("No connection found.")
                return None
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()
            print("Connection closed.")
