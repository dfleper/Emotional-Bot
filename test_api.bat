@echo off
setlocal enabledelayedexpansion

echo ============================================
echo EMOTIONAL BOT - PREGUNTA Y RESPUESTA API
echo ============================================

set /p mensaje=Escribe tu mensaje positivo o negativo: 

echo.
echo Enviando mensaje a la API...
curl -X POST http://127.0.0.1:5000/analizar ^
  -H "Content-Type: application/json" ^
  -d "{\"mensaje\": \"!mensaje!\"}"

echo.
pause