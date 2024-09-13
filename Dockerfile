# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run the application
CMD ["python", "/app/src/customer_satisfaction_analysis.py"]
# 

# # Use the Python 3.9-slim as the base image
# FROM python:3.9-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy only the necessary files to install dependencies (cache optimization)
# COPY requirements.txt .

# # Install virtualenv
# RUN python -m venv .venv

# # Activate the virtual environment and upgrade pip
# RUN . .venv/bin/activate && pip install --upgrade pip

# # Install the dependencies within the virtual environment
# RUN . .venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code to the working directory
# COPY . .

# # Expose the port Streamlit will run on
# EXPOSE 8501

# # Set the default command to activate the virtual environment and run the Streamlit app
# CMD ["/bin/bash", "-c", ". .venv/bin/activate && /app/src/customer_satisfaction_analysis.py"]