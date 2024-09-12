import pandas as pd
import psycopg2
import sys
import os

# Add the path to the custom database connection class
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../')))

from db_connection.connection import PostgresConnection  # Import the database connection class

# Step 1: Data Preparation
def prepare_user_data():
    """Prepare the user data for insertion into the database."""
    data = {
        'user_engagement': [75.3, 65.7, 82.9, 88.0, 76.5],
        'user_experience': [80.2, 70.5, 85.7, 82.0, 77.8],
        'user_satisfaction': [90.1, 88.9, 92.4, 89.0, 85.5]
    }
    return pd.DataFrame(data)

# Step 2: Table Creation
def create_user_scores_table(db_connection):
    """Create the user_scores table in the PostgreSQL database."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS user_scores (
        user_id SERIAL PRIMARY KEY,
        user_engagement FLOAT NOT NULL,
        user_experience FLOAT NOT NULL,
        user_satisfaction FLOAT NOT NULL
    );
    """
    db_connection.execute_query(create_table_sql)
    print("Table 'user_scores' created successfully.")

# Step 3: Data Insertion
def insert_user_data(db_connection, user_data_df):
    """Insert user data into the user_scores table."""
    for _, row in user_data_df.iterrows():
        insert_sql = f"""
        INSERT INTO user_scores (user_engagement, user_experience, user_satisfaction)
        VALUES ({row['user_engagement']}, {row['user_experience']}, {row['user_satisfaction']});
        """
        db_connection.execute_query(insert_sql)
    print("User data inserted successfully.")

# Step 4: Fetch and Display Data
def fetch_and_display_user_scores(db_connection):
    """Fetch user data from the user_scores table and display it."""
    select_sql = "SELECT * FROM user_scores;"
    results = db_connection.execute_query(select_sql, fetch=True)
    
    print("\nUser Scores Data:")
    print("User_ID | User_Engagement | User_Experience | User_Satisfaction")
    for row in results:
        print(row)

# Step 5: Export Data to CSV
def export_data_to_csv(db_connection, filename='user_scores_export.csv'):
    """Export user data from the user_scores table to a CSV file."""
    select_sql = "SELECT * FROM user_scores;"
    df = db_connection.fetch_data(select_sql)
    
    if df is not None:
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename} successfully.")
    else:
        print("No data available to export.")

# Step 6: Main function to run the process
def main():
    """Main function to execute the database operations."""
    # Initialize database connection
    db_connection = PostgresConnection(dbname='telecom', user='postgres', password='root', host='localhost', port='5432')
    db_connection.connect()

    # Prepare the user data
    user_data_df = prepare_user_data()

    # Create the table
    create_user_scores_table(db_connection)

    # Insert data into the table
    insert_user_data(db_connection, user_data_df)

    # Fetch and display the inserted data
    fetch_and_display_user_scores(db_connection)

    # Export the data to CSV
    export_data_to_csv(db_connection)

    # Close the connection
    db_connection.close()

# Execute the main function when the script is run
if __name__ == "__main__":
    main()
