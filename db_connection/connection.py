import psycopg2
import pandas as pd

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
            print(f"Error: {e}")

    def fetch_data(self, query):
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
