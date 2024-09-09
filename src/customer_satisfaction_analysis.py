import pandas as pd
from scipy.spatial.distance import euclidean
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sqlalchemy import create_engine
from datetime import datetime

# Task 4.1: Calculate Engagement and Experience Scores
def calculate_scores(user_data):
    engagement_clusters = KMeans(n_clusters=2).fit(user_data[['engagement_feature_1', 'engagement_feature_2']])
    experience_clusters = KMeans(n_clusters=2).fit(user_data[['experience_feature_1', 'experience_feature_2']])

    user_data['engagement_score'] = user_data[['engagement_feature_1', 'engagement_feature_2']].apply(
        lambda row: euclidean(row, engagement_clusters.cluster_centers_[0]), axis=1)
    user_data['experience_score'] = user_data[['experience_feature_1', 'experience_feature_2']].apply(
        lambda row: euclidean(row, experience_clusters.cluster_centers_[0]), axis=1)

    return user_data

# Task 4.2: Calculate Satisfaction Score and Report Top 10 Satisfied Customers
def calculate_satisfaction_score(user_data):
    user_data['satisfaction_score'] = user_data[['engagement_score', 'experience_score']].mean(axis=1)
    top_10_customers = user_data.sort_values(by='satisfaction_score', ascending=True).head(10)
    return user_data, top_10_customers

# Task 4.3: Build Regression Model to Predict Satisfaction Score
def regression_model(user_data):
    X = user_data[['engagement_score', 'experience_score']]
    y = user_data['satisfaction_score']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    return model, mse

# Task 4.4: Run K-Means on Engagement and Experience Scores
def kmeans_clustering(user_data):
    kmeans = KMeans(n_clusters=2)
    user_data['cluster'] = kmeans.fit_predict(user_data[['engagement_score', 'experience_score']])
    return user_data

# Task 4.5: Aggregate Satisfaction and Experience Scores per Cluster
def aggregate_clusters(user_data):
    cluster_agg = user_data.groupby('cluster')[['satisfaction_score', 'experience_score']].mean()
    return cluster_agg

# Task 4.6: Export Data to MySQL Database
def export_to_mysql(user_data):
    engine = create_engine('mysql+mysqlconnector://user:password@localhost/mydatabase')
    user_data.to_sql('user_satisfaction_scores', con=engine, if_exists='replace', index=False)

    with engine.connect() as connection:
        result = connection.execute("SELECT * FROM user_satisfaction_scores LIMIT 10").fetchall()
    return result

# Task 4.7: Model Deployment Tracking
def model_deployment_tracking(mse):
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

    pd.DataFrame([log_data]).to_csv('model_deployment_logs.csv', index=False)
    return log_data
