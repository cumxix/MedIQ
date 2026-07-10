# MedIQ

MedIQ is a Telegram bot that helps users search for medicine information, manage medications, and receive reminders based on their local time zone.

## ✨ Features

- 🔍 Search medicines by brand or generic name
- 📋 View and select from multiple search results
- 💊 Check drug interactions
- ⏰ Set medication reminders
- 🌍 Automatic time zone detection using the user's location
- 📍 Find nearby pharmacies
- 📖 View medicine search history
- 🗑️ Clear medicine search history
- ⭐ Add, view, and remove favorite medicines
- ℹ️ About and Help commands

## 🛠️ Technologies

- Python
- Aiogram
- SQLite
- Telegram Bot API
- TimezoneFinder
- ZoneInfo

## 📂 Project Structure

```text
MedIQ/
├── bot.py
├── handlers.py
├── keyboards.py
├── database.py
├── pharmacy_service.py
├── reminder_service.py
├── config.py
├── requirements.txt
├── medicines.csv
├── data/
│   └── medicine.db
└── README.md
```

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/cumxix/MedIQ.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your Telegram Bot Token:

```env
BOT_TOKEN=your_telegram_bot_token
```

Run the bot:

```bash
python bot.py
```

## 🌍 Time Zone Support

Users can send their location once to detect and save their time zone automatically.

Medication reminders are sent according to each user's local time, allowing MedIQ to support users from different countries.

## 📜 License

This project is for educational purposes.