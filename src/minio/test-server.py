import os
import dotenv

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession, functions, types



def _set_spark_environment():
    """
    Sets the SPARK_HOME environment variable based on the installed
    PySpark version.
    """
    try:
        # Read the spark version is installed
        from pyspark import __version__ as spark_version

        # Set the SPARK_HOME based on the spark version
        os.environ['SPARK_HOME'] = 'c:/spark/spark-{}'.format(spark_version)
        os.environ['HADOOP_HOME'] = 'c:/spark/hadoop'

        # Set the hadoop aws package version based on spark version
        os.environ['HADOOP_AWS_VERSION'] = '3.4.1' if spark_version.startswith('4.0') else '3.3.6'

        # Log the settings
        print("Using spark from {};".format(os.environ['SPARK_HOME']))
        print("Using hadoop from {};".format(os.environ['HADOOP_HOME']))
        print("Using hadoop aws package {};".format(os.environ['HADOOP_AWS_VERSION']))

    except ImportError as e:
        raise ImportError("PySpark is not installed. Please install it to proceed.") from e
    

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
    # To prevent this, especially during development and testing, and avoid re-downloading
    # the JARs each time, we can use a workaround by manually moving the initially
    # downloaded JARs from the Spark temp directory into a permanent Spark installation
    # directory : spark-4.0.0\jars
    # Required JARs to move are,
    #   - org.apache.hadoop_hadoop-aws-3.4.1.jar
    #   - org.wildfly.openssl_wildfly-openssl-1.1.3.Final.jar
    #   - software.amazon.awssdk_bundle-2.24.6.jar
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
    # 1. Clean names by lowercasing and trimming all values
    @functions.udf(returnType=types.StringType())
    def lowercase_and_trim(value: str):
        return value.strip().lower()
    
    data = \
        data \
            .withColumn('First Name', lowercase_and_trim('First Name')) \
            .withColumn('Last Name', lowercase_and_trim('Last Name')) \
            .withColumn('Company', lowercase_and_trim('Company')) \
            .withColumn('Email', lowercase_and_trim('Email')) \
    
    # 2. Clean phone numbers by triming it with the xNNN.
    @functions.udf(returnType=types.StringType())
    def trim_xnnn(value: str):
        value = value.split('x')[0]
        value = value.lstrip('0')
        return value
    
    data = \
        data \
            .withColumn('Phone 1', trim_xnnn('Phone 1')) \
            .withColumn('Phone 2', trim_xnnn('Phone 2')) \

    # 3. Add a new column with the full name
    data = \
        data \
            .withColumn('Full Name', functions.concat_ws(' ', 'First Name', 'Last Name')) \

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