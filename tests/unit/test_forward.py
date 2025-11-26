import io
import sys
import types
from email.message import EmailMessage

import pytest

# Ensure a dummy dotenv is available for imports in test environments without python-dotenv
if 'dotenv' not in sys.modules:
    mod = types.ModuleType('dotenv')
    mod.load_dotenv = lambda *a, **k: None
    sys.modules['dotenv'] = mod

# Provide a lightweight summarize shim to avoid importing heavy/absent deps (ollama, etc.)
if 'src.lib.summarize' not in sys.modules:
    sm = types.ModuleType('src.lib.summarize')
    sm.summarize_email = lambda x: 'summary'
    sys.modules['src.lib.summarize'] = sm


def make_html_email(html: str, subject: str = "Hi") -> EmailMessage:
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'a@example.com'
    msg['To'] = 'b@example.com'
    msg.set_content('fallback text')
    msg.add_alternative(html, subtype='html')
    return msg


def test_decode_subject_simple():
    from src.lib.forward import decode_subject

    assert decode_subject('Simple Subject') == 'Simple Subject'


def test_forward_email_mocks(monkeypatch):
    from src.lib import forward

    sent = {}

    class DummySMTP:
        def __init__(self, server, port):
            sent['server'] = server
            sent['port'] = port

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def starttls(self):
            sent['starttls'] = True

        def login(self, email, password):
            sent['login'] = (email, password)

        def send_message(self, msg, to_addrs=None):
            sent['to_addrs'] = to_addrs
            # capture the subject
            sent['subject'] = msg['Subject']

    # monkeypatch SMTP and summarize_email to avoid network/external calls
    monkeypatch.setattr('src.lib.forward.smtplib.SMTP', DummySMTP)
    monkeypatch.setattr('src.lib.forward.summarize_email', lambda x: 'short summary')

    html = '<p>Hello <b>world</b></p>'
    msg = make_html_email(html, subject='TestSub')

    # call forward_email with dummy SMTP details
    forward.forward_email(msg, smtp_server='smtp.example.com', smtp_port=587, smtp_email='me@example.com', smtp_password='pw', forward_to='you@example.com')

    assert sent['server'] == 'smtp.example.com'
    assert sent['port'] == 587
    assert sent['login'] == ('me@example.com', 'pw')
    assert 'you@example.com' in sent['to_addrs']
    assert 'TestSub' in sent['subject']
