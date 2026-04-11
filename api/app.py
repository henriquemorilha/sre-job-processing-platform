from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter
import redis
import uuid

app = FastAPI()

# Conexão com Redis
redis_client = redis.Redis(host="sre-redis", port=6379, db=0)

# Métrica customizada
jobs_created = Counter("jobs_created_total", "Total de jobs criados")

@app.post("/job")
def create_job(payload: dict):
    job_id = str(uuid.uuid4())
    redis_client.lpush("job_queue", job_id)
    jobs_created.inc()  # incrementa contador
    return {"job_id": job_id}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    status = redis_client.get(f"job:{job_id}:status")
    if status:
        return {"job_id": job_id, "status": status.decode("utf-8")}
    return {"job_id": job_id, "status": "not_found"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Instrumentação Prometheus
Instrumentator().instrument(app).expose(app)
