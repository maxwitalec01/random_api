from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Define the base URLs for the 4 Flask instances
FLASK_INSTANCES = [
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002",
    "http://127.0.0.1:5003",
    "http://127.0.0.1:5004"
]

@app.route('/aggregate')
def aggregate_metrics():
    """
    Aggregates data from multiple Flask instances and returns a combined response.
    If any instance fails (status code not 200), it will be set to "Error".
    """
    data = {}
    for i, url in enumerate(FLASK_INSTANCES, start=1):
        try:
            response = requests.get(f"{url}/metrics", timeout=5)
            if response.status_code == 200:
                data[f"node_{i}"] = response.json()
            else:
                data[f"node_{i}"] = "Error"
        except requests.exceptions.RequestException:
            data[f"node_{i}"] = "Error"
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)