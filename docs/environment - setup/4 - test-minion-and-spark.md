### Configure PySpark to use the created buckets

See the script `src.test_minio_server.py`.

```py
import os

from pyspark.sql import SparkSession
from dotenv import load_dotenv


def test_etl_with_minio():
    """
    Test ETL process using MinIO as S3-compatible storage.

    - Sets up a Spark session configured to connect to a local MinIO server.
    - Reads sample customer data from a MinIO bucket.
    - Writes the processed data back to another MinIO bucket in parquet format.
    """

    # Import environment variables from the .env file
    load_dotenv("./minio/.env")
    miniono_access_key = os.getenv('MINIO_ROOT_USER')
    miniono_secret_key = os.getenv('MINIO_ROOT_PASSWORD')
    hadoop_aws_version = os.getenv('HADOOP_AWS_VERSION')

    # Initialize Spark session's builder
    spark_builder = SparkSession.builder.appName("etl-with-minio")

    # Use a custom local directory for Spark temporary files instead of the default
    # AppData\Local\Temp location used on Windows.
    spark_builder.config('spark.local.dir', '.temp/spark')
    spark_builder.config('spark.sql.crossJoin.enabled', 'true')

    # Add the Hadoop AWS package to enable S3A support, required for interacting
    # with MinIO through the s3a:// protocol.
    spark_builder.config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:{}".format(hadoop_aws_version))

    # Configure to connect to MinIO server using the S3A protocol
    spark_builder.config("spark.hadoop.fs.s3a.access.key", miniono_access_key)
    spark_builder.config("spark.hadoop.fs.s3a.secret.key", miniono_secret_key)
    spark_builder.config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000")
    spark_builder.config("spark.hadoop.fs.s3a.path.style.access", "true")

    # Create Spark session
    with spark_builder.getOrCreate() as spark:
    
        # Read customers sample data from the raw-data bucket
        data = spark.read.csv("s3a://raw-data/customers.csv", header=True, inferSchema=True)
        data.show(5)

        # Write the processed data to the processed-data bucket in parquet format
        data.write.parquet("s3a://processed-data/customers.parquet", mode="overwrite")

# Run the ETL test with MinIO
test_etl_with_minio()
```