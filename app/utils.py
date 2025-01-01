import requests # type: ignore
from fastapi import HTTPException # type: ignore

def fetch_pr_diff(repo_url, pr_number, github_token=None):
    headers = {}
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"
    response = requests.get(f"{repo_url}/pull/{pr_number}.diff", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch PR diff")
    return response.text

def analyze_code(diff):
    return {
        "files": [
            {
                "name": "example.py",
                "issues": [
                    {
                        "type": "style",
                        "line": 15,
                        "description": "Line too long",
                        "suggestion": "Break line into multiple lines"
                    },
                    {
                        "type": "bug",
                        "line": 23,
                        "description": "Potential null pointer",
                        "suggestion": "Add null check"
                    }
                ]
            }
        ],
        "summary": {
            "total_files": 1,
            "total_issues": 2,
            "critical_issues": 1
        }
    }
