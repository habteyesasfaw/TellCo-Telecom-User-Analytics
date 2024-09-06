import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def load_data(query, conn):
    """Load data from the database."""
    return pd.read_sql(query, conn)

def aggregate_engagement(df):
    """Aggregate engagement metrics per customer."""
    # Calculate total traffic as the sum of total upload and download bytes
    df['total_traffic'] = df['Total UL (Bytes)'] + df['Total DL (Bytes)']
    
    # Aggregate per customer
    user_agg = df.groupby('MSISDN/Number').agg({
        'Bearer Id': 'count',            # Session frequency per user
        'Dur. (ms)': 'sum',              # Total session duration per user
        'total_traffic': 'sum'           # Total traffic per user
    }).reset_index()
    
    # Rename columns for clarity
    user_agg.rename(columns={
        'Bearer Id': 'sessions_frequency',
        'Dur. (ms)': 'session_duration'
    }, inplace=True)
    
    return user_agg


def normalize_data(df, columns):
    """Normalize specified columns in the dataframe."""
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[columns])
    scaled_df = pd.DataFrame(scaled, columns=[f'scaled_{col}' for col in columns])
    return scaled_df

def kmeans_clustering(df, columns, n_clusters=3):
    """Perform K-Means clustering."""
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(df[columns])
    df['cluster'] = kmeans.labels_
    return df, kmeans

def plot_elbow_method(df, columns):
    """Determine optimal k for K-Means using Elbow Method."""
    inertia = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=0).fit(df[columns])
        inertia.append(kmeans.inertia_)
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, 11), inertia, marker='o')
    plt.title('Elbow Method for Optimal k')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Inertia')
    plt.show()

def compute_silhouette_score(df, columns, kmeans):
    """Compute silhouette score for the chosen k."""
    return silhouette_score(df[columns], kmeans.labels_)

def plot_top_apps(df):
    """Plot the top 3 most used applications."""
    # Aggregate total traffic for each application
    app_traffic = {
        'Social Media': df['Social Media DL (Bytes)'].sum(),
        'Google': df['Google DL (Bytes)'].sum(),
        'Youtube': df['Youtube DL (Bytes)'].sum(),
        'Netflix': df['Netflix DL (Bytes)'].sum(),
        'Gaming': df['Gaming DL (Bytes)'].sum(),
        'Other': df['Other DL (Bytes)'].sum()
    }
    
    # Convert to a DataFrame for easier plotting
    app_traffic_df = pd.DataFrame(list(app_traffic.items()), columns=['Application', 'Total Traffic'])
    
    # Select the top 3 applications by traffic
    top_3_apps = app_traffic_df.nlargest(3, 'Total Traffic')
    
    # Plot the top 3 applications
    top_3_apps.plot(kind='bar', x='Application', y='Total Traffic', legend=False)
    plt.title('Top 3 Most Used Applications')
    plt.xlabel('Application')
    plt.ylabel('Total Traffic (Bytes)')
    plt.show()

