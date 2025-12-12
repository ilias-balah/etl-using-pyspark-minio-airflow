## 3. Setup `MinIO` for Local Object Storage

In this project, we need a reliable, scalable, and S3-compatible object storage solution for managing large datasets and handling file storage locally during development and testing. For that, we can use MinIO, a high-performance, open-source object storage server that is fully compatible with the Amazon S3 API.

The main reasons for choosing MinIO are:

- S3 Compatibility: MinIO allows us to use the same APIs and SDKs as AWS S3, making it easier to switch to cloud storage in the future without changing application code.

- Local Development: Running MinIO locally provides a lightweight storage environment, enabling developers to test file operations without relying on an internet connection or incurring cloud costs.

- High Performance and Scalability: MinIO is optimized for fast read/write operations and can handle large-scale data workloads efficiently, even in a local setup.

- Ease of Deployment: It can be deployed quickly using Docker or directly as a standalone binary, simplifying setup and reducing operational overhead.

- Open Source and Cost-Effective: MinIO is fully open-source, allowing full control over data without subscription costs, ideal for local development and experimentation.

Overall, `MinIO` provides a simple yet powerful solution for local object storage that mirrors cloud S3 functionality, ensuring that our development and testing environment closely resembles production workflows.

### Run `MinIO` using Docker

- Create a folder naed `minio`.
- Create an environment file `minio/.env` with the root user and password.
```
MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=*******
```

- Create the docker compose file `minio/docker-compose.yaml`.

```yaml
version: '3.8'

services:
  minio:
    image: minio/minio
    container_name: minio
    ports:
      - "9000:9000"
      - "9001:9001"
    env_file:
      - ./.env
    volumes:
      - ./data:/data
    command: server /data --console-address ":9001"
```

- Start `MinIO` server

```ps
$ docker compose -f ./minio/docker-compose.yaml up -d
```

- Access `MinIO` Console

  * URL: `http://127.0.0.1:9001`
  * Username: `minio-username`
  * Password: `*******`

### Create Buckets

* `raw-data`
* `processed-data`