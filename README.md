📩 AI Email Phishing Detector & Security Email Filter

An intelligent security system that automatically scans incoming emails, detects phishing, evaluates risk, summarizes the message, and flags suspicious communications — reducing exposure to social-engineering threats.

🔥 Overview

Organizations receive thousands of emails daily — many of which attempt to trick employees into clicking malicious links or sharing credentials.
This system leverages LLMs + contextual security scanning + attachment inspection to automatically detect phishing and malicious content.

The result: significantly increased email security, zero trust enforcement, faster threat detection.

✨ Key Features
Feature	Details
🛡 Automated Phishing Classification	Identifies phishing/legitimate emails
🧠 Threat Level Detection	Rates severity (low / medium / high / critical)
🔍 RAG-based Threat Intelligence	Uses JSON threat pattern database
📄 Summary Generation	Adds high-level description for security awareness
📎 Attachment Inspection	Extracts & analyzes PDFs / docs / images
🕵🏻‍♂️ Link Reputation Analysis	Searches for malicious URLs & patterns
🏭 Distributed Task Queue	Celery + RabbitMQ for scalable processing
🌍 Multilingual Support	Can detect phishing regardless of language
🔁 Feedback Learning	System improves detection over time
🏗 System Workflow

Email received from monitored inbox (IMAP)

Body text & attachments extracted

Email task pushed to worker queue

Content is scanned for threat indicators

LLM determines: phishing or legitimate

Summary + threat annotations added

If phishing → moved to quarantine mailbox

If legitimate → delivered normally

Feedback stored for further model improvement

🧠 What phishing signals does it detect?

Fake identity impersonation (CEO / HR / Bank)

Password reset scams

Fake invoice / payment fraud

Urgent scare messaging (“ACTION REQUIRED”)

Fraudulent links

Credential harvesting

Scam business proposals

Malware-infested attachments

🧰 Tech Stack
Component	Technology
Language	Python 3.8+
LLM Runtime	Ollama
Task Queue	Celery
Broker	RabbitMQ
UI Demo	Streamlit
Models	Qwen / LLaMA / Mixtral (configurable)
🔧 Installation
sudo apt-get install rabbitmq-server
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3:4b
python -m venv .venv
poetry env use python3
poetry install
streamlit run src/app.py

📦 Project Structure
email-classifier
 ┣ 📂 src
 ┃ ┣ 📂 data
 ┃ ┃ ┗ rag.json              # Threat patterns + keyword data
 ┃ ┣ 📂 lib
 ┃ ┃ ┣ summarize.py          # Email summarizer
 ┃ ┃ ┣ forward.py            # Mail quarantine/forwarding logic
 ┃ ┃ ┣ tasks.py              # Celery async worker functions
 ┃ ┃ ┗ attachments.py        # Attachment scanning & text extraction
 ┃ ┗ app.py                  # Streamlit UI for testing detections
 ┣ README.md
 ┗ requirements.txt