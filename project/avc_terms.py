import requests
from bs4 import BeautifulSoup
import json

# URL of the page you want to scrape
url = "https://ac.tdwg.org/termlist/"

# Send a GET request to the page
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize a list to store the scraped data
terms_data = []

# Find all table elements in the HTML
tables = soup.find_all('table')

# Iterate through each table to extract term information
for table in tables:
    term_data = {}
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if not cells:
            term_name_content = row.find('th').get_text(strip=True)
            # Check if the term name content actually contains the expected delimiter
            if ': ' in term_name_content:
                term_name = term_name_content.split(': ')[1]
            else:
                # Handle the case where the delimiter is not found (e.g., set to a default value or skip)
                term_name = "Unknown or Malformed Term Name"
            term_data['Term Name'] = term_name
        else:
            key = cells[0].get_text(strip=True)
            if 'Required:' in key:
                required_repeatable = cells[1].get_text(strip=True).split(' -- ')
                term_data['Required'] = required_repeatable[0].split(': ')[1] if len(required_repeatable) > 0 else "Unknown"
                term_data['Repeatable'] = required_repeatable[1].split(': ')[1] if len(required_repeatable) > 1 else "Unknown"
            else:
                value = cells[1].get_text(strip=True)
                if cells[1].find('a'):
                    value = cells[1].find('a')['href']
                term_data[key] = value
    terms_data.append(term_data)

file = "avc_terms.jsonl"

# Write the output to a .jsonl file
with open(file, 'w') as outfile:
    for term in terms_data:
        # Convert each dictionary to a JSON string and write it to the file
        json_line = json.dumps(term)
        outfile.write(json_line + '\n')