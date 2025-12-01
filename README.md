#✉️🛡️ AI Email Phishing Detector & Security Email Filter
An intelligent email-security system powered by LLMs, threat-intel scanning & automated workflows.
________________________________________

##🚀 Overview
Modern organizations receive thousands of emails every day, many of which are phishing attempts, scam invoices, or social-engineering attacks.
This system combines:
•	LLM-based phishing detection
•	RAG-driven threat intelligence
•	URL & attachment safety analysis
•	Celery-powered distributed processing
to deliver fast, reliable, automated email security.
The result?
⚡ Stronger zero-trust enforcement
⚡ Faster threat detection
⚡ Reduced human error risk
________________________________________

##✨ Key Features
Feature	Description
🛡️ Automated Phishing Classification	Flags emails as legitimate or phishing
🔥 Threat Level Detection	Rates severity: Low / Medium / High / Critical
📚 RAG-Based Threat Intelligence	Uses JSON patterns to match known attack types
🧠 LLM-Powered Summary	Generates human-readable security summary
📎 Attachment Inspection	Extracts & analyzes PDF / DOCX / images
🔗 Link Reputation Analysis	Detects malicious URLs or suspicious hostname patterns
🏭 Distributed Task Queue	Celery + RabbitMQ for scalable async processing
🌍 Multilingual Detection	Works across languages (English, Hindi, Spanish, etc.)
🔁 Continuous Learning Loop	Improves accuracy with user feedback
________________________________________

##🏗️ System Workflow
Incoming Email (IMAP)
       ↓
Extract Body + Attachments
       ↓
Push Task → Celery Worker Queue
       ↓
Threat Scan (content + links + files)
       ↓
LLM Reasoning → Phishing or Legit
       ↓
Add Summary + Threat Score
       ↓
[If phishing] → Move to Quarantine
[If safe]     → Deliver to Inbox
       ↓
Store Feedback → Improve Model
________________________________________

##🧠 Phishing Signals Detected
✔ Fake identity impersonation (CEO, HR, Bank)
✔ Password reset scams
✔ Fake invoice/payment fraud
✔ Urgent messages (“ACTION REQUIRED”, “LOGIN NOW”)
✔ URL spoofing / malicious redirects
✔ Credential harvesting landing pages
✔ Advance-fee scams
✔ Malware hidden in attachments
________________________________________

##🧰 Tech Stack
Component	Technology
🐍 Language	Python 3.8+
🤖 LLM Runtime	Ollama
📦 Async Queue	Celery
🐇 Message Broker	RabbitMQ
🖥️ UI Demo	Streamlit
🧩 Models	Qwen / LLaMA / Mixtral (configurable)
________________________________________

##🔧 Installation
### Install RabbitMQ
sudo apt-get install rabbitmq-server

### Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

### Pull model
ollama pull qwen3:4b

### Create venv
python -m venv .venv

### Setup poetry
poetry env use python3
poetry install

### Run UI
streamlit run src/app.py
________________________________________

##📦 Project Structure
email-classifier/
 ┣ 📂 src
 ┃ ┣ 📂 data
 ┃ ┃ ┗ rag.json              # Threat patterns + keyword DB
 ┃ ┣ 📂 lib
 ┃ ┃ ┣ summarize.py          # LLM email summarizer
 ┃ ┃ ┣ forward.py            # Quarantine / forwarding logic
 ┃ ┃ ┣ tasks.py              # Celery worker task handlers
 ┃ ┃ ┗ attachments.py        # File text extraction + scanning
 ┃ ┗ app.py                  # Streamlit UI
 ┣ README.md
 ┗ requirements.txt
________________________________________

##🧑‍💻 Future Enhancements
•	🚨 Real-time Gmail & Outlook API integration
•	🛑 Automatic URL sandboxing
•	📊 Admin dashboard for security analytics
•	🎯 Fine-tuned in-house phishing model
•	🔐 DKIM/SPF/DMARC validation
________________________________________

##🤝 Contributions
Pull requests and feature suggestions are welcome!
If you'd like to improve the threat patterns, feel free to update rag.json.
________________________________________

##💬 Support
If you need help setting up the system or modifying the detection logic, feel free to ask!
