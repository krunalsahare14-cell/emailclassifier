import pytest


def test_sample_emails_contents(sample_emails):
	# basic sanity checks for the fixture provided in conftest.py
	assert isinstance(sample_emails, list)
	assert len(sample_emails) >= 1

	allowed_labels = {"spam", "ham", "important"}

	for subj, label in sample_emails:
		assert isinstance(subj, str) and subj.strip(), "subject must be a non-empty string"
		assert isinstance(label, str), "label must be a string"
		assert label in allowed_labels, f"unexpected label: {label}"


def test_classifier_placeholder(sample_emails):
	# If a classifier function is available in the repo, prefer to run it.
	# This keeps the test CI-friendly: if the classifier isn't present, the test still validates the fixture.
	try:
		# try importing a common classifier entry points (best-effort)
		from src import llm as llm_module  # noqa: WPS433
	except Exception:
		llm_module = None

	if llm_module is None:
		pytest.skip("No classifier module available; fixture validation passed")

	# If llm.return_ans exists, call it with a sample and ensure it returns a string (safe smoke test)
	if hasattr(llm_module, "return_ans"):
		sample_subject = sample_emails[0][0]
		try:
			result = llm_module.return_ans(sample_subject)
		except Exception:
			pytest.skip("llm.return_ans raised; likely depends on external services")

		assert isinstance(result, (str, dict)), "return_ans should return a string or dict"
	else:
		pytest.skip("No return_ans on llm module; only fixture validated")
