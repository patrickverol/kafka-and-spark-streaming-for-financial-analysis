# Special Data Consulting Module
# Practical Project for Data Consulting
# Real-Time Day Trade Analytics App Deployment

# Imports
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from cassandra.cluster import Cluster
import pandas as pd
from datetime import datetime, timedelta

########## Analytics ##########

# Function to connect to Cassandra
def connect_to_cassandra():
    try:
        cluster = Cluster(['cassandra'])
        session = cluster.connect('financial_data')
        return session
    except Exception as e:
        st.error(f"Error connecting to Cassandra: {str(e)}")
        return None

# Function to get available stocks
def get_available_stocks(session):
    try:
        # Query to get all tables in the keyspace
        query = """
            SELECT table_name 
            FROM system_schema.tables 
            WHERE keyspace_name = 'financial_data'
        """
        result = session.execute(query)
        # Extract stock symbols from table names that start with 'stock_' and convert to uppercase
        stocks = [row.table_name.replace('stock_', '').upper() for row in result if row.table_name.startswith('stock_')]
        return sorted(stocks)
    except Exception as e:
        st.error(f"Error getting available stocks: {str(e)}")
        return []

# Function to get stock data
def get_stock_data(session, symbol, start_date, end_date):
    try:
        # Convert symbol to lowercase for table name
        table_symbol = symbol.lower()
        query = f"""
            SELECT timestamp, open, high, low, close, volume, symbol, time_zone
            FROM financial_data.stock_{table_symbol}
            WHERE timestamp >= %s
            AND timestamp <= %s
            ALLOW FILTERING
        """
        result = session.execute(query, (start_date, end_date))
        df = pd.DataFrame(list(result))
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            # Convert symbol to uppercase in the dataframe
            df['symbol'] = df['symbol'].str.upper()
        return df
    except Exception as e:
        st.error(f"Error getting data for {symbol}: {str(e)}")
        return pd.DataFrame()

# Function to plot stock price
def plot_stock_price(df, symbol):
    fig = px.line(df, 
                  x="timestamp", 
                  y="close", 
                  title=f"{symbol} Stock Price", 
                  markers=True)
    st.plotly_chart(fig)

# Function to plot candlestick chart
def plot_candlestick(df, symbol):
    fig = go.Figure(data=[go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    
    fig.update_layout(
        title=f"{symbol} Candlestick Chart",
        yaxis_title="Price",
        xaxis_title="Date",
        template="plotly_dark"
    )
    
    st.plotly_chart(fig)

# Function to plot moving averages
def plot_moving_averages(df, symbol):
    # Calculate moving averages
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()
    
    fig = px.line(df, 
                  x='timestamp', 
                  y=['close', 'SMA_20', 'EMA_20'],
                  title=f"{symbol} Moving Averages",
                  labels={'value': 'Price (USD)', 'timestamp': 'Date'})
    
    st.plotly_chart(fig)

# Function to plot volume
def plot_volume(df, symbol):
    fig = px.bar(df, 
                 x='timestamp', 
                 y='volume', 
                 title=f"{symbol} Trading Volume")
    
    st.plotly_chart(fig)

# Function to get date range from database
def get_date_range(session, symbol):
    try:
        query = f"""
            SELECT MIN(timestamp) as min_date, MAX(timestamp) as max_date
            FROM financial_data.stock_{symbol}
        """
        result = session.execute(query)
        row = result.one()
        if row and row.min_date and row.max_date:
            # Convert string timestamps to datetime objects
            min_date = pd.to_datetime(row.min_date)
            max_date = pd.to_datetime(row.max_date)
            return min_date, max_date
        return None, None
    except Exception as e:
        st.error(f"Error getting date range: {str(e)}")
        return None, None

########## App Web ##########

# Configure Streamlit page
st.set_page_config(page_title="Real-Time Stock Analytics", page_icon="📈", layout="wide")

# Sidebar with instructions
st.sidebar.title("Instructions")
st.sidebar.markdown("""
### How to Use the App:

- Select a stock from the dropdown menu.
- Choose your desired date range.
- View real-time analytics and visualizations.

### Available Stocks:
- IBM
- NVDA

### Purpose:
This application provides real-time stock analytics with advanced visualizations and technical indicators to support your trading decisions.
""")

# Support button in sidebar
if st.sidebar.button("Support"):
    st.sidebar.write("For any questions, please contact: patrickverol@gmail.com")

# Main title
st.title("📈 Real-Time Stock Analytics Dashboard")

# Connect to Cassandra
session = connect_to_cassandra()
if not session:
    st.error("Failed to connect to database")
    st.stop()

# Get available stocks
available_stocks = get_available_stocks(session)
if not available_stocks:
    st.error("No stocks available")
    st.stop()

# Stock selection
selected_stock = st.selectbox("Select Stock", available_stocks)

# Get date range from database
min_date, max_date = get_date_range(session, selected_stock.lower())  # Convert to lowercase for table name
if min_date and max_date:
    default_start = min_date.date()
    default_end = max_date.date()
else:
    default_start = datetime.now() - timedelta(days=7)
    default_end = datetime.now()

# Date range selection
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(
        "Start Date",
        default_start,
        min_value=min_date.date() if min_date else None,
        max_value=max_date.date() if max_date else None
    )
with col2:
    end_date = st.date_input(
        "End Date",
        default_end,
        min_value=min_date.date() if min_date else None,
        max_value=max_date.date() if max_date else None
    )

# Convert dates to strings
start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

# Get stock data
df = get_stock_data(session, selected_stock, start_date_str, end_date_str)

if not df.empty:
    # Display stock information
    st.subheader(f"Stock Information for {selected_stock}")
    
    # Create metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Price", f"${df['close'].iloc[-1]:.2f}")
    with col2:
        st.metric("Daily Change", f"${df['close'].iloc[-1] - df['open'].iloc[-1]:.2f}")
    with col3:
        st.metric("High", f"${df['high'].max():.2f}")
    with col4:
        st.metric("Low", f"${df['low'].min():.2f}")
    
    # Create visualizations
    st.subheader("Data Visualization")
    plot_stock_price(df, selected_stock)
    plot_candlestick(df, selected_stock)
    plot_moving_averages(df, selected_stock)
    plot_volume(df, selected_stock)
    
    # Display raw data
    st.subheader("Raw Data")
    st.dataframe(df)
else:
    st.warning(f"No data available for {selected_stock} in the selected date range")




