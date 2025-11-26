import pytest

from src import llm


def test_return_ans_fallback():
	try:
		ans = llm.return_ans("Please classify: test message")
	except Exception as e:
		pytest.fail(f"llm.return_ans raised unexpectedly: {e}")

	assert isinstance(ans, str)
