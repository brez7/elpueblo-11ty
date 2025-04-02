from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "brez7"  # <-- replace with yours
REPO_NAME = "elpueblo-11ty"  # <-- replace with yours

app = FastAPI()


@app.post("/check-updates")
async def check_latest_commits_post(request: Request):
    payload = await request.json()
    print("✅ Received POST data:", payload)

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "GitHub API failed", "status": response.status_code}

    commits = response.json()
    latest = [
        {
            "sha": c["sha"],
            "message": c["commit"]["message"],
            "author": c["commit"]["author"]["name"],
            "date": c["commit"]["author"]["date"],
        }
        for c in commits[:5]
    ]

    return {"received_payload": payload, "latest_commits": latest}
