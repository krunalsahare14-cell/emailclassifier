# ✉️🛡️ AI Email Phishing Detector & Security Email Filter
### _An intelligent email-security system powered by LLMs, threat-intel scanning & automated workflows._

## 🚀 Overview
Modern organizations receive thousands of emails daily, many containing phishing, malware, or credential‑harvesting attempts.

This system integrates:
- LLM-based phishing detection
- RAG-powered threat intelligence
- URL & attachment scanning
- Celery asynchronous processing

## ✨ Key Features
- Automated Phishing Classification
- Threat Level Analysis
- RAG Threat Intelligence
- LLM Summary Generation
- Attachment Inspection
- URL Reputation Check
- Distributed Processing
- Multilingual Support
- Feedback Learning

## 🏗️ System Workflow
Incoming Email → Extract → Celery Queue → Threat Scan → LLM Output → Summary → Quarantine/Deliver → Feedback Store.

## 🧠 Phishing Signals Detected
Identity impersonation, fake password resets, invoice scams, urgency messages, malicious URLs, harvesting pages, malware attachments.

## 🧰 Tech Stack
Python, Ollama, Celery, RabbitMQ, Streamlit, Qwen/LLaMA/Mixtral models.

## 🔧 Installation
sudo apt-get install rabbitmq-server
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3:4b
python -m venv .venv
poetry install
streamlit run src/app.py

## 📦 Project Structure
email-classifier/
  src/
    data/rag.json
    lib/
      summarize.py
      forward.py
      tasks.py
      attachments.py
    app.py
  README.md
  requirements.txt
________________________________________

## 🧑‍💻 Future Enhancements
•	🚨 Real-time Gmail & Outlook API integration
•	🛑 Automatic URL sandboxing
•	📊 Admin dashboard for security analytics
•	🎯 Fine-tuned in-house phishing model
•	🔐 DKIM/SPF/DMARC validation
________________________________________

## 🤝 Contributions
Pull requests and feature suggestions are welcome!
If you'd like to improve the threat patterns, feel free to update rag.json.
________________________________________

## 💬 Support
If you need help setting up the system or modifying the detection logic, feel free to ask!
________________________________________
## Deployment

This application is deployed using **Streamlit Cloud**.

### How it works
- Monitors Gmail inbox using IMAP
- Extracts unread emails
- Applies a phishing detection classifier
- Displays classification results in real time

### Security Note
This app uses **Gmail App Passwords** only.
Credentials are not stored and are used only for the active session.

