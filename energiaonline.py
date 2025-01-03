from playwright.sync_api import sync_playwright
import paho.mqtt.client as mqtt
import schedule
import time
import re

def send_to_mqtt(topic, payload):
    """Lähetä tiedot MQTT:llä"""
    client = mqtt.Client()
    client.username_pw_set("mqtt-user", "Salasana")
    client.connect("home_assistant_ip", 1883, 60)  # Korvaa 'home_assistant_ip'
    client.loop_start()
    client.publish(topic, payload)
    client.loop_stop()
    client.disconnect()
    print(f"Tiedot lähetetty MQTT:llä {topic}: {payload}")

def fetch_daily_consumption():
    """Hae energiadata verkkosivulta ja lähetä se MQTT:llä"""
    with sync_playwright() as p:
        # Käynnistä selain
        browser = p.firefox.launch(headless=True, args=["--ignore-certificate-errors"])
        page = browser.new_page(ignore_https_errors=True)

        # Avaa kirjautumissivu
        page.goto("https://energiaonline.turkuenergia.fi/eServices/Online/IndexNoAuth", timeout=60000)

        # Kirjaudu sisään
        page.fill("#emailfield", "KÄYTTÄJÄTUNNUS")  # Käyttäjänimi
        page.fill("#Password", "SALASANA")     # Salasana
        page.click("#loginsubmit", timeout=5000)

        # Navigoi kulutustietosivulle
        page.goto("https://energiaonline.turkuenergia.fi/Reporting/CustomerConsumption?", timeout=60000)

        # Odota, että kulutustiedot latautuvat
        page.wait_for_selector("#calendarIntervalDay", timeout=120000)
        page.click("#calendarIntervalDay", timeout=60000)
        page.wait_for_selector('span:has-text("kulutus")', timeout=60000)

        # Hae kulutuslukema
        daily_consumption = page.locator('span:has-text("kulutus")').text_content().strip()
        print(f"{daily_consumption}")
        cleaned_value = re.search(r"(\d+(\.\d+)?)", daily_consumption).group(1)
        print(cleaned_value)

        # Lähetä tiedot MQTT:llä
        send_to_mqtt("homeassistant/sensor/energia/daily_energy", cleaned_value)

        # Sulje selain
        browser.close()

schedule.every(3).hours.do(fetch_daily_consumption)

# Suorita skripti kolmen tunnin välein
print("Skripti päällä.")
while True:
    schedule.run_pending()
    time.sleep(1)