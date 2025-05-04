import joblib

# Cargar modelo y vectorizador
modelo = joblib.load('models/sentiment_model.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')

def predecir_sentimiento(mensaje):
    X = vectorizer.transform([mensaje])
    return modelo.predict(X)[0]
