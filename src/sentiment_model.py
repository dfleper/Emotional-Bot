import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

# Datos de entrenamiento
textos = [
    "me encanta este lugar",
    "el servicio fue excelente",
    "odio este sitio",
    "muy mala experiencia",
    "todo estuvo genial",
    "no me gustó nada"
]
etiquetas = ["positivo", "positivo", "negativo", "negativo", "positivo", "negativo"]

# Vectorizar texto
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(textos)

# Entrenar modelo
modelo = MultinomialNB()
modelo.fit(X, etiquetas)

# Guardar modelo y vectorizador
joblib.dump(modelo, 'models/sentiment_model.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')

print("Modelo entrenado y guardado.")
