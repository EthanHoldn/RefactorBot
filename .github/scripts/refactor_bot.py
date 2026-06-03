import os
import requests

AI_API_KEY = os.environ["AI_API_KEY"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
PR_NUMBER = os.environ["PR_NUMBER"]
REPO_NAME = os.environ["REPO_NAME"]

# Read the PR diff
with open("pr_diff.txt", "r") as f:
    diff = f.read()

if not diff.strip():
    print("No diff found, skipping.")
    exit(0)

# Truncate diff if too large to avoid exceeding model context limits
MAX_DIFF_CHARS = 12000
if len(diff) > MAX_DIFF_CHARS:
    diff = diff[:MAX_DIFF_CHARS] + "\n\n[diff truncated]"

# Call the OpenAI API to get refactoring suggestions
response = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers={
        "Authorization": "Bearer " + AI_API_KEY,
        "Content-Type": "application/json",
    },
    json={
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a code review assistant specializing in refactoring. "
                    "Analyze the provided git diff and suggest concrete, actionable "
                    "refactoring improvements. Be concise and focus on the most impactful changes. "
                    "Format your response as a GitHub pull request comment using markdown."
                ),
            },
            {
                "role": "user",
                "content": f"Please review this pull request diff and suggest refactoring improvements:\n\n```diff\n{diff}\n```",
            },
        ],
        "max_tokens": 1024,
        "temperature": 0.3,
    },
    timeout=60,
)

response.raise_for_status()
suggestion = response.json()["choices"][0]["message"]["content"]

# Post the suggestion as a PR comment
comment_body = f"## 🤖 AI Refactoring Suggestions\n\n{suggestion}"

github_response = requests.post(
    f"https://api.github.com/repos/{REPO_NAME}/issues/{PR_NUMBER}/comments",
    headers={
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    },
    json={"body": comment_body},
    timeout=30,
)

github_response.raise_for_status()
print(f"Posted refactoring suggestions to PR #{PR_NUMBER}")
