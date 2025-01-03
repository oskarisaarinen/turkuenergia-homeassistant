import json
import paho.mqtt.client as mqtt

def send_mqtt_discovery():
    client = mqtt.Client()
    client.username_pw_set("mqttuser", "mqttpassword")  # Korvaa nämä
    client.connect("home_assistant_ip", 1883, 60) # Korvaa nämä

    discovery_topic = "homeassistant/sensor/daily_energy/config"
    discovery_payload = {
        "name": "Päivittäinen Kulutus",
        "state_topic": "homeassistant/sensor/energia/daily_energy",
        "unit_of_measurement": "kWh",
        "value_template": "{{ value | float }}",
        "device_class": "energy",               # Määrittää sensorin energialuokaksi
        "state_class": "total_increasing"      # Pakollinen energiadatalle
    }

    client.publish(discovery_topic, json.dumps(discovery_payload))
    client.disconnect()
    print("MQTT Discovery -viesti lähetetty.")