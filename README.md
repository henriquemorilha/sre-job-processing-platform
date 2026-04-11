SRE Job Platform
A complete Job Processing Platform built with Python, Redis, Kubernetes, Prometheus, and Grafana.
This project demonstrates how to design, deploy, and monitor a distributed system with observability at its core.

🚀 Features
Job API: RESTful service to create jobs and enqueue them in Redis.

Worker: Background processor that consumes jobs from Redis and executes them.

Redis: Acts as the job queue.

Prometheus: Collects metrics from API and Worker.

Grafana: Visualizes metrics with dashboards.

Kubernetes Deployment: All components run inside a Kubernetes cluster.

📂 Project Structure

sre-job-platform/
├── api/          # Job API service
├── worker/       # Worker service
├── infra/k8s/    # Kubernetes manifests
└── README.md     # Documentation

⚙️ Setup Instructions

1. Build and Push Docker Images

cd worker
docker build -t <your-dockerhub-username>/sre-worker:latest .
docker push <your-dockerhub-username>/sre-worker:latest

cd ../api
docker build -t <your-dockerhub-username>/sre-api:latest .
docker push <your-dockerhub-username>/sre-api:latest

2. Deploy to Kubernetes

kubectl apply -f infra/k8s/


3. Restart Deployments (after updates)

kubectl rollout restart deploy sre-api -n sre
kubectl rollout restart deploy sre-worker -n sre


📡 Usage

Create a Job

curl -X POST http://localhost:32507/job \
     -H "Content-Type: application/json" \
     -d '{"payload":"test"}'

Response:

json
{ "job_id": "123e4567-e89b-12d3-a456-426614174000" }
Worker Logs
bash
kubectl logs -n sre <worker-pod-name> -f

Expected output:

INFO: Waiting for job...
INFO: Consuming job 123e4567-e89b-12d3-a456-426614174000
INFO: Job 123e4567-e89b-12d3-a456-426614174000 completed successfully


📊 Observability

Prometheus

Metrics exposed:

 - jobs_created_total

 - jobs_completed_total

 - jobs_failed_total

Grafana

Dashboards visualize:

 - Jobs created per minute

 - Jobs completed per minute

 - Total jobs failed

Alerts can be configured for job failures.

📌 Next Steps
Add retry logic for failed jobs.

Expand Grafana dashboards with alerts.

Document scaling strategies for Worker replicas.

👨‍💻 Author
Henrique Morilha

IT Specialist | Mainframe Operations & Infrastructure | SRE & DevOps Practices | Automation & Observability

📍 Brazil 🔗 LinkedIn: https://www.linkedin.com/in/hmorilha/
