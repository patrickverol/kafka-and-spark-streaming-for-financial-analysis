<h1 align="center">
    Kafka and Spark Streaming for Real-Time Financial Data Analytics
</h1>

<br>
    <div align="center">
        <a><img src="https://github.com/user-attachments/assets/f867038e-4d7f-451f-9398-b9f9cd0ad3db"></a> 
    </div>
</br>

<div align="center">
    <a href = "https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white" target="_blank"></a>
    <a href = "https://docs.docker.com/"><img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" target="_blank"></a>
    <a href = "https://airflow.apache.org/docs/"><img src="https://img.shields.io/badge/Apache%20Airflow-017CEE.svg?style=for-the-badge&logo=Apache-Airflow&logoColor=white" target="_blank"></a>
    <a href = "https://kafka.apache.org/documentation/"><img src="https://img.shields.io/badge/Apache%20Kafka-231F20.svg?style=for-the-badge&logo=Apache-Kafka&logoColor=white" target="_blank"></a>
    <a href = "https://spark.apache.org/docs/latest/streaming-programming-guide.html"><img src="https://img.shields.io/badge/Apache%20Spark-E25A1C.svg?style=for-the-badge&logo=Apache-Spark&logoColor=white"></a>
    <a href = "https://cassandra.apache.org/doc/latest/index.html"><img src="https://img.shields.io/badge/Apache%20Cassandra-1287B1.svg?style=for-the-badge&logo=Apache-Cassandra&logoColor=white" target="_blank"></a> 
    <a href = "https://docs.streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=for-the-badge&logo=Streamlit&logoColor=white" target="_blank"></a>
    
</div> 

## About the project

This project implements a real-time financial data analytics platform using Apache Kafka, Apache Cassandra, Apache Spark, and Apache Airflow. The system collects financial data from Alpha Vantage API, processes it through Kafka and Spark Streaming, stores it in Cassandra, and provides real-time analytics through a Streamlit web application.

## Architecture Overview

The system is designed with a microservices architecture, divided into three distinct environments for better scalability and maintainability:

1. **Server Environment (Docker Compose)**
   - Manages the data ingestion pipeline
   - Orchestrates the ETL process using Airflow
   - Handles API data collection and Kafka message production
   - Advantages:
     - Centralized orchestration
     - Easy monitoring of data ingestion
     - Scalable API data collection
     - Independent scaling of Kafka brokers

2. **Client Environment (Docker)**
   - Processes streaming data using Spark
   - Consumes messages from Kafka topics
   - Stores processed data in Cassandra
   - Advantages:
     - Independent scaling of data processing
     - Can run multiple consumers for different purposes
     - Better resource isolation
     - Flexible deployment options

3. **Frontend Environment (Docker)**
   - Provides real-time analytics dashboard using Streamlit
   - Queries data from Cassandra
   - Visualizes financial metrics and indicators
   - Advantages:
     - Independent scaling of web interface
     - Can be deployed closer to end-users
     - Easy to update and maintain
     - Separate resource allocation

## Data Flow and Storage Strategy

The system implements a sophisticated data partitioning strategy:

1. **Kafka Topics**
   - Each stock has its own dedicated topic (e.g., `NVDA_topic`, `IBM_topic`)
   - Advantages:
     - Better data isolation
     - Independent scaling of message processing
     - Easier monitoring per stock
     - Improved fault tolerance

2. **Cassandra Tables**
   - Each stock has its own table (e.g., `stock_NVDA`, `stock_IBM`)
   - Advantages:
     - Optimized query performance
     - Better data organization
     - Easier data management
     - Improved scalability

3. **Streamlit Dashboard**
   - Dynamically queries the appropriate table based on user selection
   - Advantages:
     - Faster data retrieval
     - Better user experience
     - More efficient resource usage
     - Easier to add new stocks

This architecture provides several key benefits:
- **Scalability**: Each component can be scaled independently
- **Maintainability**: Issues in one component don't affect others
- **Flexibility**: Easy to add new stocks or modify processing logic
- **Performance**: Optimized data flow and storage
- **Reliability**: Better fault isolation and recovery
- **Monitoring**: Clear separation of concerns for easier debugging

## Project Structure

