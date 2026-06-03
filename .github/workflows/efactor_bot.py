import os
import json
import requests

# 1. Load Environment Variables
ai_api_key = os.environ.get('AI_API_KEY')
github_token = os.environ.get('GITHUB_TOKEN')
pr_number = os.environ.get('PR_NUMBER')
repo_name = os.environ.get('REPO_NAME')

# 2. Read the PR Diff
with open('pr_diff.txt', 'r') as file:
    diff_content = file.read()

if not diff_content.strip():
    print("No changes found.")
    exit(0)

# 3. Call the AI API (Example using an OpenAI-like endpoint)
# Adjust this to match whatever AI service you used for your assignment
prompt = f"""
You are an expert software engineer. Review the following code diff. 
Identify areas for refactoring to improve cleanliness, efficiency, and maintainability.
Provide:
1. A brief explanation of why the changes are needed.
2. The refactored code.

Diff:
{diff_content}
"""

# Pseudo-code for your API request
headers = {
    "Authorization": f"Bearer {ai_api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "your-chosen-model",
    "messages": [{"role": "user", "content": prompt}]
}

# Replace with your actual AI API URL
response = requests.post("https://api.your-ai-provider.com/v1/chat/completions", headers=headers, json=payload)
ai_reply = response.json()['choices'][0]['message']['content']

# 4. Post the result back to GitHub as a PR Comment
comment_url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
gh_headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github.v3+json"
}
comment_payload = {
    "body": f"### 🤖 RefactorBot Suggestions\n\n{ai_reply}"
}

requests.post(comment_url, headers=gh_headers, json=comment_payload)
print("Successfully posted refactoring suggestions to PR!")
