# -*- coding: utf-8 -*-
import sqlite3, time, datetime, requests, os
from playwright.sync_api import sync_playwright

# # CONFIG PRODUCTION PROTECTED
DB = "rentals.db"
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
LOCATION_ID = "112039062142402"
LOCATION_NAME = "Tamiami"
RADIUS = 25
MIN_PRICE = 1700
MAX_PRICE = 1900
BEDROOMS = 1
BATHROOMS = 1
PROPERTY_TYPES = ["apartment", "house", "condo"]  # Property types to filter

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS listings (id TEXT PRIMARY KEY, title TEXT, price INTEGER, link TEXT, date TEXT)')
    conn.commit()
    conn.close()

def is_new(listing_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT 1 FROM listings WHERE id=?", (listing_id,))
    exists = c.fetchone()
    conn.close()
    return exists is None

def save(listing_id, title, price, link):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO listings VALUES (?,?,?,?,?)", (listing_id, title, price, link, str(datetime.date.today())))
    conn.commit()
    conn.close()

ef search_rentals():
    new_listings = []
    with sync_playwright() as p:
        # 🌐 A MUST FOR RENDER: headless=True
        browser = p.chromium.launch(headless=True, args=["--lang=en-US"])
        if os.path.exists("fb_session.json"):
            context = browser.new_context(storage_state="fb_session.json", locale="en-US")
        else:
            context = browser.new_context(locale="en-US")

        page = context.new_page()

        # Build property type filters: &propertyType[0]=apartment&propertyType[1]=house ...
        _type_params = "".join(f"&propertyType[{i}]={t}" for i, t in enumerate(PROPERTY_TYPES))
        _radius_param = f"&radius={RADIUS}"  
        url = (
            f"https://www.facebook.com/marketplace/{LOCATION_ID}/propertyrentals"
            f"?minPrice={MIN_PRICE}&maxPrice={MAX_PRICE}"
            f"&minBathrooms={BATHROOMS}&minBedrooms={BEDROOMS}"
            f"&exact=true"
            f"{_type_params}"
            f"{_radius_param}"  
        )

        print(f"Navigating to: {url}")
        page.goto(url, timeout=60000)

        # Wait for listings to load
        try:
            page.wait_for_selector('a[href*="/marketplace/item/"]', timeout=20000)
        except:
            print("No listings found, checking page load...")

        try:
            page.get_by_role("button", name="Allow all cookies").click(timeout=4000)
        except Exception:
            try:
                page.get_by_role("button", name="Accept all").click(timeout=1000)
            except Exception:
                pass

        time.sleep(7)
        for _ in range(5):
            page.mouse.wheel(0, 3000)
            time.sleep(2)

        page.wait_for_load_state("networkidle")

        links = page.query_selector_all('a[href*="/marketplace/item/"]')
        for link_tag in links[:40]:
            try:
                link_href = link_tag.get_attribute('href')
                if not link_href: continue
                listing_id = link_href.split('/item/')[1].split('/')[0].split('?')[0]
                card_text = link_tag.inner_text()
                lines = [line.strip() for line in card_text.split('\n') if line.strip()]
                if not lines: continue
                price_txt = next((l for l in lines if '$' in l), None)
                if not price_txt: continue
                price = int(''.join(filter(str.isdigit, price_txt)))
                title = lines[1] if lines[0] == price_txt and len(lineas) > 1 else lines[0]
                location = next((l for l in lines if ", FL" in l), "Location not specified")

                if is_new(listing_id):
                    link_full = "https://facebook.com/marketplace/item/" + listing_id
                    save(listing_id, title, price, link_full)
                    new_listings.append({"title": title, "price": price, "link": link_full, "location": location})
            except Exception:
                continue

        context.storage_state(path="fb_session.json")
        browser.close()
        return new_listings

# PRINCIPAL ENTRY POINT
if __name__ == "__main__":
    print("Starting rental scraper bot...")
    init_db()
    results = search_rentals()
    print(f"Done. New listings found: {len(results)}")
    
    # 📈 SORTING AUTOMATICALLY
    results.sort(key=lambda x: x['price'])
    
    if results:
        msg = f"🏠 *{len(results)} New Rentals - {LOCATION_NAME}*\n"
        msg += f"Filters: ${MIN_PRICE}-${MAX_PRICE} | {BEDROOMS} bd / {BATHROOMS} ba\n\n"
        for r in results[:20]:
            msg += f"💰 *${r['price']}* | 📍 _{r['location']}_\n{r['title']}\n[View on Facebook]({r['link']})\n\n"
        if len(results) > 20:
            _type_params = "".join(f"&propertyType[{i}]={t}" for i, t in enumerate(PROPERTY_TYPES))
            _radius_param = f"&radius={RADIUS}"  
            listing_url = (
                f"https://www.facebook.com/marketplace/{LOCATION_ID}/propertyrentals"
                f"?minPrice={MIN_PRICE}&maxPrice={MAX_PRICE}"
                f"&minBathrooms={BATHROOMS}&minBedrooms={BEDROOMS}"
                f"&exact=true"
                f"{_type_params}"
                f"{_radius_param}"  
            )
            msg += f"...and {len(results)-20} more\n[🔗 View all on Facebook]({listing_url})"
        send_telegram(msg)
    else:
        send_telegram(f"No new rentals today in {LOCATION_NAME} (${MIN_PRICE}-${MAX_PRICE})")
