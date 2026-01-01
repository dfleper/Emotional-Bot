from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "sentiment_model.pkl"
VECTORIZER_PATH = MODELS_DIR / "vectorizer.pkl"

_modelo = None
_vectorizer = None


def normalizar(txt: str) -> str:
    txt = (txt or "").lower().strip()

    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(c for c in txt if not unicodedata.combining(c))

    txt = re.sub(r"[^a-z0-9\s]", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt


def _cargar_activos():
    global _modelo, _vectorizer

    if _modelo is not None and _vectorizer is not None:
        return

    if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
        raise FileNotFoundError(
            "No se encontraron los archivos del modelo. "
            "Ejecuta primero: python src/sentiment_model.py (o start_project.bat). "
            f"Faltan: {MODEL_PATH} o {VECTORIZER_PATH}"
        )

    _modelo = joblib.load(MODEL_PATH)
    _vectorizer = joblib.load(VECTORIZER_PATH)


def _reglas_sentimiento(txt_norm: str) -> str | None:
    """
    Reglas rápidas para casos obvios (prioridad sobre el modelo).
    Negativo tiene prioridad sobre positivo.
    """
    negativas = [
        "asqueroso",
        "chatarra",
        "en las ultimas",
        "horrible",
        "pesimo",
        "fatal",
        "terrible",
        "desastre",
        "odio",
        "muy malo",
        "muy mal",
        "decepcion",
        "decepcionante",
        "basura",
        "no me gusta",
        "no me gusto",
    ]

    positivas = [
        "genial",
        "excelente",
        "bonito",
        "perfecto",
        "increible",
        "me encanta",
        "me gusta",
        "me gusto",
        "recomiendo",
        "muy bueno",
        "muy bien",
    ]

    for w in negativas:
        if w in txt_norm:
            return "negativo"

    for w in positivas:
        if w in txt_norm:
            return "positivo"

    return None


def predecir_sentimiento(mensaje: str) -> str:
    _cargar_activos()

    txt_norm = normalizar(mensaje)

    # 1) Reglas primero (corrigen casos obvios)
    por_regla = _reglas_sentimiento(txt_norm)
    if por_regla is not None:
        return por_regla

    # 2) Modelo
    X = _vectorizer.transform([txt_norm])

    # Si quedara vacío, devolvemos negativo conservador
    if getattr(X, "nnz", 0) == 0:
        return "negativo"

    return _modelo.predict(X)[0]
