FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY weather_requester.py .

# Set environment variables
ENV LOCATION=Delhi
ENV MQTT_BROKER=localhost
ENV MQTT_PORT=1883
ENV MQTT_TOPIC=weather/data

# Run the application
CMD ["python", "weather_requester.py"]
