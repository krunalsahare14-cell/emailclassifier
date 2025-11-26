import sys
import types
import pytest


# Provide a harmless dotenv shim for test environments without python-dotenv
if 'dotenv' not in sys.modules:
    _m = types.ModuleType('dotenv')
    _m.load_dotenv = lambda *a, **k: None
    sys.modules['dotenv'] = _m

# shim summarize to avoid importing heavy deps used by src.lib.summarize
if 'src.lib.summarize' not in sys.modules:
    _sm = types.ModuleType('src.lib.summarize')
    _sm.summarize_email = lambda x: 'summary'
    sys.modules['src.lib.summarize'] = _sm


def test_forward_flow_with_fixture(monkeypatch, sample_emails):
    """
    Integration-style test: ensure forwarding logic can be invoked in a CI-safe way.
    We mock network interactions (`smtplib.SMTP`) and the LLM call if present.
    """
    # Lazy import to avoid module-level side effects
    from src.lib import forward

    called = {}

    class DummySMTP:
        def __init__(self, server, port):
            called['server'] = server
            called['port'] = port

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def starttls(self):
            called['starttls'] = True

        def login(self, email, password):
            called['login'] = (email, password)

        def send_message(self, msg, to_addrs=None):
            called['to_addrs'] = to_addrs
            called['subject'] = msg['Subject']

    monkeypatch.setattr('src.lib.forward.smtplib.SMTP', DummySMTP)
    monkeypatch.setattr('src.lib.forward.summarize_email', lambda x: 'summary')

    # construct a minimal email message object
    from email.message import EmailMessage

    subj, _ = sample_emails[0]
    msg = EmailMessage()
    msg['Subject'] = subj
    msg.set_content('body')

    forward.forward_email(msg, smtp_server='smtp.local', smtp_port=25, smtp_email='s@example.com', smtp_password='pw', forward_to='r@example.com')

    assert called.get('server') == 'smtp.local'
    assert 'r@example.com' in called.get('to_addrs', [])
