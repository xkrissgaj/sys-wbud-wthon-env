import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")

client = mqtt.Client()
client.on_message = on_message

client.connect("test.mosquitto.org", 1883)
client.subscribe("261356/Wroclaw")

print("Listening for messages on topic '261356/Wroclaw'...")
client.loop_forever()