```
├── app/                                                       # Streamlit web application
│   ├── app.py                                                 # Main application code
│   ├── Dockerfile                                             # Container configuration
│   └── requirements.txt                                       # Python dependencies
├── server/                                                    # Airflow DAGs and infrastructure
│   ├── dags/                                                  # Airflow DAG definitions
│   │   └── kafka_stream.py                                    # Data ingestion DAG
│   ├── docker-compose.yml                                     # Infrastructure services
│   │   ├── Kafka (broker, schema-registry, control-center)
│   │   ├── Airflow (webserver, scheduler, postgres)
│   │   ├── Spark (master, worker)
│   │   └── Cassandra
│   └── requirements.txt                                       # Airflow dependencies
├── client/                                                    # Spark consumer
│   ├── consumer_stream.py                                     # Kafka consumer code
│   ├── Dockerfile                                             # Container configuration
│   └── requirements.txt                                       # Spark and processing dependencies
└── README.md                                                  # Project documentation
```

---

## Accessing the Services

1. **Airflow UI**
   - URL: http://localhost:8080
   - Default credentials:
     - Username: admin
     - Password: admin

2. **Streamlit Web App**
   - URL: http://localhost:8501

3. **Kafka Control Center**
   - URL: http://localhost:9021

---

## Requirements

- Docker
- Docker Compose
- Python 3.9+
- Alpha Vantage API key

---

## Setup Instructions
1. Clone the repository (*Section below*)
2. Set up environment variables (*Section below*)
3. Start the server by running `docker compose up --build` to initialize the containers. If you want to run it in the background, add `-d` argument
4. Wait for all services to start
5. Go to Airflow UI and start the data pipeline to send data to Kafka (*Section below*)
6. Start the client, to move data from kafka to Cassandra using Spark Streaming (*Section below*)
7. Start the app to visualize the analytics dashboard (*Section below*)

---

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Set up environment variables**
   - Create an account on https://www.alphavantage.co/ to get your Alpha Vantage API key
   - After that go to server/dags/kafka_stream.py in this part below:
   ```
   # Define stock symbol
    symbols = ["NVDA", "IBM"]

    # Define interval for data extraction
    interval = "60min"

    # Define month for which data will be obtained
    months = ["2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03", "2025-04"]  

    # Define API key
    api_key = <your-api-key>
   ```
   - Replace the _<your-api-key>_ with your API key
   - In this part of the code you will define which stocks you want to get data, the interval and the months.

   ```
   Tips:
   - You can change the approach of the code to get enviroment variables dinamically from a .env file, or you can use variables from Airflow UI
   - Alternativally, you can define a DAG for each Stock, it would be better for monitoring
   ```

3. **Start the server**
   Go to the server folder and run:
   ```bash
   docker-compose up -d
   ```

4. **Wait for all services to start**
   The system includes the following services:
   - Kafka broker
   - Zookeeper
   - Cassandra
   - Airflow
   - Spark

5. **Go to Airflow UI and start the data pipeline**
   - Access the Airflow UI
   - Enable the `real-time-etl-stack` DAG
   - The DAG will automatically collect and process data

6. **Start the client, to move data from kafka to Cassandra using Spark Streaming**
   - Go to the client folder create the image
   ```bash
      docker build -t kafka-spark-cassandra-consumer .
   ```
   - Run the container
   ```bash
      docker run -d --name client --network server_mynetwork kafka-spark-cassandra-consumer
   ```
   - Inside the container, run the command below to start the Kafka Consumer:
   ```bash
      python consumer_stream.py --mode initial
   ```
   - Open the terminal or command prompt and use the commands below to access Cassandra and check the storage result:
   ```bash
      docker exec -it cassandra cqlsh
      USE financial_data;
      SELECT * FROM stock_[symbol] LIMIT 10; (*Replace [symbol] for the stock you want - like stock_IBM*)
   ```

7. **Start the app to visualize the analytics dashboard**
   - Go to the app folder create the image
   ```bash
      docker build -t streamlit-app .
   ```
   - Run the container
   ```bash
      docker run -d --name streamlit-app -p 8501:8501 --network server_mynetwork streamlit-app
   ```
   - Open the Streamlit web app on http://localhost:8501
   - Enter a stock symbol (e.g., IBM, NVDA)
   - View real-time analytics and charts

   ```
   ## Features

   - Real-time financial data collection
   - Technical analysis charts
   - Moving averages
   - Volume analysis
   - Candlestick charts
   - Historical data visualization
   ```
