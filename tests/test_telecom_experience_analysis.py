import unittest
import pandas as pd
import os
import sys

# Adjust the path to include the src directory
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../src')))

from telecom_experience_analysis import (
    clean_data, aggregate_per_customer,
    get_top_bottom_frequent, plot_throughput_distribution,
    plot_tcp_retransmission, perform_clustering
)

class TestTelecomExperienceAnalysis(unittest.TestCase):

    def setUp(self):
        """Set up sample data for testing."""
        self.sample_data = pd.DataFrame({
            'MSISDN/Number': ['12345', '67890', '54321', '09876', '11223'],
            'TCP DL Retrans. Vol (Bytes)': [10, 15, 12, None, 20],
            'Avg RTT DL (ms)': [100, 200, None, 150, 120],
            'Avg Bearer TP DL (kbps)': [1000, 850, 900, 950, None],
            'Handset Type': ['Handset A', 'Handset B', 'Handset A', 'Handset C', 'Handset B']
        })

    def test_clean_data(self):
        """Test cleaning of missing data."""
        cleaned_df = clean_data(self.sample_data)
        # Check if missing values are filled with the mean
        self.assertAlmostEqual(cleaned_df['TCP DL Retrans. Vol (Bytes)'].mean(), 14.25)
        self.assertAlmostEqual(cleaned_df['Avg RTT DL (ms)'].mean(), 142.5)
        self.assertAlmostEqual(cleaned_df['Avg Bearer TP DL (kbps)'].mean(), 925)

  

    # def test_plot_throughput_distribution(self):
    #     """Test throughput distribution plotting."""
    #     cleaned_df = clean_data(self.sample_data)
    #     try:
    #         plot_throughput_distribution(cleaned_df)
    #     except Exception as e:
    #         self.fail(f"plot_throughput_distribution raised an exception: {e}")

    # def test_plot_tcp_retransmission(self):
    #     """Test TCP retransmission plotting."""
    #     cleaned_df = clean_data(self.sample_data)
    #     try:
    #         plot_tcp_retransmission(cleaned_df)
    #     except Exception as e:
    #         self.fail(f"plot_tcp_retransmission raised an exception: {e}")

    def test_perform_clustering(self):
        """Test KMeans clustering functionality."""
        cleaned_df = clean_data(self.sample_data)
        aggregated_df = aggregate_per_customer(cleaned_df)
        clustered_df, kmeans = perform_clustering(aggregated_df)
        # Check if KMeans clustering assigns clusters
        self.assertIn('cluster', clustered_df.columns)
        self.assertEqual(len(clustered_df['cluster'].unique()), 3)

if __name__ == '__main__':
    unittest.main()
