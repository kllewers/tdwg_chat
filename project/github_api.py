import requests
import os 
import json

# Configure your GitHub personal access token for authentication
token = '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'
headers = {'Authorization': f'token {token}'}

# Specify the repository from which to fetch issues
repo_name = "tdwg/dwc"  # Replace with the actual owner and repository name
url = f"https://api.github.com/repos/{repo_name}/issues"

# Make the request to get issues
response = requests.get(url, headers=headers)

response = requests.get(url, headers=headers)
if response.status_code == 200:
    issues = response.json()
else:
    print(f"Failed to fetch issues. Status code: {response.status_code}")
    print(f"Response body: {response.text}")

# Assuming 'issues' contains the list of issues fetched from GitHub
for issue in issues:
    # Simplified example: using issue title as the prompt and body as the completion
    prompt = issue["title"]
    completion = issue["body"]  # You may want to preprocess text to remove markdown, URLs, etc.

    # Format as a JSON object (dictionary in Python) for a single line in JSONL
    formatted_data = {"prompt": prompt, "completion": completion}
    print(formatted_data)  # This is where you'd actually write to a file

# Open a file to write
with open("dwc_github_issues_dataset.jsonl", "w") as file:
    for issue in issues:
        prompt = issue["title"]
        completion = issue["body"]
        formatted_data = {"prompt": prompt, "completion": completion}

        # Convert the dictionary to a JSON string and write it to the file
        json_line = json.dumps(formatted_data)
        file.write(json_line + "\n")
