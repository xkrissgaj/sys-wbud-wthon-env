import os
import json
import time
import requests
import paho.mqtt.client as mqtt
from datetime import datetime

class WeatherRequester:
    def __init__(self, location):
        self.location = location
        self.api_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/arctic?unitGroup=metric&key=7M7Z4G9U5ZKS773AJFCY8WNVQ&contentType=json"
        self.mqtt_broker = os.getenv("MQTT_BROKER", "localhost")
        self.mqtt_port = int(os.getenv("MQTT_PORT", 1883))
        self.mqtt_topic = os.getenv("MQTT_TOPIC", "weather/data")

    def fetch_weather_data(self):
        """Fetch weather data from the API."""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            return self.format_data(data)
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def format_data(self, api_response):
        """Format the API response into the required JSON structure."""
        try:
            measurements = api_response['results'][0]['measurements']
            values = [{m['parameter']: m['value']} for m in measurements]
            formatted_data = {
                "location": self.location,
                "timestamp": datetime.utcnow().isoformat(),
                "values": values
            }
            return formatted_data
        except (KeyError, IndexError) as e:
            print(f"Error formatting data: {e}")
            return None

    def send_to_mqtt(self, data):
        """Send formatted data to the MQTT broker."""
        try:
            client = mqtt.Client()
            client.connect(self.mqtt_broker, self.mqtt_port)
            client.publish(self.mqtt_topic, json.dumps(data))
            client.disconnect()
            print(f"Data sent to MQTT: {json.dumps(data)}")
        except Exception as e:
            print(f"Error sending data to MQTT: {e}")

    def run(self):
        """Run the weather data requester loop."""
        while True:
            print("Fetching weather data...")
            weather_data = self.fetch_weather_data()
            if weather_data:
                self.send_to_mqtt(weather_data)
            time.sleep(30)

if __name__ == "__main__":
    location = os.getenv("LOCATION", "arctic")
    requester = WeatherRequester(location)
    requester.run()
