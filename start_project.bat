@echo off
echo =====================================
echo EMOTIONAL BOT - INICIANDO PROYECTO
echo =====================================

if not exist "venv" (
    echo [1/5] Creando entorno virtual...
    python -m venv venv
)

echo [2/5] Activando entorno virtual...
call venv\Scripts\activate

echo [3/5] Instalando dependencias desde requirements.txt...
pip install -r requirements.txt

if not exist "models\sentiment_model.pkl" (
    echo [4/5] Entrenando modelo...
    python src/sentiment_model.py
) else (
    echo [4/5] Modelo ya existe. Omitiendo entrenamiento.
)

echo [5/5] Iniciando API Flask...
python api/app.py

pause