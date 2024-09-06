import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../src')))

from db_connection.connection import PostgresConnection
from utils import load_data, aggregate_engagement, normalize_data, kmeans_clustering, plot_elbow_method, plot_top_apps

# Main script execution
if __name__ == "__main__":
    db = PostgresConnection()
    db.connect()

    # Fetch data
    query = "SELECT * FROM xdr_data;"
    df = load_data(query, db)
    
    if df is not None:
        # Aggregate and analyze data
        user_agg = aggregate_engagement(df)
        normalized_data = normalize_data(user_agg, ['session_frequency', 'session_duration', 'total_traffic_DL_UL'])
        
        # Determine optimal number of clusters
        plot_elbow_method(normalized_data, ['scaled_session_frequency', 'scaled_session_duration', 'scaled_total_traffic_DL_UL'])
        
        # Apply KMeans clustering
        kmeans_df, kmeans_model = kmeans_clustering(normalized_data, ['scaled_session_frequency', 'scaled_session_duration', 'scaled_total_traffic_DL_UL'], n_clusters=3)
        user_agg['cluster'] = kmeans_df['cluster']
        
        # Print cluster summaries
        print(user_agg.groupby('cluster').agg(
            num_users=('MSISDN', 'count'),
            avg_sessions=('session_frequency', 'mean'),
            avg_duration=('session_duration', 'mean'),
            avg_traffic=('total_traffic_DL_UL', 'mean')
        ))

        # Plot top applications
        plot_top_apps(df)

    db.close()
