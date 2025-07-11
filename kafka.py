from pyspark.sql import SparkSession


# Obtener variables del entorno con valores por defecto
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "test:443")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "test")
KAFKA_TRUSTSTORE_LOCATION = os.getenv("KAFKA_TRUSTSTORE_LOCATION", "/Users/davidfonseca/Desktop/telefonica/kafka/client.truststore.jks")
KAFKA_TRUSTSTORE_PASSWORD = os.getenv("KAFKA_TRUSTSTORE_PASSWORD", "123456789")

# Crear Spark Session
spark = SparkSession.builder \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.apache.kafka:kafka-clients:2.8.0") \
    .appName("KafkaSSLConsumer") \
    .getOrCreate()

# Leer desde Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("kafka.security.protocol", "SSL") \
    .option("kafka.ssl.truststore.location", KAFKA_TRUSTSTORE_LOCATION) \
    .option("kafka.ssl.truststore.password", KAFKA_TRUSTSTORE_PASSWORD) \
    .load()

# Convert binary values to string
df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Print messages to console
query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()