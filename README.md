# turkuenergia-energiaonline-homeassistant
Python-skripti, joka hakee energiankulutustietoja Turku Energian energiaonline palvelusta ja päivittää tiedot Home Assistanttin energiasensoriksi MQTT kautta. Sovellettavissa myös helposti muihin vastaaviin palveluihin, joista ei ole avointa API:a saatavilla.

**Asennusohjeet**

**1. Vaatimukset**

  Python 3.10 tai uudempi
  Home Assistant asennettuna, jossa on:
  MQTT-integraatio (esim. Mosquitto broker)

**2. Asenna tarvittavat kirjastot**

  Aja seuraavat komennot:

  pip install playwright paho-mqtt schedule
  playwright install

  playwright: Verkkosivun automatisointiin.
  paho-mqtt: MQTT-viestien lähettämiseen Home Assistantiin.
  schedule: Ajastamaan skripti toistuvasti.

**3. Käyttöönotto**

  Muokkaa seuraavat arvot energiaonline.py -skriptissä:
  Käyttäjänimi ja salasana: energiaonline-tunnukset
  MQTT-palvelimen IP-osoite
  MQTT-käyttäjänimi ja -salasana
  Testaa skriptiä komennolla python3 energiaonline.py

  Tämän jälkeen voit tuoda energiasensorin mqtt.py -skriptin avulla Home Assistanttiin
  
  
