from fastapi import FastAPI
import redis
import uuid
import json
from datetime import datetime, UTC

app = FastAPI()

# força conexão local (evita bug no Windows)
r = redis.Redis(host="redis", port=6379, decode_responses=True)


def now():
    return datetime.now(UTC).isoformat()


@app.get("/")
def root():
    return {"message": "SRE Job Platform API is running"}


@app.post("/job")
def create_job():
    job_id = str(uuid.uuid4())

    job = {
        "id": job_id,
        "status": "pending",
        "created_at": now(),
        "updated_at": now(),
        "attempts": 0,
        "max_attempts": 3,
        "error": None
    }

    print(f"[API] Creating job {job_id}")

    r.set(job_id, json.dumps(job))
    r.lpush("queue", json.dumps(job))

    return job


@app.get("/status/{job_id}")
def get_status(job_id: str):
    data = r.get(job_id)

    if not data:
        return {"status": "not_found"}

    return json.loads(data)


@app.get("/health")
def health():
    return {"status": "ok"}