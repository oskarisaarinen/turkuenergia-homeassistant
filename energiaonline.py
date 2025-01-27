from playwright.sync_api import sync_playwright
import re
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Yhteys onnistui, statuskoodi: {rc}")

def on_publish(client, userdata, mid):
    print("Viesti lähetetty.")

def send_to_mqtt(topic, payload):
    """Lähetä tiedot MQTT:llä"""
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        client.username_pw_set("mqtt-user", "salasana") #vaihda nämä
        client.connect("192.168.68.113", 1883, 60)
        client.loop_start()
        client.publish(topic, payload, qos=0, retain=False)
        print(f"Tiedot lähetetty MQTT:llä {topic}: {payload}")
    except Exception as e:
        print(f"Virhe MQTT-yhteydessä: {e}")
    finally:
        client.loop_stop()
        client.disconnect()

def fetch_daily_consumption():
    """Hae energiadata verkkosivulta ja lähetä se MQTT:llä"""
    try:
        with sync_playwright() as p:
            # Käynnistä selain ja salli HTTPS-virheiden ohitus
            browser = p.firefox.launch(headless=True, args=["--ignore-certificate-errors"])
            page = browser.new_page(ignore_https_errors=True)

            print("Avaa kirjautumissivu...")
            page.goto("https://energiaonline.turkuenergia.fi/eServices/Online/IndexNoAuth", timeout=60000)

            print("Kirjaudu sisään...")
            page.fill("#emailfield", "kayttajatunnus")  # Käyttäjätunnus
            page.fill("#Password", "salasana")      # Salasana
            page.click("#loginsubmit")
            page.wait_for_timeout(3000)

            print("Navigoi kulutustietosivulle...")
            page.goto("https://energiaonline.turkuenergia.fi/Reporting/CustomerConsumption?", timeout=60000)

            print("Varmista, että päiväkohtainen näkymä on käytössä...")
            page.wait_for_selector("#calendarIntervalDay", timeout=60000)
            page.click("#calendarIntervalDay")
            page.wait_for_timeout(2000)

            selected_period = page.locator("#currentViewInterval").text_content().strip()
            print(f"Valittu jakso: {selected_period}")

            if " - " in selected_period:
                start_date, end_date = selected_period.split(" - ")
                if start_date.strip() != end_date.strip():
                    print("Virhe: Valittuna on useampi päivä!")
                    browser.close()
                    return

            daily_consumption = page.locator('span:has-text("Kulutus:")').text_content().strip()
            print(f"Luettu kulutus: {daily_consumption}")

            cleaned_value = re.search(r"(\d+(\.\d+)?)", daily_consumption).group(1)
            print(f"Päivän kulutus: {cleaned_value} kWh")

            send_to_mqtt("homeassistant/sensor/energia/daily_energy", cleaned_value)

            browser.close()

    except Exception as e:
        print(f"Virhe kulutustietojen haussa: {e}")

fetch_daily_consumption()
