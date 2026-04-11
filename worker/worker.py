import logging
import time
import redis
import os
from prometheus_client import Counter, start_http_server

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

# Pega variável de ambiente
redis_url = os.getenv("REDIS_URL")

# Conexão com Redis (Upstash)
if redis_url:
    redis_client = redis.Redis.from_url(
        redis_url,
        decode_responses=True
    )
else:
    logging.warning("REDIS_URL not set")
    redis_client = None

# Métricas customizadas
jobs_created = Counter("jobs_created_total", "Total de jobs criados")
jobs_completed = Counter("jobs_completed_total", "Total de jobs completados")
jobs_failed = Counter("jobs_failed_total", "Total de jobs falhados")

# Expor métricas na porta 8001
start_http_server(8001, addr="0.0.0.0")

def process_job(job_id):
    logging.info(f"Consumindo job {job_id}")
    jobs_created.inc()
    try:
        # Simula processamento
        time.sleep(2)
        redis_client.set(f"job:{job_id}:status", "completed")
        jobs_completed.inc()
        logging.info(f"Job {job_id} concluído com sucesso ✅")
    except Exception as e:
        redis_client.set(f"job:{job_id}:status", "failed")
        jobs_failed.inc()
        logging.error(f"Falha ao processar job {job_id}: {e}")

def main():
    if not redis_client:
        logging.error("Redis não configurado")
        return

    while True:
        logging.info("Esperando job...")
        job_id = redis_client.rpop("job_queue")
        if job_id:
            process_job(job_id)
        else:
            time.sleep(1)

if __name__ == "__main__":
    main()
