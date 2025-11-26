import sys
import os
import pytest

@pytest.fixture
def sample_emails():
	return [
		("WIN CASH NOW", "spam"),
		("Meeting at 3PM", "ham"),
		("URGENT: server down", "important"),
	]
    
# Ensure repository root is on sys.path so tests can import `src` on CI
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
	sys.path.insert(0, ROOT)
