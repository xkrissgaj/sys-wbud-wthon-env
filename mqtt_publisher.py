#import paho.mqtt.client as mqtt

# Pobieranie danych z zmiennych środowiskowych
#location = os.getenv("LOCATION", "Wroclaw")                                     # Domyślna lokalizacja: Wroclaw
#BROKER_ADDRESS = os.getenv("BROKER_ADDRESS", "test.mosquitto.org")              # Domyślny broker publiczny
##BROKER_PORT = int(os.getenv("BROKER_PORT", 1883))                               # Port brokera MQTT (domyślnie 1883)
#MQTT_USER = os.getenv("MQTT_USER", None)                                        # Nazwa użytkownika (opcjonalna dla publicznego brokera)
#MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", None)                                # Hasło (opcjonalne dla publicznego brokera)
#STUDENT_ID = os.getenv("STUDENT_ID", "213769")                                  # Unikalny identyfikator studenta
#TOPIC = f"{STUDENT_ID}/{location}"                                              # Temat MQTT, np. "261356/Wroclaw"
#TOPIC_PATTERN = "#"  


import paho.mqtt.client as mqtt

class MQTTPublisher:
    def __init__(self, broker_address, broker_port, username, password):
        # Tworzy nową instancję klienta MQTT z wersji 3 API
        self.client = mqtt.Client()

        # Ustawia dane uwierzytelniające użytkownika (nazwa i hasło)
        self.client.username_pw_set(username, password)

        # Ustawienie callbacków
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish

        # Łączy klienta z brokerem MQTT na podanym adresie i porcie
        self.client.connect(broker_address, broker_port, 60)

        # Uruchamia pętlę MQTT w tle (background)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback wywoływany po udanym połączeniu z brokerem.
        """
        if rc == 0:
            print("Połączenie z brokerem udane.")
        else:
            print(f"Połączenie z brokerem nie powiodło się. Kod błędu: {rc}")

    

    def on_publish(self, client, userdata, mid):
        """
        Callback wywoływany po opublikowaniu wiadomości.
        """
        print(f"Wiadomość opublikowana: {mid}")

    def publish_message(self, topic, message):
        """
        Publikuje wiadomość na podany temat (topic) z treścią (message).
        """
        self.client.publish(topic, message)

    def stop(self):
        """
        Zatrzymuje pętlę klienta i kończy połączenie.
        """
        self.client.loop_stop()
        self.client.disconnect()
