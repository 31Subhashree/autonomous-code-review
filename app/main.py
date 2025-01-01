from fastapi import FastAPI
from app.models import AnalyzePRRequest
from app.tasks import analyze_pr_task
from app.redis_config import redis_client
from uuid import uuid4
import json

app = FastAPI()

@app.post("/analyze-pr")
def analyze_pr(request: AnalyzePRRequest):
    task_id = str(uuid4())
    redis_client.set(task_id, json.dumps({"status": "pending"}))
    analyze_pr_task.apply_async(args=[task_id, request.dict()])
    return {"task_id": task_id, "status": "pending"}

@app.get("/status/{task_id}")
def get_status(task_id: str):
    task_data = redis_client.get(task_id)
    if not task_data:
        return {"error": "Task not found"}, 404
    return json.loads(task_data)

@app.get("/results/{task_id}")
def get_results(task_id: str):
    task_data = redis_client.get(task_id)
    if not task_data:
        return {"error": "Task not found"}, 404

    data = json.loads(task_data)
    if data["status"] != "completed":
        return {"error": "Task not completed yet"}, 400
    return data.get("results", {})
