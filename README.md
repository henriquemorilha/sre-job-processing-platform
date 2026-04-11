# 🚀 SRE Job Platform

A complete **Job Processing Platform** built with **Python, Redis, Kubernetes, Prometheus, and Grafana**.

This project demonstrates how to design, deploy, and monitor a **distributed system with observability at its core**, following SRE and DevOps best practices.

---

## ✨ Features

* **Job API**
  RESTful service to create jobs and enqueue them in Redis

* **Worker**
  Background processor that consumes and executes jobs

* **Redis**
  Acts as a job queue

* **Prometheus**
  Collects metrics from API and Worker

* **Grafana**
  Visualizes metrics through dashboards

* **Kubernetes Deployment**
  All components run inside a Kubernetes cluster

---

## 📂 Project Structure

```bash
sre-job-platform/
├── api/           # Job API service
├── worker/        # Worker service
├── infra/k8s/     # Kubernetes manifests
└── README.md      # Documentation
```

---

## ⚙️ Setup Instructions

### 1. Build and Push Docker Images

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

### 3. Restart Deployments (after updates)

```bash
kubectl rollout restart deploy sre-api -n sre
kubectl rollout restart deploy sre-worker -n sre
```

---

## 📡 Usage

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

### Worker Logs

```bash
kubectl logs -n sre -f <worker-pod-name>
```

### Expected Output

```bash
INFO: Waiting for job...
INFO: Consuming job 123e4567-e89b-12d3-a456-426614174000
INFO: Job 123e4567-e89b-12d3-a456-426614174000 completed successfully
```

---

## 📊 Observability

### Prometheus

Available metrics:

* `jobs_created_total`
* `jobs_completed_total`
* `jobs_failed_total`

---

### Grafana

Dashboards include:

* Jobs created per minute
* Jobs completed per minute
* Total failed jobs

You can also configure **alerts for job failures**.

---

## 📌 Next Steps

* [ ] Add retry logic for failed jobs
* [ ] Expand Grafana dashboards with alerts
* [ ] Document scaling strategies for worker replicas

---

## 👨‍💻 Author

**Henrique Morilha**

IT Specialist | Mainframe Operations & Infrastructure
SRE & DevOps Practices | Automation & Observability

📍 Brazil
🔗 LinkedIn: https://www.linkedin.com/in/hmorilha/

---

## ⭐ About This Project

This project was built to demonstrate **real-world SRE concepts**, including:

* Distributed job processing
* Observability-first architecture
* Containerization and orchestration
* Scalable system design

---
