<h1 align="center">
    Kafka and Spark Streaming for Financial Analysis
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

# Real-Time Financial Data Analytics Platform

This project implements a real-time financial data analytics platform using Apache Kafka, Apache Cassandra, Apache Spark, and Apache Airflow. The system collects financial data from Alpha Vantage API, processes it through Kafka and Spark Streaming, stores it in Cassandra, and provides real-time analytics through a Streamlit web application.

---

In this project, I develop a data lakehouse on the Snowflake and Databricks platforms, performing data transformations with DBT and using Airbyte for data loading.

The entire environment is managed with Docker, ensuring environment isolation and version control.

Airbyte is one of the most widely used open-source tools for data movement. In this project, the data is moved from a Postgres database to Snowflake or Databricks, but several data sources can be connected through the Airbyte UI.

Likewise, DBT is one of the most widely used open-source tools for data transformation. In this project, DBT is used to build the bronze, silver, and gold layers in Snowflake or Databricks.

With this approach, the benefits of the best open-source data tools are taken advantage of, as well as the benefits of the best data platforms.

In addition, this project addresses the main step in building a data lakehouse: data modeling. A fictitious company and a business problem to be solved are defined. From this business problem, data modeling is performed to solve the problem, where the conceptual, dimensional, logical and physical models are defined to build the data lakehouse and solve the proposed problem based on data.

If you want to understand the modeling part, go to the modeling folder, where the entire resolution of the business problem is developed.

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

## Architecture

The system consists of three main components:

1. **Data Producer (Airflow DAG)**
   - Collects financial data from Alpha Vantage API
   - Processes and formats the data
   - Sends data to Kafka topics

2. **Data Consumer (Spark)**
   - Consumes data from Kafka topics
   - Processes and transforms the data
   - Stores data in Cassandra

3. **Web Application (Streamlit)**
   - Provides real-time analytics dashboard
   - Visualizes financial data
   - Shows technical indicators and charts

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

## Credentials

### Airflow
- **username:** `admin`
- **password:** `admin`

---

## Setup Instructions
1. Clone the repository
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

   *Tips:*
   _- You can change the approach of the code to get enviroment variables dinamically from a .env file, or you can use variables from Airflow UI_
   _- Alternativally, you can define a DAG for each Stock, it would be better for monitoring_
   

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
