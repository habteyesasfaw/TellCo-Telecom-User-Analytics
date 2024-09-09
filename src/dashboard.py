
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your aggregated data
# Load the dataset
def load_data(query, conn):
    """Load data from the database."""
    return pd.read_sql(query, conn)

# Main dashboard function
def dashboard():
    st.title("Telecom User Experience Dashboard")
    
    # Load the data
    df = load_data()

    # Sidebar for filters
    st.sidebar.header("Filters")
    handset_type = st.sidebar.selectbox("Select Handset Type", df['Handset Type'].unique())
    
    # Filter the data based on the selected handset type
    filtered_df = df[df['Handset Type'] == handset_type]
    
    # Show some key statistics
    st.header(f"Statistics for {handset_type}")
    st.write(f"Average Throughput: {filtered_df['avg_throughput'].mean():.2f} kbps")
    st.write(f"Average RTT: {filtered_df['avg_rtt'].mean():.2f} ms")
    st.write(f"Average TCP Retransmission: {filtered_df['avg_tcp_retransmission'].mean():.2f} bytes")
    
    # Plot Throughput Distribution
    st.subheader("Distribution of Throughput")
    plt.figure(figsize=(10, 6))
    sns.histplot(filtered_df['avg_throughput'], kde=True, color='blue')
    plt.xlabel('Throughput (kbps)')
    plt.ylabel('Frequency')
    st.pyplot(plt)
    
    # Plot TCP Retransmission
    st.subheader("TCP Retransmission per Handset Type")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Handset Type', y='avg_tcp_retransmission', data=df)
    plt.xticks(rotation=45)
    plt.xlabel('Handset Type')
    plt.ylabel('Average TCP Retransmission (Bytes)')
    st.pyplot(plt)
    
    # Add interactive elements
    st.sidebar.header("Additional Filters")
    throughput_range = st.sidebar.slider('Throughput Range', min_value=int(df['avg_throughput'].min()), max_value=int(df['avg_throughput'].max()), value=(200, 1000))
    st.write(f"Selected throughput range: {throughput_range}")

# Run the dashboard
if __name__ == "__main__":
    dashboard()
