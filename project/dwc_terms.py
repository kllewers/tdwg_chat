from bs4 import BeautifulSoup
import requests

# URL of the page to scrape
url = 'https://dwc.tdwg.org/terms/'

# Make the request to get the page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all tables - assuming each set of term details is in its own table
tables = soup.find_all('table')

# Initialize a list to hold all terms details
terms_details = []

# Process each table
for table in tables:
    term_details = {}
    rows = table.find_all('tr')
    for row in rows:
        first_td = row.find('td')
        # Check if the row contains at least one <td>
        if first_td:
            # Assuming the first column is always the field name
            field_name = first_td.text.strip()
            # The second column is the field value
            field_value = first_td.find_next_sibling('td').text.strip()
            # Special handling for examples which might have a list structure
            if field_name.lower() == 'examples':
                examples = first_td.find_next_sibling('td').find_all('li')
                field_value = [example.text.strip() for example in examples]
            term_details[field_name] = field_value

    # Add the collected term details to the list if it's not empty
    if term_details:
        terms_details.append(term_details)

# Display the collected terms details
for term in terms_details:
    print(term)

import json

# Assuming `terms_details` is your list of dictionaries from the previous script
with open('dwc_terms.jsonl', 'w') as outfile:
    for term_detail in terms_details:
        # Convert each dictionary to a JSON string and write it to the file
        json_line = json.dumps(term_detail)
        outfile.write(json_line + '\n')
