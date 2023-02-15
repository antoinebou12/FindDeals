import email
from html import escape
import requests
from bs4 import BeautifulSoup


def eml_to_html(eml_file):
    # Read the EML file
    with open(eml_file, "r") as f:
        raw_email = f.read()

    # Parse the raw email message using the email library
    message = email.message_from_string(raw_email)

    # Extract the HTML part of the message
    for part in message.walk():
        if part.get_content_type() == "text/html":
            html = part.get_payload(decode=True).decode("utf-8")

    return html


def html_extract_table(html):
    soup = BeautifulSoup(html, 'html.parser')

    soup.prettify()

    # td class outlook-fallback-font-family-receipt ereceipt-font-size
    table = soup.find('td', attrs={'class': 'outlook-fallback-font-family-receipt ereceipt-font-size'})
    print(table)

    for row in table.find_all('tr'):
        for cell in row.find_all('td'):
            print(cell.text)

            



if __name__ == "__main__":
    html = eml_to_html("./eml/2023-01-30|19:32.eml")
    html_extract_table(html)