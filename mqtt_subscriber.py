import paho.mqtt.client as mqtt
import json
import os

# Pobieranie danych z zmiennych środowiskowych
#BROKER_ADDRESS = os.getenv("BROKER_ADDRESS", "localhost")
#BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))
#MQTT_USER = os.getenv("MQTT_USER", "user")
#MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "password")
#TOPIC_PATTERN = "#"


# Pobieranie danych z zmiennych środowiskowych
location = os.getenv("LOCATION", "Wroclaw")                                     # Domyślna lokalizacja: Wroclaw
BROKER_ADDRESS = os.getenv("BROKER_ADDRESS", "test.mosquitto.org")              # Domyślny broker publiczny
BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))                               # Port brokera MQTT (domyślnie 1883)
MQTT_USER = os.getenv("MQTT_USER", None)                                        # Nazwa użytkownika (opcjonalna dla publicznego brokera)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", None)                                # Hasło (opcjonalne dla publicznego brokera)
STUDENT_ID = os.getenv("STUDENT_ID", "213769")                                  # Unikalny identyfikator studenta
TOPIC = f"{STUDENT_ID}/{location}"                                              # Temat MQTT, np. "261356/Wroclaw"
TOPIC_PATTERN = "#"                                                             # Subskrypcja wszystkich tematów

# Funkcja zapisująca dane do pliku
def save_data_to_file(student_id, location, data):
    # Ścieżka do folderu danych
    directory = os.getenv("DATA_FOLDER", "./data")
    os.makedirs(directory, exist_ok=True)
    
    # Tworzenie nazwy pliku na podstawie student_id i location
    file_name = f"{student_id}-{location}.json"
    file_path = os.path.join(directory, file_name)
    
    # Sprawdzanie, czy plik istnieje i aktualizacja danych
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            existing_data = json.load(f)
            if isinstance(existing_data, list):
                existing_data.append(data)
            else:
                existing_data = [existing_data, data]
    else:
        existing_data = [data]
    
    # Zapis danych do pliku JSON
    with open(file_path, "w") as f:
        json.dump(existing_data, f, indent=4)
    
    print(f"Data saved to {file_path}")

# Funkcja obsługująca odebrane wiadomości
def on_message(client, userdata, message):
    try:
        # Dekodowanie wiadomości JSON
        payload = message.payload.decode()
        data = json.loads(payload)
        
        # Wypisanie wiadomości na konsolę
        print(f"Received message: {payload} on topic {message.topic}")
        
        # Zapisanie danych do pliku
        save_data_to_file(STUDENT_ID, location, data)
    
    except Exception as e:
        print(f"Error processing message: {e}")

# Ustawienie klienta MQTT
client = mqtt.Client()

# Rejestracja funkcji callback na odebrane wiadomości
client.on_message = on_message

# Połączenie z brokerem MQTT
if MQTT_USER and MQTT_PASSWORD:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

client.connect(BROKER_ADDRESS, BROKER_PORT)

# Subskrypcja tematów (w tym wildcard #)
client.subscribe(TOPIC_PATTERN)
print(f"Listening for messages on topic '{TOPIC_PATTERN}'...")

# Uruchomienie pętli nasłuchującej
client.loop_forever()
