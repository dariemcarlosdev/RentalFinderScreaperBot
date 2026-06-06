# RentalFinderScreaperBot

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![Telegram](https://img.shields.io/badge/Telegram-Integrated-2CA5E0)
![Render](https://img.shields.io/badge/Deploy-Render-46E3B7)
![Playwright](https://img.shields.io/badge/Browser-Playwright-orange)

RentalFinderScreaperBot is a Python automation bot that searches Facebook Marketplace rental listings, stores newly discovered listings in SQLite, and sends Telegram notifications with matching results.

## ✨ Features

- Scrapes Facebook Marketplace property rental listings with Playwright
- Filters listings by location, radius, min/max price, bedrooms, bathrooms, and property type
- Stores seen listings in `rentals.db` to avoid duplicate notifications
- Sends Telegram alerts for new listings
- Saves and reuses Facebook session state with `fb_session.json`
- Automatically sorts results by price before sending alerts
- Supports deployment on Render

## 📁 Main File

- `fb_rent_scraper.py` — main scraper, database handling, and Telegram notification logic

## ⚙️ Requirements

- Python 3.10+
- pip
- A Telegram bot token
- A Telegram chat ID
- Internet connection
- Render account (for cloud deployment)
- Playwright Chromium browser

## 🚀 Local Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/dariemcarlosdev/RentalFinderScreaperBot.git
   ```

2. Enter the project folder:

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

4. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Install Playwright Chromium:

   ```bash
   playwright install chromium
   ```

## 🔐 Environment Variables

The script reads its configuration from environment variables.

Required by the current scraper code:

```env
TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
```

Optional / deployment-related variables for Render:

```env
PYTHON_VERSION=3.10.0
PLAYWRIGHT_BROWSERS_PATH=/opt/render/.cache/ms-playwright
```

> Important: the current `fb_rent_scraper.py` uses `TOKEN` and `CHAT_ID`.
> If your Render service currently uses `TELEGRAM_TOKEN` or `TELEGRAM_CHAT_ID`, update either the code or the Render environment variables so the names match exactly.

## 🤖 Telegram Setup

1. Open Telegram and search for **@BotFather**.
2. Run `/newbot` and create your bot.
3. Copy the bot token.
4. Add it as the `TOKEN` environment variable.
5. Start a chat with your bot.
6. Get your personal or group chat ID.
7. Add it as the `CHAT_ID` environment variable.

## ▶️ Usage

Run the scraper locally:

```bash
python fb_rent_scraper.py
```

What the script does:

- Initializes `rentals.db`
- Opens Facebook Marketplace rentals for the configured area
- Applies filters from the constants in `fb_rent_scraper.py`
- Collects listing links, title, price, and location
- Saves unseen listings to SQLite
- Sends a Telegram summary of new listings

## 🧩 Current Search Filters in `fb_rent_scraper.py`

These values are currently hardcoded in the script:

- `LOCATION_ID = "112039062142402"`
- `LOCATION_NAME = "Tamiami"`
- `RADIUS = 25`
- `MIN_PRICE = 1700`
- `MAX_PRICE = 1900`
- `BEDROOMS = 1`
- `BATHROOMS = 1`
- `PROPERTY_TYPES = ["apartment", "house", "condo"]`

If you want to monitor a different market, update these values in `fb_rent_scraper.py`.

## ☁️ Deploy to Render

This project can be deployed on **Render** as a Background Worker or Cron Job.

### Recommended Render service type

Use one of these:

- **Cron Job** — best if you want the scraper to run on a schedule
- **Background Worker** — best if you manage execution continuously yourself

For most rental monitoring setups, **Cron Job** is the better choice.

### Render Build Command

Use a build command similar to:

```bash
pip install -r requirements.txt && playwright install chromium
```

### Render Start Command

Use this start command:

```bash
python fb_rent_scraper.py
```

### Render Environment Variables

In Render, open your service and go to **Environment Variables**.
Configure these keys:

```env
CHAT_ID=your_telegram_chat_id
TOKEN=your_telegram_bot_token
PYTHON_VERSION=3.10.0
PLAYWRIGHT_BROWSERS_PATH=/opt/render/.cache/ms-playwright
```

#### Variable notes

- `TOKEN`: Telegram bot token used to send messages
- `CHAT_ID`: Telegram user or group chat ID that receives alerts
- `PYTHON_VERSION`: Python runtime version for Render
- `PLAYWRIGHT_BROWSERS_PATH`: path where Playwright browsers are cached on Render

> Keep secret values private. Do not commit them to the repository.

## 🛠 Render Deployment Steps

1. Push your latest code to GitHub.
2. Log in to Render.
3. Create a new **Cron Job** or **Background Worker**.
4. Connect the GitHub repository: `dariemcarlosdev/RentalFinderScreaperBot`.
5. Set the build command:

   ```bash
   pip install -r requirements.txt && playwright install chromium
   ```

6. Set the start command:

   ```bash
   python fb_rent_scraper.py
   ```

7. Add the environment variables:
   - `TOKEN`
   - `CHAT_ID`
   - `PYTHON_VERSION`
   - `PLAYWRIGHT_BROWSERS_PATH`
8. Deploy the service.
9. Check logs to verify the bot launches correctly and Telegram messages are delivered.

## 🗃️ Generated Files

During execution, the project may create:

- `rentals.db` — local SQLite database of seen listings
- `fb_session.json` — saved Facebook session state for reuse

If deploying to Render, remember that the filesystem may be ephemeral depending on service configuration. If the instance is recreated, these files may be lost unless you attach persistent storage or redesign persistence.

## ⚠️ Notes

- Facebook Marketplace page structure can change and may break selectors.
- The script depends on Playwright and Chromium being available.
- If Facebook requires login, `fb_session.json` may need to be created and refreshed.
- The code currently installs Chromium automatically if it is missing.

## 👨‍💻 Creator

Created by **Dariem Carlos Macias Mora**.
