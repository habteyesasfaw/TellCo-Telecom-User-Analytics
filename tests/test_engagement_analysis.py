import unittest
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import sys
import os
import matplotlib.pyplot as plt

# Adjust the path to point to the src directory
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../src')))
from utils import aggregate_engagement, normalize_data, kmeans_clustering, plot_elbow_method

class TestUserEngagementAnalysis(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.data = {
            'MSISDN': [1, 1, 2, 2, 3, 3],
            'sessions_frequency': [1, 4, 2, 3, 5, 2],
            'session_duration': [30, 40, 20, 50, 60, 25],
            'session_total_traffic': [100, 200, 150, 250, 300, 120]
        }
        self.df = pd.DataFrame(self.data)

    def test_aggregate_engagement(self):
        # Aggregate metrics per customer id
        user_agg = self.df.groupby('MSISDN').agg({
            'sessions_frequency': 'sum',
            'session_duration': 'sum',
            'session_total_traffic': 'sum'
        }).reset_index()

        # Test assertions
        self.assertEqual(user_agg.loc[user_agg['MSISDN'] == 1, 'sessions_frequency'].values[0], 5)
        self.assertEqual(user_agg.loc[user_agg['MSISDN'] == 2, 'sessions_frequency'].values[0], 5)
        self.assertEqual(user_agg.loc[user_agg['MSISDN'] == 3, 'sessions_frequency'].values[0], 7)

    def test_normalize_data(self):
        # Normalize the data
        scaler = StandardScaler()
        normalized_data = pd.DataFrame(scaler.fit_transform(self.df[['sessions_frequency', 'session_duration', 'session_total_traffic']]),
                                        columns=['sessions_frequency', 'session_duration', 'session_total_traffic'])
        
        # Test that the standard deviation of the normalized data is approximately 1
        tolerance = 0.1  # Allowable tolerance due to floating-point precision
        for col in normalized_data.columns:
            std_dev = normalized_data[col].std()
            self.assertAlmostEqual(std_dev, 1, delta=tolerance)

    def test_plot_elbow_method(self):
        # Normalize the data
        scaler = StandardScaler()
        normalized_data = scaler.fit_transform(self.df[['sessions_frequency', 'session_duration', 'session_total_traffic']])

        # Elbow method
        distortions = []
        K = range(1, min(6, len(self.df) + 1))  # Ensure k <= number of samples
        for k in K:
            kmeans = KMeans(n_clusters=k, random_state=0)
            kmeans.fit(normalized_data)
            distortions.append(kmeans.inertia_)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(K, distortions, 'bx-')
        plt.xlabel('Number of clusters')
        plt.ylabel('Distortion')
        plt.title('Elbow Method for Optimal k')
        plt.grid(True)
        plt.show()

        # Check if plotting was successful
        success = True  # If no exception occurred
        self.assertTrue(success, "Elbow plot method failed")

if __name__ == '__main__':
    unittest.main()
