import requests

def fetch_weather_data(location):
    url = f'https://api.openaq.org/v1/measurements?city={location}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Sprawdza, czy odpowiedź HTTP jest pozytywna
        data = response.json()  # Zmieniamy odpowiedź na format JSON
        print(data)  # Wypisujemy dane w konsoli, aby sprawdzić strukturę

        # Teraz dostosuj kod, aby odwołać się do odpowiednich danych
        if 'results' in data:
            print("Weather data:", data['results'])
        else:
            print("Brak danych pogodowych w odpowiedzi.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# Przykład wywołania funkcji
location = "London"
fetch_weather_data(location)
