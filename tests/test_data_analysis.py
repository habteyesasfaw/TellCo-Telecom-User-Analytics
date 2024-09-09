import unittest
import pandas as pd
import numpy as np

# Updated handle_missing_values function
def handle_missing_values(df):
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
    return df

# Test class
class TestUserOverviewAnalysis(unittest.TestCase):

    def setUp(self):
        """Set up a sample dataset."""
        data = {
            'MSISDN/Number': ['user1', 'user2', 'user3'],
            'Bearer Id': [5, 10, np.nan],  # One missing value
            'Dur. (ms)': [1000, 2000, 3000],  # Session duration
            'Total DL (Bytes)': [100, 200, 300],  # Download data
            'Total UL (Bytes)': [50, 100, np.nan],  # One missing value in upload
        }
        self.df = pd.DataFrame(data)

    def test_handle_missing_values(self):
        """Test if missing values are correctly replaced."""
        cleaned_df = handle_missing_values(self.df)

        # Check if there are no missing values after handling
        self.assertFalse(cleaned_df.isnull().values.any())

        # Check if missing values were replaced by the correct mean
        self.assertEqual(cleaned_df.loc[2, 'Bearer Id'], self.df['Bearer Id'].mean())
        self.assertEqual(cleaned_df.loc[2, 'Total UL (Bytes)'], self.df['Total UL (Bytes)'].mean())

# Run the tests
unittest.main(argv=[''], verbosity=2, exit=False)
