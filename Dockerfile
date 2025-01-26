FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install requests
RUN pip install -r requirements.txt

# zainstaluj system i zainstaluj pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip

# Copy application code
COPY weather_requester.py .

# Set environment variables
ENV LOCATION=Delhi
ENV MQTT_BROKER=localhost
ENV MQTT_PORT=1883
ENV MQTT_TOPIC=weather/data

# Run the application
CMD ["python", "weather_requester.py"]
