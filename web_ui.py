from flask import Flask, render_template
import os
import json

app = Flask(__name__)

DATA_FOLDER = os.getenv("DATA_FOLDER", "./data")

@app.route('/')
def index():
    try:
        files = os.listdir(DATA_FOLDER)
        measurements = []

        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(DATA_FOLDER, file)

                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            measurements.append({
                                "file": file,
                                "data": data
                            })
                        else:
                            measurements.append({
                                "file": file,
                                "data": {"error": "Nieprawidłowy format danych (nie jest słownikiem)."}
                            })
                except json.JSONDecodeError:
                    measurements.append({
                        "file": file,
                        "data": {"error": "Nieprawidłowy format pliku JSON."}
                    })
                except Exception as e:
                    measurements.append({
                        "file": file,
                        "data": {"error": f"Błąd: {str(e)}"}
                    })

        return render_template('index.html', measurements=measurements)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
