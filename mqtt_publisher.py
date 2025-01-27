import paho.mqtt.client as mqtt

class MQTTPublisher:
    def __init__(self, broker_address, broker_port, username, password):
        # Tworzy nową instancję klienta MQTT
        self.client = mqtt.Client()

        # Ustawia dane uwierzytelniające użytkownika (nazwa i hasło)
        self.client.username_pw_set(username, password)

        # Ustawienie callbacków
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish

        # Łączy klienta z brokerem MQTT na podanym adresie i porcie
        self.client.connect(broker_address, broker_port)

        # Uruchamia pętlę MQTT w tle
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
