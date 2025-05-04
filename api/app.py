import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from src.predict import predecir_sentimiento

app = Flask(__name__)

@app.route("/analizar", methods=["POST"])
def analizar():
    data = request.get_json()
    mensaje = data.get("mensaje", "")
    sentimiento = predecir_sentimiento(mensaje)
    return jsonify({"sentimiento": sentimiento})

@app.route("/", methods=["GET"])
def home():
    return "✅ Emotional Bot API is running. Use /analizar with POST."

if __name__ == "__main__":
    app.run(debug=True)
