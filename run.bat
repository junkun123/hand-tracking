@echo off
REM Script para ejecutar Hand Tracking en Windows
REM Activa el entorno virtual y ejecuta el programa

cls
echo =====================================
echo Hand Tracking - Windows Launcher
echo =====================================
echo.

REM Verificar si el entorno existe
if not exist "hand_tracking_env\" (
    echo Error: El entorno virtual no existe.
    echo Por favor ejecuta primero: python setup.py
    pause
    exit /b 1
)

REM Activar entorno
echo Activando entorno virtual...
call hand_tracking_env\Scripts\activate.bat

REM Ejecutar programa
echo.
echo =====================================
echo Iniciando Hand Tracking...
echo Presiona 'q' para salir
echo =====================================
echo.

python hand_tracking.py

pause
