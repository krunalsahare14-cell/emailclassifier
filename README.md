# 📩 AI Email Classifier & Auto-Routing System  

A complete intelligent solution that automatically classifies incoming emails, identifies the appropriate department based on context, summarizes the content, and forwards messages without manual intervention.

---

## 🔥 Overview  

Organizations face high email traffic daily — manually scanning, understanding & routing each one is slow and error-prone.  
This system solves that by using **LLMs + RAG + parallel processing workers**, making email management **faster, smarter and scalable**.

---

### ✨ Key Features

| Feature | Details |
|--------|---------|
| ⚡ Automated Email Classification | Uses LLMs to detect context and topic |
| 🧠 Sentiment & Priority Detection | Marks emails as urgent/complaint/neutral |
| 🔥 RAG-based Department Mapping | Routes to team using a hierarchical JSON database |
| 📄 Summary Generation | Quick overview added at top of forwarded email |
| 📎 Attachment Parsing | Extracts text from PDF/Docs for better classification |
| 🏭 Distributed Task Queue | Celery + RabbitMQ for mass email processing |
| 🌍 Multilingual Support | Uses translation pipeline for non-English mails |
| 🔁 Feedback + Retraining | Improves accuracy continuously |

---

## 🏗 System Workflow

1. Email received on monitored inbox (IMAP)
2. Content + attachments extracted
3. Task is pushed to distributed workers
4. Text encrypted & sent to processing server
5. LLM classifies + summarizes + detects sentiment
6. Email reconstructed with summary + metadata
7. Auto-forwarded via SMTP to correct team inbox
8. Feedback used for improving future routing

---

## 🧰 Tech Stack

| Component | Technology |
|---|---|
| Language | **Python 3.8+** |
| LLM Runtime | **Ollama** |
| Task Queue | **Celery** |
| Message Broker | **RabbitMQ** |
| UI (Demo) | **Streamlit** |
| Models Used | Qwen / LLaMA / Mixtral (configurable) |

---

## 🔧 Installation

### 1️⃣ Install RabbitMQ

```bash
sudo apt-get install rabbitmq-server
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3:4b
python -m venv .venv
poetry env use python3
poetry install
streamlit run src/app.py

📦 email-classifier
 ┣ 📂 src
 ┃ ┣ 📂 data
 ┃ ┃ ┗ rag.json              # Department hierarchy data
 ┃ ┣ 📂 lib
 ┃ ┃ ┣ summarize.py          # Email summarizer
 ┃ ┃ ┣ forward.py            # Auto email forwarding logic
 ┃ ┃ ┣ tasks.py              # Celery async worker functions
 ┃ ┃ ┗ attachments.py        # Attachment extraction & reading
 ┃ ┗ app.py                  # RAG demo streamlit UI
 ┣ README.md
 ┗ requirements.txt
