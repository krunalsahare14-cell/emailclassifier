import pytest
from email.message import EmailMessage

from src.lib.info import get_email_body, RAWEmail


def test_sample_emails_fixture(sample_emails):
	assert isinstance(sample_emails, list)
	assert len(sample_emails) == 3
	subj, label = sample_emails[0]
	assert subj == "WIN CASH NOW"
	assert label == "spam"


def _make_plain_message(text: str) -> EmailMessage:
	msg = EmailMessage()
	msg.set_content(text)
	msg['From'] = 'alice@example.com'
	msg['To'] = 'bob@example.com'
	msg['Subject'] = 'Test'
	return msg


def test_get_email_body_plain():
	msg = _make_plain_message("hello world")
	body = get_email_body(msg)
	assert isinstance(body, str)
	assert "hello" in body


def test_RAWEmail_returns_string():
	msg = _make_plain_message("hi")
	raw = RAWEmail(msg)
	assert isinstance(raw, str)
	assert "Subject" in raw
