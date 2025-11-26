import pytest

@pytest.fixture
def sample_emails():
	return [
		("WIN CASH NOW", "spam"),
		("Meeting at 3PM", "ham"),
		("URGENT: server down", "important"),
	]
