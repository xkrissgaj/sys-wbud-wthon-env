import paho.mqtt.client as mqtt

class MQTTPublisher:
    def __init__(self, broker_address, broker_port, username, password):
        # Tworzy nową instancję klienta MQTT
        self.client = mqtt.Client()
        
        # Ustawia dane uwierzytelniające użytkownika (nazwa i hasło)
        self.client.username_pw_set(username, password)
        
        # Łączy klienta z brokerem MQTT na podanym adresie i porcie
        self.client.connect(broker_address, broker_port)
        
        # Start pętli w tle
        self.client.loop_start()  
    
    def publish_message(self, topic, message):
        # Publikuje wiadomość na podany temat (topic) z treścią (message)
        self.client.publish(topic, message)
