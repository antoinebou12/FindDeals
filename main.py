import os
import email
from html import escape
import requests
from bs4 import BeautifulSoup

import imaplib
import email

import pandas as pd
import csv


from dotenv import load_dotenv


# Load the environment variables from .env
load_dotenv()


# This modified function will download all emails from the specified sender,
# extract the HTML content from each one, find the table in each HTML content,
# and then do whatever processing you want with the table (e.g., write it to a file).


def download_eml():
    # Login credentials
    # Get the values for the OUTLOOK_USERNAME and OUTLOOK_PASSWORD variables
    username = os.getenv("OUTLOOK_USERNAME")
    password = os.getenv("OUTLOOK_PASSWORD")

    # Connect to the IMAP server
    imap_server = "outlook.office365.com"
    imap_port = 993
    mail = imaplib.IMAP4_SSL(imap_server, imap_port)

    # Login to the email account
    mail.login(username, password)

    # Select the inbox folder
    mail.select("inbox")

    # Search for all emails from the specified sender
    sender = "transaction@transaction-metro.ca"
    result, data = mail.search(None, f'(FROM "{sender}")')

    # Loop through the list of email ids and download each one as an eml file
    for email_id in data[0].split():
        result, data = mail.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        file_name = f"{email_message['Subject']}.eml"
        with open(file_name, "wb") as f:
            f.write(raw_email)

    # Logout from the email account
    mail.logout()


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
    soup = BeautifulSoup(html, "html.parser")

    soup.prettify()

    # td class outlook-fallback-font-family-receipt ereceipt-font-size
    table = soup.find(
        "td", attrs={"class": "outlook-fallback-font-family-receipt ereceipt-font-size"}
    )
    print(table)

    for row in table.find_all("tr"):
        for cell in row.find_all("td"):
            print(cell.text)


def parse_transaction_data():

    categories = {
        "EPICERIE": "Groceries",
        "VIANDE": "Meat",
        "CHARCUTERIE": "Charcuterie",
        "MICHE": "Bakery",
        "FROMAGE": "Cheese",
        
    }


if __name__ == "__main__":
    html = eml_to_html("eml/Antoine, Your digital receipt has arrived.eml")
    table = html_extract_table(html)
    print(table)

    parse_transaction_data()
