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

# Example usage
if __name__ == "__main__":
    db = PostgresConnection()
    db.connect()

    # Fetch data from xdr_data table
    query = "SELECT * FROM xdr_data;"
    df = db.fetch_data(query)
    
    if df is not None:
        print("Column Names:", df.columns)  # Print column names
        print(df.head())  # Display the first 5 rows

        # Use actual column names from df.columns
        user_agg = df.groupby('MSISDN/Number').agg(
            num_sessions=('actual_bearer_id_column', 'count'),  # Update with correct column names
            total_duration=('actual_session_duration_column', 'sum'),
            total_dl=('actual_total_dl_bytes_column', 'sum'),
            total_ul=('actual_total_ul_bytes_column', 'sum')
        ).reset_index()

        print(user_agg)
        top_handsets = df['handset'].value_counts().head(10)



    db.close()
