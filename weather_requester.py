import os                                           # Importuje bibliotekę os do pracy z zmiennymi środowiskowymi
import json                                         # Importuje bibliotekę do pracy z danymi w formacie JSON
import time                                         # Importuje bibliotekę do zarządzania czasem
import requests                                     # Importuje bibliotekę do wykonywania zapytań HTTP
from datetime import datetime                       # Importuje bibliotekę do pracy z datami i czasami
import pytz                                         # Importuje bibliotekę do pracy z czasami strefowymi
from mqtt_publisher import MQTTPublisher            # Importuje klasę do publikowania wiadomości MQTT

# Pobieranie lokalizacji i danych MQTT ze zmiennych środowiskowych
location = os.getenv("LOCATION", "Wroclaw")                                     # Domyślna lokalizacja: Wroclaw
BROKER_ADDRESS = os.getenv("BROKER_ADDRESS", "test.mosquitto.org")              # Domyślny broker publiczny
BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))                               # Port brokera MQTT (domyślnie 1883)
MQTT_USER = os.getenv("MQTT_USER", None)                                        # Nazwa użytkownika (opcjonalna dla publicznego brokera)
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", None)                                # Hasło (opcjonalne dla publicznego brokera)
STUDENT_ID = os.getenv("STUDENT_ID", "213769")                                  # Unikalny identyfikator studenta
TOPIC = f"{STUDENT_ID}/{location}"                                              # Temat MQTT, np. "261356/Wroclaw"

# Inicjalizacja klienta MQTT
mqtt_publisher = MQTTPublisher(
    broker_address=BROKER_ADDRESS,
    broker_port=BROKER_PORT,
    username=MQTT_USER,
    password=MQTT_PASSWORD,
)


class WeatherRequester:
    def __init__(self, location, mqtt_publisher):
        """
        Inicjalizuje obiekt WeatherRequester z nazwą lokalizacji oraz ustawieniami API.
        """
        self.location = location                         # Lokalizacja dla zapytania pogodowego (np. 'Wroclaw')
        self.mqtt_publisher = mqtt_publisher

        # Buduje URL do API pogodowego z dynamiczną nazwą lokalizacji i kluczem API
        self.api_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{self.location}?unitGroup=metric&key=7M7Z4G9U5ZKS773AJFCY8WNVQ&contentType=json"

    def fetch_weather_data(self):
        """
        Wysyła zapytanie do API pogodowego i zwraca odpowiedź w formacie JSON.
        """
        try:
            print(f"Fetching data from: {self.api_url}")                # Wypisuje URL zapytania na konsolę
            response = requests.get(self.api_url)                       # Wykonuje zapytanie GET do API pogodowego
            response.raise_for_status()                                 # Sprawdza, czy zapytanie zakończyło się sukcesem
            data = response.json()                                      # Parsuje odpowiedź w formacie JSON

            return self.format_data(data)                               # Przekazuje dane do funkcji formatującej
        
        except requests.RequestException as e:                          # Obsługuje błędy podczas zapytania HTTP
            print(f"Error fetching data: {e}")                          # Wypisuje komunikat o błędzie
            return None                                                 # Zwraca None, jeśli zapytanie nie powiodło się

    def format_data(self, api_response):
        """
        Formatuje odpowiedź z API do żądanej struktury JSON.
        """
        try:
            # Wyciąganie danych z "currentConditions" dla pomiarów aktualnej pogody
            current_conditions = api_response.get('currentConditions', {})

            # Wyciągamy konkretne dane (temperatura, opady, wilgotność)
            temperature = current_conditions.get('temp', 'N/A')              # Otrzymujemy temperaturę
            precipitation = current_conditions.get('precip', 'N/A')          # Otrzymujemy opady
            humidity = current_conditions.get('humidity', 'N/A')             # Otrzymujemy wilgotność

            # Tworzymy sformatowaną wiadomość
            formatted_data = {
                "location": self.location,                                                          # Lokalizacja (np. 'Wroclaw')
                "timestamp": datetime.now(pytz.timezone('Europe/Warsaw')).isoformat(),              # Używamy lokalnego czasu
                "values": [
                    {"temperature": temperature if temperature is not None else 'N/A'},             # Upewniamy się, że wartość jest poprawna
                    {"precipitation": precipitation if precipitation is not None else 'N/A'},       # Jeśli brak wartości, ustawiamy 'N/A'
                    {"humidity": humidity if humidity is not None else 'N/A'}                       # Jeśli brak wartości, ustawiamy 'N/A'
                ]
            }

            return formatted_data                                                                    # Zwracamy sformatowane dane

        except (KeyError, IndexError) as e:                  # Obsługuje błędy w trakcie formatowania danych
            print(f"Error formatting data: {e}")             # Wypisuje komunikat o błędzie
            return None                                      # Zwraca None, jeśli nie udało się sformatować danych

    def run(self):
        """
        Pętla, która co 30 sekund odpytuje API i publikuje dane na MQTT.
        """
        while True:
            print("Fetching weather data...")                        # Wypisuje komunikat informujący o pobieraniu danych
            weather_data = self.fetch_weather_data()                 # Pobiera dane pogodowe z API
            if weather_data:                                         # Jeżeli dane zostały pomyślnie pobrane

                # Przekształca dane do formatu JSON i wypisuje na konsolę
                data_to_send = json.dumps(weather_data, indent=4)  
                print(data_to_send)                                     # Wypisuje dane w formacie JSON

                # Publikowanie wiadomości na MQTT
                self.mqtt_publisher.publish_message(TOPIC, data_to_send)

            time.sleep(30)                                              # Czeka 30 sekund przed kolejnym zapytaniem


# Główna część programu
if __name__ == "__main__":
    # Tworzy instancję obiektu WeatherRequester z podaną lokalizacją
    requester = WeatherRequester(location, mqtt_publisher)  
    
    # Uruchamia główną pętlę zapytań o dane pogodowe
    requester.run()
