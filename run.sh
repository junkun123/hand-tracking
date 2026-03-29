#!/bin/bash
# Script para ejecutar Hand Tracking en Mac/Linux
# Activa el entorno virtual y ejecuta el programa

clear

echo "====================================="
echo "Hand Tracking - Mac/Linux Launcher"
echo "====================================="
echo ""

# Verificar si el entorno existe
if [ ! -d "hand_tracking_env" ]; then
    echo "Error: El entorno virtual no existe."
    echo "Por favor ejecuta primero: python3 setup.py"
    read -p "Presiona Enter para salir..."
    exit 1
fi

# Activar entorno
echo "Activando entorno virtual..."
source hand_tracking_env/bin/activate

# Ejecutar programa
echo ""
echo "====================================="
echo "Iniciando Hand Tracking..."
echo "Presiona 'q' para salir"
echo "====================================="
echo ""

python hand_tracking.py

read -p "Presiona Enter para salir..."
