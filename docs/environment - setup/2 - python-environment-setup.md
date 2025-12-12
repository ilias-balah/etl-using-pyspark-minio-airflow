## 2. Python Environment Setup

### Create a virtual environment

```ps
$ python -m venv venv/py-3.11.9-with-spark-4.0.0
$ venv\Scripts\activate
```

### Install Python dependencies

```ps
$ pip install pyspark==4.0.0 pandas boto3 requests dotenv
```