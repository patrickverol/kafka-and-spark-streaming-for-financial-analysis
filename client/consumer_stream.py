# Import logging module for log registration
import logging

# Import argparse module for command line argument handling
import argparse

# Import Cluster class from Cassandra to create database connections
from cassandra.cluster import Cluster

# Import SparkSession to create Spark sessions
from pyspark.sql import SparkSession

# Import PySpark functions for data manipulation
from pyspark.sql.functions import from_json, col

# Import structured data types from PySpark
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Configure logger to display INFO level messages
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Function to create a keyspace in Cassandra
def create_keyspace(session):
    # Execute statement from the received session
    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS financial_data
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
        """
    )
    print("Keyspace created successfully!")

# Function to create a table in Cassandra for a specific stock
def create_stock_table(session, symbol):
    # Execute statement from the received session
    session.execute(
        f"""
        CREATE TABLE IF NOT EXISTS financial_data.stock_{symbol} (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            symbol TEXT,
            time_zone TEXT,
            open DOUBLE,
            high DOUBLE,
            low DOUBLE,
            close DOUBLE,
            volume DOUBLE
        );
        """
    )
    print(f"Table for {symbol} created successfully!")

# Function to insert formatted data into Cassandra
def insert_data(session, row):
    try:
        # Convert string values to float, maintaining decimal precision
        open_val = float(row.open) if row.open else 0.0
        high_val = float(row.high) if row.high else 0.0
        low_val = float(row.low) if row.low else 0.0
        close_val = float(row.close) if row.close else 0.0
        volume_val = float(row.volume) if row.volume else 0.0

        # Create the query for the specific stock table
        query = f"""
            INSERT INTO financial_data.stock_{row.symbol}(
                id, timestamp, symbol, time_zone, open, high, low, close, volume
            ) VALUES (
                '{row.id}', '{row.timestamp}', '{row.symbol}', '{row.time_zone}', 
                {open_val}, {high_val}, {low_val}, {close_val}, {volume_val}
            )
        """
        
        # Insert formatted data into Cassandra table
        session.execute(query)
        logging.info(f"Log - Data inserted for record: {row.id} - {row.symbol} - {row.timestamp}")
    except Exception as e:
        # Display error if data insertion fails
        logging.error(f"Log - Data cannot be inserted due to error: {e}")
        print(f"Log - This is the query:\n{query}")

# Function to create a Spark connection
def create_spark_connection():
    try:
        # Configure and create Spark connection
        s_conn = (
            SparkSession.builder.appName("Project")
            .master("spark://spark-master:7077")
            .config(
                "spark.jars.packages",
                "com.datastax.spark:spark-cassandra-connector_2.12:3.4.1,"
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1",
            )
            .config("spark.cassandra.connection.host", "cassandra")
            .config("spark.cassandra.connection.port", "9042")
            .config("spark.executor.memory", "1g")
            .config("spark.executor.cores", "1")
            .config("spark.cores.max", "2")
            .getOrCreate()
        )

        # Set log level
        s_conn.sparkContext.setLogLevel("ERROR")
        logging.info("Log - Spark Connection created successfully!")
        return s_conn
    except Exception as e:
        logging.error(f"Log - Could not create Spark Connection due to error: {e}")
        return None

# Function to create a Kafka connection in Spark for multiple topics
def create_kafka_connection(spark_conn, stream_mode, topics):
    try:
        # Configure and create a Spark DataFrame for reading Kafka data
        spark_df = (
            spark_conn.readStream.format("kafka")
            .option("kafka.bootstrap.servers", "broker:29092")
            .option("subscribe", ",".join(topics))  # Subscribe to multiple topics
            .option("startingOffsets", stream_mode)
            .load()
        )
        logging.info("Log - Kafka DataFrame created successfully")
        return spark_df
    except Exception as e:
        # Display warning if Kafka DataFrame creation fails
        logging.warning(f"Log - Kafka DataFrame could not be created due to error: {e}")
        return None

# Function to create a structured DataFrame from Kafka data
def create_df_from_kafka(spark_df):
    # Define schema for data received in JSON format
    schema = StructType([
        StructField("id", StringType(), False),
        StructField("timestamp", StringType(), False),
        StructField("symbol", StringType(), False),
        StructField("time_zone", StringType(), False),
        StructField("open", StringType(), False),
        StructField("high", StringType(), False),
        StructField("low", StringType(), False),
        StructField("close", StringType(), False),
        StructField("volume", StringType(), False)
    ])

    # Process Kafka data to extract records
    return (
        spark_df.selectExpr("CAST(value AS STRING)")            # Convert data to string
        .select(from_json(col("value"), schema).alias("data"))  # Convert JSON to structured columns
        .select("data.*")                                       # Extract all columns from "data" field
    )

# Function to create a Cassandra connection
def create_cassandra_connection():
    try:
        # Create a cluster and return Cassandra connection session
        cluster = Cluster(["cassandra"])
        return cluster.connect()
    except Exception as e:
        # Display error if Cassandra connection fails
        logging.error(f"Log - Could not create Cassandra connection due to error: {e}")
        return None

# Main program entry point
if __name__ == "__main__":
    
    # Configure parser for command line arguments
    parser = argparse.ArgumentParser(description = "Real Time ETL.")
    
    # Add argument for data consumption mode
    parser.add_argument(
        "--mode",
        required=True,
        help="Data consumption mode",
        choices=["initial", "append"],
        default="append",
    )

    # Parse provided arguments
    args = parser.parse_args()

    # Define consumption mode based on provided argument
    stream_mode = "earliest" if args.mode == "initial" else "latest"

    # Define the list of stock symbols to monitor
    stock_symbols = ["IBM", "NVDA"]  # Add more symbols as needed
    topics = [f"{symbol}_topic" for symbol in stock_symbols]

    # Create connections to Cassandra and Spark
    session = create_cassandra_connection()
    spark_conn = create_spark_connection()

    # If session is created
    if session and spark_conn:
        # Create keyspace in Cassandra
        create_keyspace(session)
        
        # Create tables for each stock
        for symbol in stock_symbols:
            create_stock_table(session, symbol)

        # Create Kafka connection and get DataFrame
        kafka_df = create_kafka_connection(spark_conn, stream_mode, topics)

        if kafka_df:

            # Create structured DataFrame from Kafka data
            structured_df = create_df_from_kafka(kafka_df)

            # Function to process data batches
            def process_batch(batch_df, batch_id):
                # Log the number of records in this batch
                count = batch_df.count()
                logging.info(f"Processing batch {batch_id} with {count} records")
                
                if count > 0:
                    # Log the first record in the batch
                    first_row = batch_df.first()
                    logging.info(f"First record in batch: {first_row}")
                
                # Iterate over batch rows and insert data into Cassandra
                for row in batch_df.collect():
                    insert_data(session, row)
                    logging.info(f"Log - Processing batch {batch_id} for record: {row.id}")

            # Configure continuous processing of structured DataFrame
            query = (
                structured_df.writeStream
                .foreachBatch(process_batch)  # Define batch processing
                .outputMode("append")         # Set output mode
                .trigger(processingTime="5 seconds")  # Process every 5 seconds
                .option("checkpointLocation", "/tmp/checkpoint")  # Add checkpoint location
                .start()                      # Start processing
            )
        
            # Wait for stream completion with proper error handling
            try:
                logging.info("Starting stream processing...")
                logging.info(f"Subscribed to topics: {topics}")
                logging.info(f"Stream mode: {stream_mode}")
                query.awaitTermination()
            except Exception as e:
                logging.error(f"Stream processing failed: {e}")
                query.stop()
                raise


