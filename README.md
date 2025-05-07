```
EMOTIONAL BOT/
├── api/
│   └── app.py                ✅ Tu API en Flask
├── models/
│   ├── sentiment_model.pkl   ✅ Modelo entrenado
│   └── vectorizer.pkl        ✅ Vectorizador
├── src/
│   ├── predict.py            ✅ Función de predicción
│   └── sentiment_model.py    ✅ Entrenamiento del modelo
├── venv/                     
├── .gitignore                
├── requirements.txt          
```
```
curl -X POST http://127.0.0.1:5000/analizar ^
  -H "Content-Type: application/json" ^
  -d "{\"mensaje\": \"no me gustó nada\"}"
```
