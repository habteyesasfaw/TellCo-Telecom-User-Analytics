import pandas as pd
from scipy.spatial.distance import euclidean
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime
from db_connection.connection import PostgresConnection
from sklearn.impute import SimpleImputer

# Load the dataset
def load_data(query, conn):
    """Load data from the database using a PostgresConnection."""
    return conn.fetch_data(query)

# Task 4.1: Calculate Engagement and Experience Scores
def calculate_scores(user_data):
    # Define engagement and experience features
    engagement_features = ['Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)']
    experience_features = ['Avg RTT UL (ms)', 'Avg Bearer TP UL (kbps)']

    # Impute missing values
    imputer = SimpleImputer(strategy='mean')
    user_data[engagement_features] = imputer.fit_transform(user_data[engagement_features])
    user_data[experience_features] = imputer.fit_transform(user_data[experience_features])
    
    # Fit KMeans clustering on engagement and experience features
    engagement_clusters = KMeans(n_clusters=2).fit(user_data[engagement_features])
    experience_clusters = KMeans(n_clusters=2).fit(user_data[experience_features])

    # Calculate engagement scores
    user_data['engagement_score'] = user_data[engagement_features].apply(
        lambda row: euclidean(row, engagement_clusters.cluster_centers_[0]), axis=1)
    
    # Calculate experience scores
    user_data['experience_score'] = user_data[experience_features].apply(
        lambda row: euclidean(row, experience_clusters.cluster_centers_[0]), axis=1)

    return user_data

# Task 4.2: Calculate Satisfaction Score and Report Top 10 Satisfied Customers
def calculate_satisfaction_score(user_data):
    # Compute satisfaction score as the mean of relevant columns
    user_data['satisfaction_score'] = user_data[['Avg RTT UL (ms)', 'Avg Bearer TP UL (kbps)']].mean(axis=1)
    # Identify the top 10 customers based on satisfaction score
    top_10_customers = user_data.sort_values(by='satisfaction_score', ascending=False).head(10)
    return user_data, top_10_customers

# Task 4.3: Build Regression Model to Predict Satisfaction Score
def regression_model(user_data):
    # Define features and target variable
    X = user_data[['Avg RTT UL (ms)', 'Avg Bearer TP UL (kbps)']]
    y = user_data['satisfaction_score']
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Compute Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)
    return model, mse

# Task 4.4: Run K-Means on Engagement and Experience Scores
def kmeans_clustering(user_data):
    # Perform K-Means clustering with 2 clusters
    kmeans = KMeans(n_clusters=2, random_state=42)
    user_data['cluster'] = kmeans.fit_predict(user_data[['Avg RTT UL (ms)', 'Avg Bearer TP UL (kbps)']])
    return user_data

# Task 4.5: Aggregate Satisfaction and Experience Scores per Cluster
def aggregate_clusters(user_data):
    # Aggregate mean scores per cluster
    cluster_agg = user_data.groupby('cluster')[['satisfaction_score', 'Avg RTT UL (ms)', 'Avg Bearer TP UL (kbps)']].mean()
    return cluster_agg

# Task 4.6: Export Data to MySQL Database
def export_to_mysql(user_data):
    # Create SQLAlchemy engine for MySQL
    engine = create_engine('mysql+mysqlconnector://user:password@localhost/mydatabase')
    # Export data to SQL
    user_data.to_sql('user_satisfaction_scores', con=engine, if_exists='replace', index=False)

    # Verify export by querying the database
    with engine.connect() as connection:
        result = connection.execute("SELECT * FROM user_satisfaction_scores LIMIT 10").fetchall()
    return result

# Task 4.7: Model Deployment Tracking
def model_deployment_tracking(mse):
    # Record deployment details
    start_time = datetime.now()
    log_data = {
        'code_version': 'v1.0',
        'start_time': start_time,
        'end_time': datetime.now(),
        'source': 'customer_satisfaction_model',
        'parameters': 'Linear Regression',
        'metrics': {'MSE': mse},
        'artifacts': 'model.pkl'
    }

    # Save logs to a CSV file
    pd.DataFrame([log_data]).to_csv('model_deployment_logs.csv', index=False)
    return log_data