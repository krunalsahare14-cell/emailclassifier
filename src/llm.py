
from typing import List
import re


def _extract_urls(text: str) -> List[str]:
    # Match http/https URLs; avoid unbalanced quoting by escaping the double-quote
    # character inside the character class.
    return re.findall(r"https?://[^\s)'\"]+", text or "")


def _score_phishing(text: str) -> int:
    """Return a simple score indicating how phishing-like `text` is.

    This is a lightweight heuristic classifier that looks for suspicious
    keywords, urgent language, and presence of URLs. It intentionally avoids
    any heavy external dependencies so the app can run in minimal environments.
    """
    if not text:
        return 0
    t = text.lower()
    score = 0

    # Strong indicators
    strong = [
        "verify your account",
        "update your account",
        "suspended",
        "unauthorized",
        "provide your password",
        "enter your password",
        "verify your identity",
        "confirm your identity",
        "security alert",
        "account locked",
    ]
    for s in strong:
        if s in t:
            score += 3

    # Medium indicators
    medium = [
        "click here",
        "login",
        "password",
        "credentials",
        "urgent",
        "immediately",
        "verify",
        "confirm",
        "update",
        "bank",
        "social security",
        "ssn",
    ]
    for s in medium:
        if s in t:
            score += 1

    # URLs are often present in phishing; suspicious subdomains/phrases add weight
    urls = _extract_urls(text)
    if urls:
        score += 2
        for u in urls:
            if any(x in u.lower() for x in ("security-", "verify-", "login-", "account-")):
                score += 2
            # very short or obviously odd-looking hosts
            host = re.sub(r"https?://", "", u).split("/")[0]
            if re.search(r"\d{3,}", host):
                score += 1

    # Greeting patterns often used: 'dear customer' etc.
    if re.search(r"dear (customer|user|client)|dear sir", t):
        score += 1

    # If message is very short and contains many indicators, bias towards phishing
    if len(t) < 100 and score >= 2:
        score += 1

    return score


def return_ans(query: str) -> str:
    """Return a lightweight phishing classification for `query`.

    Outputs are simple strings: "phishing" or "not phishing".
    This function uses a fast heuristic and does not require haystack/PyTorch.
    """
    try:
        score = _score_phishing(query or "")
        # Threshold chosen conservatively: 3+ indicates likely phishing
        return "phishing" if score >= 3 else "not phishing"
    except Exception as e:
        # On any unexpected error, default to not phishing to avoid false
        # positives that could block legitimate messages in the UI.
        print("llm.return_ans heuristic error:", e)
        return "not phishing"

def test_output():
    content = '''
    Dear customer, your bank account has been suspended due to unusual activity.
    Please update your credentials immediately using the link below:
    https://barclays.security-verify-login.com/update
    Failure to comply in 24 hours will result in access termination.
    '''

    print("RESULT:", return_ans(content))


if __name__ == "__main__":
    test_output()
#         rag_pipeline.connect("prompt_builder", "llm")
