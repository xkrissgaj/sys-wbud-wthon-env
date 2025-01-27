import paho.mqtt.client as mqtt
import json
import os

# Fetch environment variables

# BROKER_ADDRESS = os.getenv("BROKER_ADDRESS", "localhost")
location = os.getenv("LOCATION", "Wroclaw")
BROKER_ADDRESS = os.getenv("BROKER_ADDRESS", "test.mosquitto.org")
BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER", None)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", None)

STUDENT_ID = os.getenv("STUDENT_ID", "213769")
TOPIC = f"{STUDENT_ID}/{location}"
TOPIC_PATTERN = f"{STUDENT_ID}/+"

# Save data to file
def save_data_to_file(student_id, location, data):
    directory = os.getenv("DATA_FOLDER", "./data")
    os.makedirs(directory, exist_ok=True)
    
    file_name = f"{student_id}-{location}.json"
    file_path = os.path.join(directory, file_name)
    
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    
    print(f"Data saved to {file_path}")

# Callback function when message is received
def on_message(client, userdata, message):
    try:
        topic = message.topic
        payload = message.payload.decode("utf-8")
        data = json.loads(payload)
        
        topic_parts = topic.split("/")
        student_id = topic_parts[0]
        location = topic_parts[1]
        
        save_data_to_file(student_id, location, data)

    except Exception as e:
        print(f"Error processing message: {e}")
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")

# Callback function when connection is successful
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker successfully.")
        client.subscribe(TOPIC_PATTERN)
    else:
        print(f"Connection failed, return code {rc}")

# Callback function after message is published
def on_publish(client, userdata, mid):
    print(f"Message published with mid: {mid}")

# Initialize MQTT client
client = mqtt.Client(client_id=None, clean_session=True)

# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Set up authentication if necessary
if MQTT_USER and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

# Connect to the broker
client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

# Start the loop to process incoming messages
print("Listening for messages on all topics...")
client.loop_forever()
