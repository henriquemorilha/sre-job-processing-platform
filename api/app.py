from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter
import redis
import uuid
import os

app = FastAPI()

redis_url = os.getenv("REDIS_URL")

if redis_url:
    redis_client = redis.from_url(redis_url, decode_responses=True)
else:
    print("WARNING: REDIS_URL not set")
    redis_client = None

# Métrica customizada
jobs_created = Counter("jobs_created_total", "Total de jobs criados")

@app.post("/job")
def create_job(payload: dict):
    if not redis_client:
        return {"error": "Redis not configured"}

    job_id = str(uuid.uuid4())
    redis_client.lpush("job_queue", job_id)
    jobs_created.inc()
    return {"job_id": job_id}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    if not redis_client:
        return {"error": "Redis not configured"}

    status = redis_client.get(f"job:{job_id}:status")
    if status:
        return {"job_id": job_id, "status": status}
    return {"job_id": job_id, "status": "not_found"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/debug")
def debug():
    return {"redis_url": redis_url}

# Instrumentação Prometheus
Instrumentator().instrument(app).expose(app)