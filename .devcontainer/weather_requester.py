import os  # Importuje bibliotekę os do pracy z zmiennymi środowiskowymi
import json  # Importuje bibliotekę do pracy z danymi w formacie JSON
import time  # Importuje bibliotekę do zarządzania czasem
import requests  # Importuje bibliotekę do wykonywania zapytań HTTP
from datetime import datetime  # Importuje bibliotekę do pracy z datami i czasami
import pytz  # Importuje bibliotekę do pracy z czasami strefowymi


class WeatherRequester:
    def __init__(self, location):
        """
        Inicjalizuje obiekt WeatherRequester z nazwą lokalizacji oraz ustawieniami API.
        """
        self.location = location  # Lokalizacja dla zapytania pogodowego (np. 'Wroclaw')
        
        # Buduje URL do API pogodowego z dynamiczną nazwą lokalizacji i kluczem API
        self.api_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{self.location}?unitGroup=metric&key=7M7Z4G9U5ZKS773AJFCY8WNVQ&contentType=json"

    def fetch_weather_data(self):
        """
        Wysyła zapytanie do API pogodowego i zwraca odpowiedź w formacie JSON.
        """
        try:
            print(f"Fetching data from: {self.api_url}")  # Wypisuje URL zapytania na konsolę
            response = requests.get(self.api_url)  # Wykonuje zapytanie GET do API pogodowego
            response.raise_for_status()  # Sprawdza, czy zapytanie zakończyło się sukcesem
            data = response.json()  # Parsuje odpowiedź w formacie JSON

            # Drukujemy odpowiedź API, aby zobaczyć, jaka jest struktura
            # print(json.dumps(data, indent=4))  # Drukowanie całej odpowiedzi w formacie JSON

            return self.format_data(data)  # Przekazuje dane do funkcji formatującej
        
        except requests.RequestException as e:  # Obsługuje błędy podczas zapytania HTTP
            print(f"Error fetching data: {e}")  # Wypisuje komunikat o błędzie
            return None  # Zwraca None, jeśli zapytanie nie powiodło się

    def format_data(self, api_response):
        """
        Formatuje odpowiedź z API do żądanej struktury JSON.
        """
        try:
            
            # Sprawdzamy, czy odpowiedź zawiera dane dla lokalizacji
            location_data = api_response.get('locations', {}).get(self.location, {})

            # Wyciąganie danych z "currentConditions" dla pomiarów aktualnej pogody
            current_conditions = api_response.get('currentConditions', {})

            # Wyciągamy konkretne dane (temperatura, opady, wilgotność)
            temperature = current_conditions.get('temp', 'N/A')  # Otrzymujemy temperaturę
            precipitation = current_conditions.get('precip', 'N/A')  # Otrzymujemy opady
            humidity = current_conditions.get('humidity', 'N/A')  # Otrzymujemy wilgotność

            # Tworzymy sformatowaną wiadomość
            formatted_data = {
                "location": self.location,  # Lokalizacja (np. 'Wroclaw')
                "timestamp": datetime.now(pytz.timezone('Europe/Warsaw')).isoformat(),  # Używamy lokalnego czasu
                "values": [
                    {"temperature": temperature if temperature is not None else 'N/A'},  # Upewniamy się, że wartość jest poprawna
                    {"precipitation": precipitation if precipitation is not None else 'N/A'},  # Jeśli brak wartości, ustawiamy 'N/A'
                    {"humidity": humidity if humidity is not None else 'N/A'}  # Jeśli brak wartości, ustawiamy 'N/A'
                ]
            }

            return formatted_data  # Zwracamy sformatowane dane

        except (KeyError, IndexError) as e:  # Obsługuje błędy w trakcie formatowania danych
            print(f"Error formatting data: {e}")  # Wypisuje komunikat o błędzie
            return None  # Zwraca None, jeśli nie udało się sformatować danych


    def run(self):
        """
        Pętla, która co 30 sekund odpytuje API i wypisuje dane na konsolę.
        """
        while True:
            print("Fetching weather data...")  # Wypisuje komunikat informujący o pobieraniu danych
            weather_data = self.fetch_weather_data()  # Pobiera dane pogodowe z API
            if weather_data:  # Jeżeli dane zostały pomyślnie pobrane
                # Przekształca dane do formatu JSON i wypisuje na konsolę
                data_to_send = json.dumps(weather_data, indent=4)  
                print(data_to_send)  # Wypisuje dane w formacie JSON
            time.sleep(30)  # Czeka 30 sekund przed kolejnym zapytaniem


# Główna część programu
if __name__ == "__main__":
    # Odczytuje nazwę lokalizacji z zmiennych środowiskowych (domyślnie 'Wroclaw')
    location = os.getenv("LOCATION", "Wroclaw")
    
    # Tworzy instancję obiektu WeatherRequester z podaną lokalizacją
    requester = WeatherRequester(location)
    
    # Uruchamia główną pętlę zapytań o dane pogodowe
    requester.run()
