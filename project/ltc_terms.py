import requests
from bs4 import BeautifulSoup
import json

# URL of the page you want to scrape
url = "https://ltc.tdwg.org/terms/"

# Send a GET request to the page
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.content, 'html.parser')

# Initialize a list to store the scraped data
terms_data = []

# The given HTML seems to be a series of tables or similar structure for each term
# Let's find each term's table and extract information
tables = soup.find_all('table', class_='table-compact')  # Assuming class to narrow down

for table in tables:
    term_data = {}
    # Iterate through each row in the table
    for row in table.find_all('tr'):
        # Try to extract data from both 'th' and 'td' elements
        header = row.find('th').get_text(strip=True) if row.find('th') else None
        value = row.find('td').get_text(strip=True) if row.find('td') else None

        # Check for link in 'td' and possibly override the value with the href attribute
        if row.find('td') and row.find('td').find('a'):
            value = row.find('td').find('a')['href']

        if header and value:
            if header == "Qualified Term":
                header = "Term"
            term_data[header] = value

        

    if term_data:  # Ensure it's not empty
        terms_data.append(term_data)

# Specify the filename where the output should be saved
file_name = "ltc_terms.jsonl"

# Write the output to a .jsonl file
with open(file_name, 'w') as outfile:
    for term in terms_data:
        json_line = json.dumps(term)
        outfile.write(json_line + '\n')

print(f"Data extracted and saved to {file_name}")