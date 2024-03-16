from bs4 import BeautifulSoup
import requests
import json

# URL of the page to scrape
url = 'https://dwc.tdwg.org/terms/'

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
with open('dwc_terms.jsonl', 'w') as outfile:
    for term_detail in terms_details:
        # Convert each dictionary to a JSON string and write it to the file
        json_line = json.dumps(term_detail)
        outfile.write(json_line + '\n')
