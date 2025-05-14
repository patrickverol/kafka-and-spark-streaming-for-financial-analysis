# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Create start script
RUN echo '#!/bin/bash\n\
echo "Waiting for Cassandra..."\n\
while ! nc -z cassandra_db 9042; do\n\
  sleep 1\n\
done\n\
echo "Cassandra is up!"\n\
streamlit run app.py --server.address 0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

# Create a non-root user and switch to it
RUN useradd -m -u 1000 streamlit && \
    chown -R streamlit:streamlit /app
USER streamlit

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run the start script when the container launches
CMD ["/app/start.sh"] 