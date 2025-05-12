# Social Media Sentiment Pipeline

This repository contains a production-ready Docker Compose setup for a scalable, secure social media sentiment analysis pipeline. The stack includes Zookeeper, Kafka, MinIO, Spark (Master & Worker), a Spark Streaming job, a FastAPI-based ML prediction service, and monitoring components (Prometheus & Grafana) behind a centralized Nginx HTTPS reverse proxy.

---

## Table of Contents

* [Architecture](#architecture)
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Getting Started](#getting-started)
* [Environment Variables](#environment-variables)
* [Docker Compose Services](#docker-compose-services)
* [Security Considerations](#security-considerations)
* [Monitoring & Logging](#monitoring--logging)
* [License](#license)

---

## Architecture

```text
             +---------------------+       +------------------+
             |   Zookeeper (2181)  | <---> |    Kafka Broker   |
             +---------------------+       +------------------+
                       ^                         ^
                       |                         |
         +-------------+-------------+           |
         | Producer: Social Media    |           |
         |  (Fetch & Publish Posts)  |           |
         +---------------------------+           |
                                               |
                +----------------------+        |
                | Spark Streaming Job  | -------+
                |  (Consume & Process) |        |
                +----------------------+        |
                         |                       |
                         v                       v
                +----------------------+   +--------------------+
                |     MinIO (S3)       |   |  Delta Lake Tables |
                +----------------------+   +--------------------+

  +---------------------------------------------------------------+
  |                       FastAPI ML API                         |
  |             (Expose sentiment predictions)                   |
  +---------------------------------------------------------------+
                         ^                       ^
                         |                       |
              +----------+------+      +---------+-----------+
              |     Users/Apps   |      |  Grafana Dashboard  |
              +------------------+      +---------------------+
                                               ^
                                               |
                                        +------+-------+
                                        | Prometheus    |
                                        +--------------+
                                        | Nginx Proxy   |
                                        +--------------+

```

## Features

* **Kafka with SASL\_SSL**: Secure, authenticated message streaming.
* **MinIO over HTTPS**: Encrypted object storage for intermediate data and Delta Lake.
* **Spark with SSL**: Secure cluster communication and encrypted storage.
* **Spark Streaming**: Real-time ingestion & processing of social media posts.
* **FastAPI ML Service**: Scalable sentiment prediction API behind Nginx.
* **Prometheus & Grafana**: Centralized metrics collection & visualization.
* **Nginx Reverse Proxy**: Centralized TLS termination for all HTTP services.

## Prerequisites

* Docker Engine >= 20.10
* Docker Compose CLI >= 1.29
* A certificate authority or self-signed certificates for TLS (zookeeper, Kafka, Spark, MinIO, Nginx).
* A secrets management solution (e.g., HashiCorp Vault, AWS Secrets Manager) to inject real credentials at runtime.

## Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/SalimYs/Social-Media-Sentiment-Pipeline.git
   cd social-media-sentiment-pipeline
   ```

2. **Copy the example `.env` and configure secrets**

   ```bash
   cp .env.example .env
   # Update placeholders or configure your CI/CD to inject real values
   ```

3. **Ensure your certificates and secrets are mounted**

   * Place JKS keystores/truststores under `./secrets/kafka/` and `./secrets/zookeeper/`.
   * Place TLS cert/key pairs under `./certs/minio/` and `./certs/nginx/`.

4. **Start the stack**

   ```bash
   docker-compose up -d
   ```

5. **Access the services**

   * **API**: `https://<proxy-domain>/api`
   * **Grafana**: `https://<proxy-domain>/grafana`
   * **Prometheus**: `https://<proxy-domain>/prometheus`
   * **MinIO**: `https://<proxy-domain>/minio`

## Environment Variables

All service configuration is driven by the `.env` file.
**Never commit real secrets**; commit only placeholders and add `.env` to `.gitignore`.
See [`.env.example`](./.env.example) for a full list of supported variables.

## Docker Compose Services

* **zookeeper**: Coordination service for Kafka.
* **kafka**: Message broker with SASL\_SSL listeners.
* **producer**: Fetches social media posts and publishes to Kafka.
* **minio**: S3-compatible storage over HTTPS.
* **spark-master/worker**: Spark cluster with TLS.
* **spark-streaming**: Real-time processing job writing to Delta Lake.
* **ml-api**: FastAPI-based ML inference service.
* **proxy**: Nginx reverse proxy handling TLS termination.
* **grafana**: Dashboard for Prometheus metrics.
* **prometheus**: Metrics collection for all services.

## Security Considerations

* **TLS Everywhere**: All inter-service and external communication is encrypted.
* **No Plaintext Ports**: Only the Nginx proxy exposes external ports.
* **Secrets Management**: Credentials are injected at runtime; no hard-coded secrets.
* **Rotate Certificates & Keys**: Establish a rotation policy for keystores, truststores, and application secrets.

## Monitoring & Logging

* **Logging**: JSON-file driver with size and file count limits to prevent disk exhaustion.
* **Metrics**: Exported by each service and scraped by Prometheus.
* **Dashboards**: Pre-configured Grafana dashboards are included under `./grafana/provisioning`.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
