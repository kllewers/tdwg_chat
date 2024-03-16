import requests
from bs4 import BeautifulSoup

url = "https://dwc.tdwg.org/terms/"  # The URL where the terms are listed
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Example: Extracting term names - Adjust the selector based on actual page structure
for term in soup.select('table.terms tr td:first-child'):
    print(term.text)