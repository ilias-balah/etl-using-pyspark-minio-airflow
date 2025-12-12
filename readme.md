## Project Description

In this project, we demonstrate the design and implementation of a **production grade ETL pipeline** using modern data engineering tools.

The goal of this demonstration, is to showcase the ability to design and implement a robust, scalable, and maintainable **ETL pipeline** that can handle large-scale data processing tasks, including :
- Reading raw data from various sources, including a local S3-like storage, to simulate **AWS S3** cloud storage;
- Cleaning and transforming the data using **PySpark**;
- Scheduling and orchestrating the data processing jobs with **Apache Airflow**;
- Writing the processed data into **Parquet** format for efficient querying;
- Demonstrating data lineage and monitoring.
- Setting up notifications for job success or failure using Slack or email.


## Tech Stack & Tools

| Component              | Tool / Library        | Purpose                                                    |
| ---------------------- | --------------------- | ---------------------------------------------------------- |
| Data Processing        | PySpark               | Large-scale data transformations, aggregations, cleaning   |
| Storage                | MinIO                 | Simulate cloud storage for raw and processed data          |
| Workflow Orchestration | Apache Airflow        | DAG scheduling, dependency management, pipeline monitoring |
| File Format            | Parquet               | Efficient columnar storage for processed data              |
| Notifications          | Slack / Email         | Alerts for job success or failure                          |
| Environment            | Python 3.11.9, Docker | Local development and containerized services               |