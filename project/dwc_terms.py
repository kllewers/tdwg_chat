from bs4 import BeautifulSoup
import requests
import json

# URL of the page to scrape
url = "https://dwc.tdwg.org/list/"

# Send a GET request to the page
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize an empty list to hold all terms
terms = []

# Find all tables and iterate over them
for table in soup.find_all('table'):
    # Initialize an empty dictionary for the term
    term_data = {}
    
    # Extracting term name from the table's heading
    heading = table.find('th').text.strip()
    # Removing "Term Name: " prefix and updating to just "Term"
    term_name = heading.replace('Term Name: ', '')
    if term_name.startswith('Term Name '):
        term_name = term_name.replace('Term Name  ', '', 1)
    term_data['Term'] = term_name
    # Additional step to remove "Term Name " prefix if it exists

    
    # Iterate over all rows in the table body to extract term details
    for row in table.find('tbody').find_all('tr'):
        cells = row.find_all('td')
        if cells and len(cells) > 1:
            # Assuming the first cell is the key and the second is the value
            key = cells[0].text.strip()
            value = cells[1].text.strip()
            # Special handling for URLs
            if cells[1].find('a'):
                value = cells[1].find('a')['href']
            term_data[key] = value

    # Add the populated term data to the terms list
    terms.append(term_data)

# Specify the filename where the output should be saved
file_name = "dwc_terms.jsonl"

# Write the output to a .jsonl file
with open(file_name, 'w') as outfile:
    for term in terms:
        json_line = json.dumps(term)
        outfile.write(json_line + '\n')

print(f"Data extracted and saved to {file_name}")
