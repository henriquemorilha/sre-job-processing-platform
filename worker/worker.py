import redis
import time
import json
import random
from datetime import datetime, UTC

# força conexão local
r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)


def now():
    return datetime.now(UTC).isoformat()


def process_job(job):
    time.sleep(2)

    if random.random() < 0.3:
        raise Exception("Random processing failure")


print("🚀 Worker started...")

while True:
    print("⏳ Waiting for job...")

    result = r.brpop("queue", timeout=5)

    if not result:
        print("⚠️ No job found in queue...")
        continue

    _, job_data = result
    job = json.loads(job_data)

    job_id = job["id"]

    print(f"📥 Job received: {job_id}")

    try:
        job["status"] = "processing"
        job["updated_at"] = now()
        r.set(job_id, json.dumps(job))

        process_job(job)

        job["status"] = "completed"
        job["updated_at"] = now()
        job["error"] = None

        print(f"✅ Job completed: {job_id}")

        r.set(job_id, json.dumps(job))

    except Exception as e:
        job["attempts"] += 1
        job["error"] = str(e)
        job["updated_at"] = now()

        print(f"❌ Job failed: {job_id} | Attempt {job['attempts']}")

        if job["attempts"] < job["max_attempts"]:
            job["status"] = "retrying"
            r.lpush("queue", json.dumps(job))
        else:
            job["status"] = "failed"
            r.set(job_id, json.dumps(job))
            print(f"💀 Job permanently failed: {job_id}")