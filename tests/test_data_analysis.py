import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
from sklearn.decomposition import PCA

# Add database connection path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../')))
from db_connection.connection import PostgresConnection

# Initialize Postgres connection
db = PostgresConnection()

def load_data(query):
    """
    Load data from PostgreSQL database.
    """
    conn = db.connect()
    data = pd.read_sql(query, conn)
    conn.close()
    return data

def handle_missing_values(df):
    """
    Handle missing values by replacing them with column means.
    """
    return df.fillna(df.mean())

def perform_univariate_analysis(df):
    """
    Perform univariate analysis by plotting histograms and computing summary statistics.
    """
    for column in df.select_dtypes(include=[np.number]).columns:
        plt.figure(figsize=(8, 6))
        sns.histplot(df[column], kde=True)
        plt.title(f'Distribution of {column}')
        plt.show()

        # Summary statistics
        print(f"Summary statistics for {column}:")
        print(df[column].describe())

def perform_pca(df, n_components=2):
    """
    Perform Principal Component Analysis (PCA) on the numerical dataset.
    """
    pca = PCA(n_components=n_components)
    numerical_data = df.select_dtypes(include=[np.number])
    pca_result = pca.fit_transform(numerical_data)
    
    explained_variance = pca.explained_variance_ratio_
    print(f"Explained variance by component: {explained_variance}")
    
    return pca_result, explained_variance

def visualize_pca(pca_result, labels):
    """
    Visualize the PCA results in a scatter plot.
    """
    plt.figure(figsize=(10, 8))
    plt.scatter(pca_result[:, 0], pca_result[:, 1], c=labels, cmap='viridis')
    plt.title("PCA Scatter Plot")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.colorbar()
    plt.show()

def correlation_matrix(df):
    """
    Compute and display the correlation matrix of numerical data.
    """
    correlation = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()
    return correlation

# Sample query to load data
query = "SELECT * FROM telecom_data"  # Replace with your actual query
data = load_data(query)

# Handle missing values
data_cleaned = handle_missing_values(data)

# Perform univariate analysis
perform_univariate_analysis(data_cleaned)

# Perform PCA
pca_result, explained_variance = perform_pca(data_cleaned)

# Visualize PCA
labels = data_cleaned['target_column']  # Replace with the actual label column for color coding
visualize_pca(pca_result, labels)

# Compute correlation matrix
correlation_matrix(data_cleaned)
