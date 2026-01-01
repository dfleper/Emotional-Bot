from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# =========================
# Paths (robust on Windows)
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent  # /src -> project root
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODELS_DIR / "sentiment_model.pkl"
VECTORIZER_PATH = MODELS_DIR / "vectorizer.pkl"


def normalizar(txt: str) -> str:
    """Normaliza texto para mejorar coincidencias del vectorizador."""
    txt = (txt or "").lower().strip()

    # Quitar acentos: qué -> que
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(c for c in txt if not unicodedata.combining(c))

    # Mantener letras/números y espacios
    txt = re.sub(r"[^a-z0-9\s]", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt


# =========================
# Datos de entrenamiento (demo)
# - Más ejemplos + ejemplos del dominio "coche"
# =========================
textos = [
    # POSITIVOS (lugar/servicio)
    "me encanta este lugar",
    "el servicio fue excelente",
    "todo estuvo genial",
    "que sitio tan bonito",
    "me ha gustado mucho",
    "muy buena experiencia",
    "perfecto lo recomiendo",
    "increible atencion",

    # POSITIVOS (coche)
    "el coche va genial",
    "el coche esta perfecto",
    "mi coche quedo como nuevo",
    "el coche funciona muy bien",
    "muy buen trabajo con el coche",

    # NEGATIVOS (lugar/servicio)
    "odio este sitio",
    "muy mala experiencia",
    "no me gusto nada",
    "horrible que desastre",
    "pesimo servicio",
    "fatal no vuelvo",
    "terrible experiencia",
    "muy malo",

    # NEGATIVOS (coche)
    "el coche esta asqueroso",
    "el coche es una chatarra",
    "el coche esta en las ultimas",
    "mi coche va fatal",
    "el coche funciona muy mal",
    "una decepcion con el coche",
]

etiquetas = [
    # positivos (8)
    "positivo", "positivo", "positivo", "positivo", "positivo", "positivo", "positivo", "positivo",
    # positivos coche (5)
    "positivo", "positivo", "positivo", "positivo", "positivo",
    # negativos (8)
    "negativo", "negativo", "negativo", "negativo", "negativo", "negativo", "negativo", "negativo",
    # negativos coche (6)
    "negativo", "negativo", "negativo", "negativo", "negativo", "negativo",
]

# Normalizar entrenamiento
textos_norm = [normalizar(t) for t in textos]

# Vectorizador robusto: char-ngrams
vectorizer = TfidfVectorizer(
    analyzer="char_wb",
    ngram_range=(3, 5),
    sublinear_tf=True
)

X = vectorizer.fit_transform(textos_norm)

# Entrenar modelo
modelo = MultinomialNB()
modelo.fit(X, etiquetas)

# Guardar
joblib.dump(modelo, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)

print(f"Modelo guardado en: {MODEL_PATH}")
print(f"Vectorizador guardado en: {VECTORIZER_PATH}")
