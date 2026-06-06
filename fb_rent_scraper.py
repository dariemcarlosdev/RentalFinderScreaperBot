import sqlite3, time, datetime, requests, os
from playwright.sync_api import sync_playwright

# CONFIG
DB = "rentas.db"
TOKEN = "8828207901:AAGLALCvQ0lagsrl7m6qcDfiIWXruiL2Xsw" 
CHAT_ID = "6456127410"
LOCATION = "miami"
RADIUS = 25
MIN_PRICE = 1200
MAX_PRICE = 1900
BEDROOMS = 1

def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Error Telegram: {e}")

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS listings (id TEXT PRIMARY KEY, titulo TEXT, precio INTEGER, link TEXT, fecha TEXT)')
    conn.commit()
    conn.close()

def es_nuevo(listing_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT 1 FROM listings WHERE id=?", (listing_id,))
    existe = c.fetchone()
    conn.close()
    return existe is None

def guardar(listing_id, titulo, precio, link):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO listings VALUES (?,?,?,?,?)", (listing_id, titulo, precio, link, str(datetime.date.today())))
    conn.commit()
    conn.close()

def buscar_rentas():
    nuevos = []
    with sync_playwright() as p:
        # Esta es la línea que faltaba. Abre el navegador (headless=False para que lo veas la primera vez)
        browser = p.chromium.launch(headless=True, args=["--lang=es-ES"])
        
        # Validamos si el archivo de sesión ya existe
        if os.path.exists("fb_session.json"):
            context = browser.new_context(storage_state="fb_session.json", locale="es-ES")
        else:
            context = browser.new_context(locale="es-ES")
            
        page = context.new_page()
        
        url = f"https://www.facebook.com/marketplace/{LOCATION}/propertyrentals?radius={RADIUS}&minPrice={MIN_PRICE}&maxPrice={MAX_PRICE}&bedrooms={BEDROOMS}"
        page.goto(url, timeout=60000)
        time.sleep(5)
        
        for _ in range(6):
            page.mouse.wheel(0, 4000)
            time.sleep(2.5)
            
        cards = page.query_selector_all('div[aria-label="Collection of Marketplace items"] > div > div > div')
        
        for card in cards[:40]: # límite para no baneo
            try:
                a_tag = card.query_selector('a[href*="/marketplace/item/"]')
                if not a_tag:
                    continue
                link = a_tag.get_attribute('href')
                listing_id = link.split('/item/')[1].split('/')[0].split('?')[0]
                
                precio_txt = card.query_selector('span[aria-label]').inner_text()
                precio = int(''.join(filter(str.isdigit, precio_txt)))
                titulo = card.query_selector('span[dir="auto"]').inner_text()
                
                if es_nuevo(listing_id):
                    link_full = "https://facebook.com" + link
                    guardar(listing_id, titulo, precio, link_full)
                    nuevos.append({"titulo": titulo, "precio": precio, "link": link_full})
            except:
                continue
                
        context.storage_state(path="fb_session.json")
        browser.close()
        return nuevos

if __name__ == "__main__":
    init_db()
    nuevos = buscar_rentas()
    
if __name__ == "__main__":
    init_db()
    nuevos = buscar_rentas()
    
    if nuevos:
        # Ahora el mensaje reflejará exactamente tus variables de configuración
        msg = f"🏠 *{len(nuevos)} Rentas nuevas - {LOCATION.capitalize()}*\n"
        msg += f"Filtros: ${MIN_PRICE}-${MAX_PRICE} | {BEDROOMS} cuarto(s) | {RADIUS} millas\n\n"
        
        for r in nuevos[:8]:
            msg += f"💰 *${r['precio']}*\n{r['titulo']}\n[Ver en Facebook]({r['link']})\n\n"
            
        if len(nuevos) > 8:
            msg += f"...y {len(nuevos)-8} más"
        enviar_telegram(msg)
    else:
        enviar_telegram(f"✅ Sin rentas nuevas hoy en {LOCATION.capitalize()} (${MIN_PRICE}-${MAX_PRICE})")
