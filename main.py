import email
from html import escape


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

    # Escape HTML special characters
    escaped_html = escape(html)

    return escaped_html


def html_extract_table(html):
    pass
     


if __name__ == "__main__":
    html = eml_to_html("./eml/2023-01-30|19:32.eml")