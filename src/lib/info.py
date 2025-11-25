import imaplib
from email import message_from_bytes
from email.message import EmailMessage
import re


def _decode_bytes(payload, charset):
    """Decode a bytes payload using the given charset with fallbacks.

    Returns a Unicode string. Uses errors='replace' to avoid exceptions on
    malformed bytes.
    """
    if payload is None:
        return ""
    if isinstance(payload, str):
        return payload

    # payload is bytes
    if charset:
        try:
            return payload.decode(charset, errors="replace")
        except Exception:
            pass

    # Try common fallbacks
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return payload.decode(enc, errors="replace")
        except Exception:
            continue

    # Last resort
    return payload.decode("utf-8", errors="replace")


def _html_to_text(html: str) -> str:
    """Very small HTML -> text fallback used when only HTML body is present."""
    # Remove script/style
    text = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html)
    # Replace tags with spaces
    text = re.sub(r"<[^>]+>", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_email_body(msg: EmailMessage) -> str:
    """
    Extracts the body of an email message and returns a plain-text string.

    This function is defensive: it handles multipart messages, missing
    charsets, and falls back from HTML to text when no plain text part is
    available.
    """

    # If it's multipart, prefer text/plain parts, but remember text/html
    html_fallback = ""
    body_parts = []

    if msg.is_multipart():
        for part in msg.walk():
            # Skip containers
            if part.get_content_maintype() == "multipart":
                continue

            content_type = part.get_content_type()
            payload = part.get_payload(decode=True)
            charset = part.get_content_charset()

            if content_type == "text/plain":
                text = _decode_bytes(payload, charset)
                if text:
                    body_parts.append(text)
            elif content_type == "text/html":
                html_fallback = _decode_bytes(payload, charset)
    else:
        payload = msg.get_payload(decode=True)
        charset = msg.get_content_charset()
        body = _decode_bytes(payload, charset)
        if body:
            return body

    if body_parts:
        return "\n\n".join(p.strip() for p in body_parts if p.strip())

    if html_fallback:
        return _html_to_text(html_fallback)

    return ""

def latest_email_message(imap_server, imap_port, email, password):
    """
    Fetches the latest email from the specified email account using IMAP.

    Args:
        `imap_server` (str): IMAP server hostname
        `imap_port` (int): IMAP server port number
        `email` (str): Email address
        `password` (str): Email password (App password for Gmail)

    Returns:
        email.message.EmailMessage: The latest email message.

    You can access the sender, subject, and body of the email using the following properties:
    ```
        sender = msg['From']
        subject = msg['Subject']
        body = get_email_body(msg)
    ```

    """
    # Log in to the IMAP server
    imap = imaplib.IMAP4_SSL(imap_server, imap_port)
    imap.login(email, password)
    imap.select('INBOX')

    # Search for the latest email
    _, data = imap.search(None, 'ALL')
    email_ids = data[0].split()
    if not email_ids:
        print("No emails found. Inbox is empty.")
        return None
    
    latest_email_id = email_ids[-1]
    typ, data = imap.fetch(latest_email_id, '(RFC822)')
    raw_email = data[0][1]
    email_message = message_from_bytes(raw_email)
    
    imap.close()
    imap.logout()
    
    return data, email_message

def get_ssb(mail: EmailMessage) -> tuple:
    """
    Fetch the sender, subject, and body of an email.

    return: Tuple of sender, subject, and body
    """

    sender = mail['From']
    subject = mail['Subject']
    body = get_email_body(mail)

    return sender, subject, body

def RAWEmail(mail: EmailMessage) -> str:
    """
    Fetch the raw email.

    return: Raw email
    """
    # Return a string representation of the full email
    try:
        return mail.as_string()
    except Exception:
        # Fallback to bytes representation then decode
        try:
            raw = mail.as_bytes()
            return raw.decode("utf-8", errors="replace")
        except Exception:
            return ""