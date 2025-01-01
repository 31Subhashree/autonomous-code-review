from celery import Celery # type: ignore
from app.utils import fetch_pr_diff, analyze_code
from app.redis_config import redis_client
import json
import os

celery_app = Celery(
    "code_review_tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_BACKEND_URL", "redis://localhost:6379/0")
)

@celery_app.task(bind=True)
def analyze_pr_task(self, task_id, request_data):
    try:
        diff = fetch_pr_diff(request_data["repo_url"], request_data["pr_number"], request_data.get("github_token"))
        results = analyze_code(diff)
        redis_client.set(task_id, json.dumps({"status": "completed", "results": results}))
    except Exception as e:
        redis_client.set(task_id, json.dumps({"status": "failed", "error": str(e)}))
