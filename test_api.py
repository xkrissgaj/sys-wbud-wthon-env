services:
  weather_requester:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - BROKER_ADDRESS=167.172.164.168
      - BROKER_PORT=1883
      - MQTT_USER=student
      - MQTT_PASSWORD=sys-wbud
      - STUDENT_ID=261356
      - LOCATIONS=10890
    restart: always

  subscriber:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ./data:/app/data  # Wolumen współdzielący dane
    environment:
      - BROKER_ADDRESS=167.172.164.168
      - BROKER_PORT=1883
      - MQTT_USER=student
      - MQTT_PASSWORD=sys-wbud
      - DATA_FOLDER=/app/data
    command: ["python", "mqtt_subscriber.py"]  # Poprawiona nazwa pliku
    restart: always

########################################################
services:
#  weather_requester:
#    build: .
#    ports:
#      - "8080:8080"
#    environment:
#      - LOCATION=Wroclaw                      # Można to nadpisać w przypadku potrzeby zmiany lokalizacji
#    volumes:
#      - .:/app                                # Mapowanie bieżącego katalogu (na hoście) do katalogu roboczego w kontenerze  
#    restart: always                           # Ustawiamy restart kontenera w razie błędu
#    container_name: weather_requester

  weather_requester:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - BROKER_ADDRESS="test.mosquitto.org"
      #- BROKER_ADDRESS=167.172.164.168
      - BROKER_PORT=1883
      # - MQTT_USER=student
      - MQTT_USER = None                                      # Nazwa użytkownika (opcjonalna dla publicznego brokera)
      - MQTT_PASSWORD = None
      # - MQTT_PASSWORD=sys-wbud
      - STUDENT_ID=213769
      - LOCATIONS=Wroclaw
    restart: always 

# subscriber:
#    build:
#     context: .
#      dockerfile: Dockerfile
#    volumes:
#      - ./data:/app/data  # Wolumen współdzielący dane
#    environment:
#      - BROKER_ADDRESS=167.172.164.168
#      - BROKER_PORT=1883
#      - MQTT_USER=student
#      - MQTT_PASSWORD=sys-wbud
#      - DATA_FOLDER=/app/data
#
#    command: ["python", "mqtt_subscriber.py"]  
#    restart: always


  publisher:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - BROKER_ADDRESS="test.mosquitto.org"
      - BROKER_PORT=1883
      # - MQTT_USER=student
      - MQTT_USER = None                                      # Nazwa użytkownika (opcjonalna dla publicznego brokera)
      - MQTT_PASSWORD = None
      # - MQTT_PASSWORD=sys-wbud
      - STUDENT_ID=213769
      - LOCATIONS=Wroclaw
    command: ["python", "mqtt_publisher.py"]  # Poprawiona nazwa pliku
    restart: always
