import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mode
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the dataset
def load_data(query, conn):
    """Load data from the database."""
    return pd.read_sql(query, conn)

# Clean data and aggregate per customer
def clean_data(df):
    for col in ['TCP DL Retrans. Vol (Bytes)', 'Avg RTT DL (ms)', 'Avg Bearer TP DL (kbps)']:
        if col in df.columns:
            mean_value = df[col].mean()
            df[col].fillna(mean_value, inplace=True)
        else:
            print(f"Column '{col}' not found in the DataFrame")
    return df

def aggregate_per_customer(df):
    agg_df = df.groupby('MSISDN/Number').agg({
        'TCP DL Retrans. Vol (Bytes)': 'mean',
        'Avg RTT DL (ms)': 'mean',
        'Avg Bearer TP DL (kbps)': 'mean',
        'Handset Type': 'first'
    }).reset_index()
    
    agg_df.rename(columns={
        'TCP DL Retrans. Vol (Bytes)': 'avg_tcp_retransmission',
        'Avg RTT DL (ms)': 'avg_rtt',
        'Avg Bearer TP DL (kbps)': 'avg_throughput'
    }, inplace=True)
    
    return agg_df

# Get top, bottom, and most frequent values for a column
def get_top_bottom_frequent(df, column):
    top_10 = df[column].nlargest(10)
    bottom_10 = df[column].nsmallest(10)
    most_frequent = df[column].mode().head(10)
    
    return top_10, bottom_10, most_frequent

# Plot throughput and TCP retransmission per handset type
def plot_throughput_distribution(df):
    plt.figure(figsize=(10, 6))  # Adjust figure size to avoid layout issues
    sns.barplot(x='Handset Type', y='avg_throughput', data=df, palette='Blues', legend=False)  # Use legend=False
    plt.title('Throughput Distribution by Handset Type')
    plt.xlabel('Handset Type')
    plt.ylabel('Average Throughput')
    plt.xticks(rotation=45)  # Rotate x-axis labels if necessary
    plt.tight_layout(pad=1.5)  # Adjust padding
    plt.show()

def plot_tcp_retransmission(df):
    plt.figure(figsize=(10, 6))  # Adjust figure size
    sns.barplot(x='Handset Type', y='avg_tcp_retransmission', data=df, palette='Reds', legend=False)  # Fix palette and hue warning
    plt.title('TCP Retransmission by Handset Type')
    plt.xlabel('Handset Type')
    plt.ylabel('Average TCP Retransmission')
    plt.xticks(rotation=45)  # Rotate x-axis labels if necessary
    plt.tight_layout(pad=1.5)  # Adjust padding to fit layout
    plt.show()

# Perform k-means clustering for user experience segmentation
def prepare_clustering_data(df):
    features = df[['avg_tcp_retransmission', 'avg_rtt', 'avg_throughput']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    return scaled_features

def perform_clustering(df, n_clusters=3):
    scaled_data = prepare_clustering_data(df)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(scaled_data)
    return df, kmeans
