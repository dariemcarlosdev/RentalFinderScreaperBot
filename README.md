# RentalFinderScreaperBot

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![Telegram](https://img.shields.io/badge/Telegram-Integrated-2CA5E0)
![AI Automation](https://img.shields.io/badge/AI-Automation-purple)

RentalFinderScreaperBot is a small Python automation project that uses AI-assisted workflows to help streamline the process of finding rental listings, collect relevant property information, and support notifications through Telegram integration for faster review.

## ✨ Features

- Automates parts of the rental listing search workflow
- Helps collect and organize relevant rental information
- Supports Telegram integration for notifications and updates
- Built in Python for simple customization and extension
- Supports AI-assisted automation use cases

## ⚙️ Requirements

- Python 3.10 or newer
- pip
- Internet connection
- Telegram bot credentials for integration features
- Any project-specific dependencies listed in `requirements.txt`

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dariemcarlosdev/RentalFinderScreaperBot.git
   ```

2. Go to the project folder:

   ```bash
   cd RentalFinderScreaperBot
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   ```

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

   On macOS/Linux:

   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## 🔐 Environment Variables

Create a `.env` file in the project root and define the variables required by your bot.

Example:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
OPENAI_API_KEY=your_openai_api_key
```

> Add or remove variables depending on the services used by your project.

## 🤖 Telegram Setup Guide

1. Open Telegram and search for **@BotFather**.
2. Create a new bot using the `/newbot` command.
3. Copy the bot token provided by BotFather.
4. Add the token to your `.env` file as `TELEGRAM_BOT_TOKEN`.
5. Start a chat with your bot.
6. Get your Telegram chat ID and set it in `.env` as `TELEGRAM_CHAT_ID`.
7. Run the bot and verify that notifications are delivered correctly.

## ▶️ Usage

1. Make sure your virtual environment is activated.
2. Configure any required environment variables, API keys, or Telegram bot credentials.
3. Run the main Python script for the bot.
4. Receive or send updates through your Telegram integration workflow.

Example:

```bash
python main.py
```

> Replace `main.py` with the actual entry-point script used in this project.

## 🖼️ Screenshots

Add screenshots here to show the bot in action, such as:

- Telegram notifications
- Rental listing results
- Console output

Example placeholder:

```md
![App Screenshot](docs/screenshot.png)
```

## 👨‍💻 Creator

Created by **Dariem Carlos Macias Mora**.
