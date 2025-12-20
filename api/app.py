import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from src.predict import predecir_sentimiento

MAX_MESSAGE_LENGTH = 1000

app = Flask(__name__)

@app.route("/analizar", methods=["POST"])
def analizar():
    if not request.is_json:
        return jsonify({"error": "El cuerpo debe ser JSON."}), 400

    data = request.get_json(silent=True) or {}
    mensaje = data.get("mensaje", "")
    if not isinstance(mensaje, str):
        return jsonify({"error": "El campo 'mensaje' debe ser texto."}), 400
    mensaje = mensaje.strip()
    if not mensaje:
        return jsonify({"error": "El campo 'mensaje' no puede estar vacío."}), 400
    if len(mensaje) > MAX_MESSAGE_LENGTH:
        return jsonify({"error": "El campo 'mensaje' supera el límite permitido."}), 400
    sentimiento = predecir_sentimiento(mensaje)
    return jsonify({"sentimiento": sentimiento})

@app.route("/", methods=["GET"])
def home():
    return "✅ Emotional Bot API is running. Use /analizar with POST."

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)
