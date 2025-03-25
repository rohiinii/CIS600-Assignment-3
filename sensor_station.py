import paho.mqtt.client as mqtt
import time
import random

# ThingSpeak MQTT configuration
CHANNEL_ID = "2889190"
MQTT_USERNAME = "Kg8zECEOFS4xKh0LIgYWHhY"  # Username (Write API Key)
MQTT_CLIENT_ID = "Kg8zECEOFS4xKh0LIgYWHhY"  # Client ID
MQTT_PASSWORD = "u8Kc3IPPGwtRD7gMwWFILMmT"  # Password
MQTT_BROKER = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_TOPIC = f"channels/{CHANNEL_ID}/publish"

connected = False

# Simulate sensor data
def get_sensor_data():
    return {
        "field1": round(random.uniform(-50, 50), 2),    # Temperature
        "field2": round(random.uniform(0, 100), 2),     # Humidity
        "field3": round(random.uniform(300, 2000), 2)   # CO2
    }

# MQTT connect callback
def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        connected = True
        print("✅ Connected to ThingSpeak MQTT broker")
    else:
        print(f"❌ Connection failed with code {rc}")

# MQTT publish callback
def on_publish(client, userdata, mid):
    print("✅ Data published to ThingSpeak")

# Create client with proper credentials
client = mqtt.Client(client_id=MQTT_CLIENT_ID, protocol=mqtt.MQTTv311, transport="tcp")
client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
client.on_connect = on_connect
client.on_publish = on_publish

print("🔌 Connecting to ThingSpeak MQTT broker...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# Wait for connection before publishing
while not connected:
    print("⏳ Waiting for connection...")
    time.sleep(1)

# Publish data every 15 seconds
while True:
    data = get_sensor_data()
    payload = f"field1={data['field1']}&field2={data['field2']}&field3={data['field3']}"
    print("📤 Publishing:", payload)

    result = client.publish(MQTT_TOPIC, payload)
    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        print("❌ Failed to send data")

    time.sleep(15)
