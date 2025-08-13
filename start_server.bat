@echo off
echo ========================================
echo    GlaciarIng - Full Stack Application
echo ========================================
echo.
echo Iniciando servidor con MongoDB Atlas...
echo.
echo Frontend disponible en: http://localhost:5003
echo API disponible en: http://localhost:5003/api/
echo.
echo Presiona Ctrl+C para detener el servidor
echo ========================================
echo.

.venv\Scripts\python.exe api_server.py

pause
