### Configure PySpark to use the created buckets

See the script `src/minio/test-server.py`.

```py

import os
import dotenv

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession, functions, types



def _set_spark_environment():
    """
    Sets the SPARK_HOME environment variable based on the installed
    PySpark version.
    """
    # Environment variable to specify the Spark home directory
    # This is necessary for PySpark to find the required JAR files
    ...
    

def _create_spark_session():
    """
    Create a Spark session configured to connect to a local MinIO server.

    - Sets up the Spark session with necessary configurations for S3A access.
    - Reads sample customer data from a MinIO bucket.
    - Writes the processed data back to another MinIO bucket in parquet format.
    """
    # Import environment variables from the .env file
    dotenv.load_dotenv("./minio/.env")
    miniono_access_key = os.getenv('MINIO_ROOT_USER')
    miniono_secret_key = os.getenv('MINIO_ROOT_PASSWORD')
    hadoop_aws_version = os.getenv('HADOOP_AWS_VERSION')

    # Initialize Spark session's builder
    spark_builder = SparkSession.builder.appName("test-minio-s3a")

    # Use a custom local directory for Spark temporary files instead of the default
    # AppData\Local\Temp location used on Windows.
    spark_builder.config('spark.local.dir', '.temp/spark')
    spark_builder.config('spark.sql.crossJoin.enabled', 'true')

    # Add the Hadoop AWS package to enable S3A support, required for interacting
    # with MinIO through the s3a:// protocol.
    required_packages = [
        # NOTE: Needs to be commented if using the manual JAR copy workaround below.
        "org.apache.hadoop:hadoop-aws:{}".format(hadoop_aws_version),
    ]

    # NOTE: Spark downloads these JARs at runtime and stores them in its temp directory.
    # On Windows, Spark may fail to delete these cached JARs during shutdown due to
    # file locks held by the JVM. This can produce "Failed to delete" warnings.
    if required_packages:
        spark_builder.config("spark.jars.packages", ",".join(required_packages))

    # Configure to connect to MinIO server using the S3A protocol
    spark_builder.config("spark.hadoop.fs.s3a.access.key", miniono_access_key)
    spark_builder.config("spark.hadoop.fs.s3a.secret.key", miniono_secret_key)
    spark_builder.config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000")
    spark_builder.config("spark.hadoop.fs.s3a.path.style.access", "true")
    
    # Create and return the Spark session
    return spark_builder.getOrCreate()


def transform_data(data: DataFrame) -> DataFrame:
    """
    Dummy transformation function to simulate data processing for 
    the customer data before writing it back to MinIO.
    """
    # Transformation logic added here ...
    return data


def main():
    """
    Run a small test of an ETL process using MinIO as S3-compatible storage.

    - Sets up a Spark session configured to connect to a local MinIO server.
    - Reads sample customer data from a MinIO bucket.
    - Writes the processed data back to another MinIO bucket in parquet format.
    """
    # Create Spark session
    with _create_spark_session() as spark:
    
        # Read customers sample data from the raw-data bucket
        data = spark.read.csv("s3a://raw-data/customers.csv", header=True, inferSchema=True)

        # Transform the data into a new cleaned DataFrame
        data = transform_data(data)

        # Write the processed data to the processed-data bucket in parquet format
        data.write.parquet("s3a://processed-data/customers.parquet", mode="overwrite", partitionBy='Country')



if __name__ == "__main__":

    # Ensure the right Spark version is set in the environment
    _set_spark_environment()

    # Run the ETL test with MinIO
    main()

```