FROM python:3.10-slim

WORKDIR /app


# Kopiowanie plików aplikacji
COPY . /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install requests
RUN pip install -r requirements.txt
RUN pip install --upgrade paho-mqtt


# zainstaluj system i zainstaluj pip


# Copy application code
COPY weather_requester.py .
COPY mqtt_subscriber.py .
COPY mqtt_publisher.py .

# Set environment variables
#ENV LOCATION=Delhi
#ENV MQTT_BROKER=localhost
#ENV MQTT_PORT=1883
#ENV MQTT_TOPIC=weather/data

# Run the application
CMD ["python", "weather_requester.py"]
