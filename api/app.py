from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter
import redis
import uuid
import os

app = FastAPI()

# Pega variável de ambiente
redis_url = os.getenv("REDIS_URL")

# Conexão com Redis (Upstash - com SSL + timeout)
if redis_url:
    redis_client = redis.Redis.from_url(
        redis_url,
        decode_responses=True
    )
else:
    print("WARNING: REDIS_URL not set")
    redis_client = None

# Métrica customizada
jobs_created = Counter("jobs_created_total", "Total de jobs criados")

@app.get("/")
def root():
    return {
        "message": "SRE Job Processing Platform is running 🚀",
        "endpoints": [
            "/job (POST)",
            "/status/{job_id}",
            "/health",
            "/debug",
            "/metrics"
        ]
    }

@app.post("/job")
def create_job(payload: dict):
    if not redis_client:
        return {"error": "Redis not configured"}

    try:
        # Testa conexão
        print("PING:", redis_client.ping())
    except Exception as e:
        print("REDIS ERROR:", str(e))
        return {"error": str(e)}

    job_id = str(uuid.uuid4())

    try:
        redis_client.lpush("job_queue", job_id)
        jobs_created.inc()
    except Exception as e:
        print("LPUSH ERROR:", str(e))
        return {"error": str(e)}

    return {"job_id": job_id}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    if not redis_client:
        return {"error": "Redis not configured"}

    try:
        status = redis_client.get(f"job:{job_id}:status")
    except Exception as e:
        return {"error": str(e)}

    if status:
        return {"job_id": job_id, "status": status}

    return {"job_id": job_id, "status": "not_found"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/debug")
def debug():
    return {"redis_url": redis_url}

# Prometheus
Instrumentator().instrument(app).expose(app)
