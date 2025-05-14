# Data Science Academy

# Imagem base
FROM python:3.11-slim

# Instala dependências do sistema 
RUN apt-get update && apt-get install -y \
    openjdk-17-jre \
    curl \
    wget \
    && apt-get clean

# Instala dependências Python
RUN pip install pyspark==3.5.4 kafka-python==2.0.2 cassandra-driver==3.29.2

# Set Spark environment variables
ENV SPARK_HOME=/usr/local/lib/python3.11/site-packages/pyspark
ENV PATH=$PATH:$SPARK_HOME/bin
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages/pyspark/python

# Copia o script para o container
COPY consumer_stream.py /app/consumer_stream.py

# Configura diretório de trabalho
WORKDIR /app

# Keep container running by default
CMD ["tail", "-f", "/dev/null"]

# Uncomment to run the consumer
#CMD ["python", "consumer_stream.py", "--mode", "append"]