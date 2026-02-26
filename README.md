\# 🚀 Telegram Ads Automation Bot


# 🚀 Telegram Ads Automation Bot

A production-ready Telegram bot for selling digital advertising systems (Google Ads & Meta Ads) with automated PayPal payments and instant PDF delivery.

Built with **Aiogram 3**, **aiohttp**, and deployed on **Railway**.

---

## 💎 Features

- 📘 Sell Google Ads & Meta Ads systems
- 💳 PayPal Checkout (Sandbox / Live)
- 🔐 Automatic payment capture
- 📦 Instant PDF delivery after payment
- 🛡 Anti-duplicate order protection
- ☁️ Railway-ready deployment
- 🧱 Modular structure (handlers / services / keyboards)

---

## 📦 Project Structure


telegram-ads-bot/
│
├── main.py
├── config.py
├── requirements.txt
├── Procfile
├── README.md
├── .gitignore
│
├── handlers/
├── services/
├── keyboards/
├── assets/
└── data/


---

## ⚙️ Environment Variables

Set these in Railway → Variables:


BOT_TOKEN=
PAYPAL_CLIENT_ID=
PAYPAL_SECRET=
PAYPAL_BASE=https://api-m.sandbox.paypal.com

APP_BASE_URL=https://yourproject.up.railway.app


For live payments:


PAYPAL_BASE=https://api-m.paypal.com


---

## 🚀 Deployment (Railway)

1. Push project to GitHub
2. Go to Railway → New Project
3. Deploy from GitHub
4. Add Environment Variables
5. Railway will auto-deploy

Procfile:


web: python main.py


---

## 💳 Payment Flow

1. User selects product
2. PayPal Checkout opens
3. After payment → `/success`
4. Payment captured automatically
5. PDF delivered instantly in Telegram

---

## 🔐 Security Notes

- Never commit `.env`
- Use Railway Variables
- Rotate tokens if exposed
- Consider private repository for premium PDF files

---

## 🧠 Tech Stack

- Python 3.11+
- Aiogram 3
- aiohttp
- PayPal REST API
- Railway hosting

---

## 📜 License

Private commercial project.
Unauthorized redistribution of materials is prohibited.

---

## 👤 Author

Built as a scalable SaaS-style Telegram sales system.