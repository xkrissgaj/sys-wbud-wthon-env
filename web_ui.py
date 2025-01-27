from flask import Flask, render_template
import os
import json

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

# Ścieżka do folderu z danymi (współdzielona przez Docker Volume)
DATA_FOLDER = os.getenv("DATA_FOLDER", "./data")

@app.route('/')
def index():
    try:
        # Pobierz listę plików z folderu DATA_FOLDER
        files = os.listdir(DATA_FOLDER)
        
        # Lista do przechowywania danych
        measurements = []

        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(DATA_FOLDER, file)

                with open(file_path, 'r') as f:
                    data = json.load(f)
                    measurements.append({
                        "file": file,
                        "data": data
                    })

        # Renderuj stronę HTML z wykorzystaniem Jinja2
        return render_template('index.html', measurements=measurements)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
