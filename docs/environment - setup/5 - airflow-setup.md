## 4. Setup Apache Airflow

- Create project folder

```ps
$ mkdir airflow
```

- Create `airflow/docker-compose.yaml` and copy the content from the the official dockerfile of airflow : https://airflow.apache.org/docs/apache-airflow/3.0.1/docker-compose.yaml.

- Initialize Airflow database

```ps
$ docker compose -f ./airflow/docker-compose.yaml up airflow-init
```

- Start Airflow

```ps
$ docker compose -f ./airflow/docker-compose.yaml up -d
```

### Access Airflow UI

* URL: `http://localhost:8080`
* Username: `airflow-username`
* Password: `********`