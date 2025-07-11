from pyspark.sql import SparkSession

# Spark Session
spark = SparkSession.builder \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.apache.kafka:kafka-clients:2.8.0") \
    .appName("KafkaSSLConsumer") \
    .getOrCreate()


# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-cluster-kafka-external-bootstrap-prod-broker.apps.epico-seed-col-1.tmve.local:443") \
    .option("subscribe", "test") \
    .option("kafka.security.protocol", "SSL") \
    .option("kafka.ssl.truststore.location", "/Users/davidfonseca/Desktop/telefonica/kafka/client.truststore.jks") \
    .option("kafka.ssl.truststore.password", "123456789") \
    .load()

# Convert binary values to string
df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Print messages to console
query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()