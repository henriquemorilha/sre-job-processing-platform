# 🚀 SRE Job Processing Platform

> A production-like **distributed job processing system** designed with **observability, scalability, and reliability** at its core.

This project simulates a real-world SRE scenario where services must handle asynchronous workloads, expose meaningful metrics, and operate reliably under a distributed architecture.

---

## 🧠 Overview

Modern systems rely heavily on **background job processing** — from payments to notifications and data pipelines.

This platform demonstrates how to:

* Design a **decoupled architecture** using queues
* Process jobs **asynchronously and reliably**
* Implement **observability-first systems**
* Deploy and manage services using **Kubernetes**

---

## 🏗️ Architecture

```
        ┌──────────────┐
        │    Client    │
        └──────┬───────┘
               │ HTTP
               ▼
        ┌──────────────┐
        │   Job API    │
        └──────┬───────┘
               │ Push job
               ▼
        ┌──────────────┐
        │    Redis     │  ← Queue
        └──────┬───────┘
               │ Consume
               ▼
        ┌──────────────┐
        │    Worker    │
        └──────────────┘

        📊 Metrics → Prometheus → Grafana
```

---

## ✨ Key Features

### ⚙️ Distributed Job Processing

* API receives jobs and pushes them to Redis
* Workers consume jobs independently
* Fully decoupled architecture

### 📊 Observability First

* Metrics exposed via Prometheus
* Dashboards built in Grafana
* Tracks:

  * Jobs created
  * Jobs completed
  * Jobs failed

### ☸️ Kubernetes Native

* Fully containerized services
* Deployed with Kubernetes manifests
* Easy to scale workers horizontally

### 🔄 Scalable by Design

* Workers can be replicated to handle load
* Queue-based architecture prevents bottlenecks

---

## 🧱 Tech Stack

* **Python (FastAPI)** — API layer
* **Python Worker** — background processing
* **Redis** — job queue
* **Docker** — containerization
* **Kubernetes** — orchestration
* **Prometheus** — metrics collection
* **Grafana** — visualization & dashboards

---

## 📂 Project Structure

```bash
sre-job-platform/
├── api/           # FastAPI service
├── worker/        # Background job processor
├── infra/k8s/     # Kubernetes manifests
└── README.md
```

---

## ⚙️ Getting Started

### 1. Build & Push Images

```bash
cd worker
docker build -t <your-dockerhub-username>/sre-worker:latest .
docker push <your-dockerhub-username>/sre-worker:latest

cd ../api
docker build -t <your-dockerhub-username>/sre-api:latest .
docker push <your-dockerhub-username>/sre-api:latest
```

---

### 2. Deploy to Kubernetes

```bash
kubectl apply -f infra/k8s/
```

---

### 3. Verify Deployment

```bash
kubectl get pods -n sre
```

---

### 4. Restart Services (if needed)

```bash
kubectl rollout restart deploy sre-api -n sre
kubectl rollout restart deploy sre-worker -n sre
```

---

## 📡 API Usage

### Create a Job

```bash
curl -X POST http://localhost:32507/job \
-H "Content-Type: application/json" \
-d '{"payload":"test"}'
```

### Response

```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

---

## 🔍 Monitoring & Observability

### 📊 Prometheus Metrics

* `jobs_created_total`
* `jobs_completed_total`
* `jobs_failed_total`

---

### 📈 Grafana Dashboards

Visualize:

* Jobs created per minute
* Jobs completed per minute
* Failure rates

➡️ Enables real-time monitoring and alerting strategies

---

## 🧪 Example Worker Logs

```bash
INFO: Waiting for job...
INFO: Consuming job 123e4567-e89b-12d3-a456-426614174000
INFO: Job 123e4567-e89b-12d3-a456-426614174000 completed successfully
```

---

## 📌 Future Improvements

* [ ] Retry mechanism for failed jobs
* [ ] Dead-letter queue (DLQ)
* [ ] Advanced alerting in Grafana
* [ ] Horizontal Pod Autoscaler (HPA)
* [ ] Load testing scenarios

---

## 🎯 What This Project Demonstrates

* Real-world **SRE mindset**
* Observability-driven development
* Distributed systems fundamentals
* Kubernetes-based deployments
* Scalable job processing architecture

---

## 👨‍💻 Author

**Henrique Morilha**

IT Specialist | Mainframe Operations & Infrastructure
| SRE & DevOps Practices | Automation & Observability

📍 Brazil
🔗 https://www.linkedin.com/in/hmorilha/

---

## ⭐ Final Note

This is not just a demo — it's a **practical representation of how modern backend systems are designed and operated in production environments**.
