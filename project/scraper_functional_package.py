import requests
import json

"""def fetch_and_write_github_issues(token, repo_name, output_filename):
    Fetch GitHub issues for the specified repository and write them to a .jsonl file.
    
    # Configure the request headers with the provided authentication token
    headers = {'Authorization': f'token {token}'}
    
    # Construct the URL for fetching issues from the specified repository
    url = f"https://api.github.com/repos/{repo_name}/issues"
    
    # Make the request to get issues
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        issues = response.json()
        
        # Open a file to write the issues data
        with open(output_filename, "w") as file:
            for issue in issues:
                # Extract the title as prompt and body as completion from each issue
                prompt = issue["title"]
                completion = issue["body"]  # Consider preprocessing to remove markdown, URLs, etc.
                
                # Format the data as a JSON object (dictionary in Python)
                formatted_data = {"prompt": prompt, "completion": completion}
                
                # Convert the dictionary to a JSON string and write it to the file with a newline
                json_line = json.dumps(formatted_data)
                file.write(json_line + "\n")
    else:
        # Print an error message if the request failed
        print(f"Failed to fetch issues. Status code: {response.status_code}")
        print(f"Response body: {response.text}")

# Example usage
token = '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'  # Replace with your actual GitHub token
repo_name = "tdwg/dwc"  # Repository from which to fetch issues
output_filename = "dwc_github_issues_data.jsonl"  # Output file name

# Call the function
fetch_and_write_github_issues(token, repo_name, output_filename)"""

from bs4 import BeautifulSoup
import requests
import json

# URL of the page to scrape
url = 'https://dwc.tdwg.org/terms/'

def scrape_dwc_terms(url)
    # Make the request to get the page content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the page title from the <head> section and add it as the first term
    page_title = soup.head.find('title').text.strip()
    terms_details = [{'Term': 'Page Title', 'Definition': page_title, 'Comments': '', 'Examples': []}]

    # Find all tables - assuming each set of term details is in its own table
    tables = soup.find_all('table')

    # Process each table for DwC terms
    for table in tables:
        term_details = {}
        rows = table.find_all('tr')
        for row in rows:
            first_td = row.find('td')
            # Check if the row contains at least one <td>
            if first_td:
                # Assuming the first column is always the field name
                field_name = first_td.text.strip()
                # Handle the Identifier specifically to extract the last part of the URL
                if field_name.lower() == 'identifier':
                    url = first_td.find_next_sibling('td').find('a')['href']
                    identifier_last_part = url.split('/')[-1]  # Get the last part after the last slash
                    term_details['Term'] = identifier_last_part
                else:
                    # The second column is the field value for other fields
                    field_value = first_td.find_next_sibling('td').text.strip()
                    # Special handling for examples which might have a list structure
                    if field_name.lower() == 'examples':
                        examples = first_td.find_next_sibling('td').find_all('li')
                        field_value = [example.text.strip() for example in examples]
                    term_details[field_name] = field_value

        # Add the collected term details to the list if it's not empty
        if term_details:
            terms_details.append(term_details)

    # Write the output to a .jsonl file
    with open('dwc_terms_2.jsonl', 'w') as outfile:
        for term_detail in terms_details:
            # Convert each dictionary to a JSON string and write it to the file
            json_line = json.dumps(term_detail)
            outfile.write(json_line + '\n')

scrape_dwc_terms('https://dwc.tdwg.org/terms/')