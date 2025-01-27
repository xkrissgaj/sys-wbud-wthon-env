FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Kopiowanie plików aplikacji
COPY . /app

# Install dependencies

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
