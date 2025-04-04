# 🔗 LinkedIn Auto Connector Bot

This project is a LinkedIn automation tool written in Python using Selenium WebDriver. It searches for people using custom filters and sends connection requests automatically. It runs entirely in Docker using `docker-compose` and Selenium Grid for browser automation.

---

## 📦 Features

- Authenticates and logs into LinkedIn
- Searches users by keywords and location
- Sends connection requests automatically
- Dockerized for portability and easy deployment
- Logs activity to standard output for debugging

---

## 🧰 Prerequisites

- Docker
- Docker Compose

---

## ⚙️ Environment Configuration

Edit the `parameters.py` file and provide your LinkedIn credentials and search configuration:

```python
linkedin_username = "your_email@example.com"
linkedin_password = "your_password"
keywords = "DevOps Engineer"
start_page = 1
till_page = 3
geoUrn = "103644278"  # Example: Iran
```
---
## 🚀 How to Run

### 1. Build and Run the Docker Container

```bash
docker-compose up --build

```
This will:

Build your Python application image

Start Selenium Chrome container

Wait for Selenium to be ready

Launch your LinkedIn bot

### 2. View Logs
```bash
docker logs -f linkedin-bot

```
Logs are flushed in real-time so you can follow activity live.

---
## 🐳 Stop the Services
To stop and remove the running containers, execute:
```bash
docker-compose down
```

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.


