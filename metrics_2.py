from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
    """
    Root endpoint providing information about the random number generator.
    """
    return jsonify({
        "message": "Welcome to the Random Number Generator API!",
        "endpoint": "/random",
        "description": "Call /random to get a new random number."
    })

@app.route('/metrics')

def random_number():
    """
    Returns a random number between 1 and 100.
    """
    return jsonify({"random_number": random.randint(1, 100)})

if __name__ == '__main__':
    app.run(debug=True, port=5002)