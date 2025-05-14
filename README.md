<h1 align="center">
    Kafka and Spark Streaming for Financial Analysis
</h1>

<br>
    <div align="center">
        <a><img src="https://github.com/user-attachments/assets/46a5f8b1-f047-4c6b-b8da-e3cc9a57bb7e"></a> 
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

In this project, I develop a data lakehouse on the Snowflake and Databricks platforms, performing data transformations with DBT and using Airbyte for data loading.

The entire environment is managed with Docker, ensuring environment isolation and version control.

Airbyte is one of the most widely used open-source tools for data movement. In this project, the data is moved from a Postgres database to Snowflake or Databricks, but several data sources can be connected through the Airbyte UI.

Likewise, DBT is one of the most widely used open-source tools for data transformation. In this project, DBT is used to build the bronze, silver, and gold layers in Snowflake or Databricks.

With this approach, the benefits of the best open-source data tools are taken advantage of, as well as the benefits of the best data platforms.

In addition, this project addresses the main step in building a data lakehouse: data modeling. A fictitious company and a business problem to be solved are defined. From this business problem, data modeling is performed to solve the problem, where the conceptual, dimensional, logical and physical models are defined to build the data lakehouse and solve the proposed problem based on data.

If you want to understand the modeling part, go to the modeling folder, where the entire resolution of the business problem is developed.

## Databricks Lakehouse Schema

<br>
    <div align="center">
        <a><img src="https://github.com/user-attachments/assets/535e22a6-21b6-4cab-a7c7-95d3b369e2ed"></a> 
    </div>
</br>

## Databricks Lineage

<br>
    <div align="center">
        <a><img src="https://github.com/user-attachments/assets/94ac959d-fa2f-4f39-906e-48c335616ad8"></a> 
    </div>
</br>

## Snowflake Lakehouse Schema

<br>
    <div align="center">
        <a><img src="https://github.com/user-attachments/assets/5fd109e1-974e-4df0-97f5-69e7c34e19a0"></a> 
    </div>
</br>

## Snowflake Lineage

<br>
    <div align="center">
        <a><img src="https://github.com/user-attachments/assets/5077fe58-bd4f-4c81-b469-4c8b7aee6a29"></a> 
    </div>
</br>

---

## Installation and configuration

- **Airbyte:** data extraction - http://localhost:56174/
- **Dbt:** data transformation
- **Airflow:** task orchestration - http://localhost:8085/
- **PostgreSQL:** data storage - http://localhost:5780/

--- 

## Requirements
- Docker Desktop
- Python 3.6 or higher
- Recommended 8GB RAM or higher only for docker containers.

---

## Credentials

### Airflow
- **username:** `airflow`
- **password:** `airflow`

### Postgres
- **Name:** `db_source`
- **Host name/adress:** `localhost`
- **Port:** `5780`
- **Maintenance database:** `dbSource`
- **Username:** `useradmin`
- **password:** `password`
*Credentials to connect using pgAdmin*

### Airbyte
Enter a valid email when trying to log in.
- For other configurations:
 - **internal_host:** `host.docker.internal`
 - **internal_host_and_port:** `http://host.docker.internal:8000`
 - **user:** `airbyte`
 - **password:** `password`

---

## Setup Instructions
1. Open your terminal.
2. Navigate to the root of the `data-stack` repository
3. Run `docker compose up --build` to initialize the containers. If you want to run it in the background, add `-d` argument.
4. Make shure you have the accounts created in Databricks or Snowflake (you will need the tokens, account and password to configure Airbyte and Airflow).
5. Perform Airflow configurations (*Section below*)
6. Go to Airflow UI and run the 3 firsts DAGs to populate the data source in Postgres.
5. Perform Airbyte configurations (*Section below*)
6. Go to the airflow-worker container terminal and inicialize the dbt project (*Section below*)
8. Run all the Airflow DAGs exactly in the configured order.
9. Go to Snowflake or Databricks and see the schemas created.
































# Real-Time Financial Data Analytics Platform

This project implements a real-time financial data analytics platform using Apache Kafka, Apache Cassandra, Apache Spark, and Apache Airflow. The system collects financial data from Alpha Vantage API, processes it through Kafka and Spark Streaming, stores it in Cassandra, and provides real-time analytics through a Streamlit web application.

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

## Prerequisites

- Docker
- Docker Compose
- Python 3.9+
- Alpha Vantage API key

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Set up environment variables**
   Create a `.env` file in the root directory with your Alpha Vantage API key:
   ```
   ALPHA_VANTAGE_API_KEY=your_api_key_here
   ```

3. **Build and start the containers**
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
   - Streamlit web app

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

## Running the Application

1. **Start the data pipeline**
   - Access the Airflow UI
   - Enable the `real-time-etl-stack` DAG
   - The DAG will automatically collect and process data

2. **Start the client, to move data from kafka to Cassandra using Spark Streaming**
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

3. **View the analytics dashboard**
   - Open the Streamlit web app on http://localhost:8501
   - Enter a stock symbol (e.g., IBM, NVDA)
   - View real-time analytics and charts

## Features

- Real-time financial data collection
- Technical analysis charts
- Moving averages
- Volume analysis
- Candlestick charts
- Historical data visualization

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
