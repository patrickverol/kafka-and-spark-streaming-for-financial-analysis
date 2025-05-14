# Import date and time related classes
from datetime import datetime, timedelta

# Import main Airflow classes for creating DAGs
from airflow import DAG

# Import Python operator from Airflow for executing Python functions as tasks
from airflow.operators.python import PythonOperator

# Import hashlib module for creating deterministic hash
import hashlib

# Import logging module for message logging
import logging

# Import time module for managing time intervals
import time

# Define default DAG arguments, including owner and start date
default_args = {"owner": "Patrick Verol"}

# Define function to get data from API
def extract_api_data(symbol: str, month: str, api_key: str, interval: str) -> dict:

    # Import requests module for making HTTP requests
    import requests

    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&month={month}&outputsize=full&apikey={api_key}'

    # Make a GET request to get data from a random users API
    res = requests.get(url)

    # Convert response to JSON
    res = res.json()

    # Return obtained data
    return res

# Define function to format data obtained from API
def format_data(timestamp, values, meta_data):

    # Create empty dictionary to store formatted data
    data = {}

    # Create unique ID based on symbol and timestamp
    unique_string = f"{meta_data['2. Symbol']}_{timestamp}"
    # Generate MD5 hash of combined string
    hash_object = hashlib.md5(unique_string.encode())
    # Convert hash to hexadecimal
    data["id"] = hash_object.hexdigest()

    # Extract and store timestamp
    data["timestamp"] = timestamp

    # Extract and store values directly
    data["open"] = values["1. open"]
    data["high"] = values["2. high"]
    data["low"] = values["3. low"]
    data["close"] = values["4. close"]
    data["volume"] = values["5. volume"]

    # Add Symbol and Time Zone from Meta Data
    data["symbol"] = meta_data["2. Symbol"]
    data["time_zone"] = meta_data["6. Time Zone"]

    # Return formatted data
    return data

# Define function to create Kafka connection
def create_kafka_connection():

    # Import Kafka producer
    from kafka import KafkaProducer

    try:

        # Create connection with Kafka broker
        producer = KafkaProducer(bootstrap_servers = ["broker:29092"], max_block_ms = 5000)

        # Wait 5 seconds before starting streaming
        time.sleep(5)

        # Log successful connection with Kafka broker
        logging.info("Log - Kafka Producer connected successfully.")

        return producer

    except Exception as e:

        # Log any error when trying to connect to Kafka broker
        logging.error(f"Log - Failed to connect to Kafka broker: {e}")
        return

def stream_data():

    # Import json module for handling JSON data
    import json

    producer = create_kafka_connection()

    # Define stock symbol
    symbols = ["NVDA", "IBM"]

    # Define interval for data extraction
    interval = "60min"

    # Define month for which data will be obtained
    months = ["2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03", "2025-04"]  

    # Define API key
    api_key = "YOUR_API_KEY"
    
    try:

        for symbol in symbols:

            for month in months:

                data = extract_api_data(symbol, month, api_key, interval)

                if data:
                    logging.info("Log - Data read successfully")    
                    time.sleep(2)

                # Get time series and meta data
                time_series = data.get(f"Time Series ({interval})")
                meta_data = data.get("Meta Data")
            
                if time_series is None:
                    logging.error(f"Error: Time series not found in JSON file for {symbol} in {month}")
                    return
                    
                if meta_data is None:
                    logging.error(f"Error: Meta Data not found in JSON file for {symbol} in {month}")
                    return
                
                logging.info(f"Log - Processing {len(time_series)} records from {symbol} in {month}")
                
                # Iterate over each time series item
                for timestamp, values in time_series.items():
                    try:
                        # Format data including meta data
                        res = format_data(timestamp, values, meta_data)

                        # Send data to Kafka topic
                        producer.send(f"{symbol}_topic", json.dumps(res).encode("utf-8"))
                        logging.info(f"Log - Data sent to Kafka: {timestamp} from {symbol} in {month}")
                    except Exception as e:
                        # Log any error during data streaming
                        logging.error(f"Log - Error processing data for timestamp {timestamp} from {symbol} in {month}: {e}")
                        continue

                logging.info(f"Log - Processing completed for month {month} of {symbol}")

    except Exception as e:
        logging.error(f"Log - Error processing data: {e}")
        return

    finally:
        # Close Kafka producer
        producer.close()
        logging.info("Log - Kafka Producer closed")

# Define Airflow DAG
with DAG("real-time-etl-stack",
         # Define default DAG arguments
         default_args=default_args,
         # Define DAG schedule as once per day
         schedule=timedelta(days=1),
         # Prevent retroactive DAG execution
         catchup=False,
         # Define DAG start date
         start_date=datetime(2024, 1, 1),
) as dag:
    # Define task that streams data
    streaming_task = PythonOperator(task_id="stream_from_api", 
                                    python_callable=stream_data)




