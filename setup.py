#!/usr/bin/env python3
"""
Setup script para Hand Tracking
Funciona en Windows, Mac y Linux
Instala automáticamente todas las dependencias
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"🔄 {description}...")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, check=True)
        else:
            result = subprocess.run(command, check=True)
        print(f"✅ {description} completado\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}\n")
        return False

def main():
    print_header("🎯 Hand Tracking - Setup Automático")
    
    system = platform.system()
    print(f"Sistema operativo detectado: {system}\n")
    
    # Paso 1: Crear entorno virtual
    env_name = "hand_tracking_env"
    
    print(f"📁 Entorno será creado en: {os.path.abspath(env_name)}\n")
    
    if not os.path.exists(env_name):
        if not run_command([sys.executable, "-m", "venv", env_name], 
                          "Creando entorno virtual"):
            print("❌ No se pudo crear el entorno virtual")
            sys.exit(1)
    else:
        print(f"✅ El entorno virtual '{env_name}' ya existe\n")
    
    # Paso 2: Obtener comando de pip según el SO
    if system == "Windows":
        pip_cmd = f"{env_name}\\Scripts\\pip"
        python_cmd = f"{env_name}\\Scripts\\python"
        activate_cmd = f"{env_name}\\Scripts\\activate.bat"
    else:  # Mac y Linux
        pip_cmd = f"{env_name}/bin/pip"
        python_cmd = f"{env_name}/bin/python"
        activate_cmd = f"source {env_name}/bin/activate"
    
    # Paso 3: Actualizar pip
    if not run_command(f"{pip_cmd} install --upgrade pip", 
                      "Actualizando pip"):
        print("⚠️  Pip no se actualizó, continuando...")
    
    # Paso 4: Instalar dependencias
    if not os.path.exists("requirements.txt"):
        print("❌ No se encontró requirements.txt")
        sys.exit(1)
    
    if not run_command(f"{pip_cmd} install -r requirements.txt", 
                      "Instalando dependencias"):
        print("❌ No se pudieron instalar las dependencias")
        sys.exit(1)
    
    # Paso 5: Verificar instalación
    print_header("✓ Verificando instalación")
    try:
        result = subprocess.run(
            [python_cmd, "-c", "import cv2; import mediapipe; print('ok')"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ opencv-python correctamente instalado")
            print("✅ mediapipe correctamente instalado\n")
        else:
            print("⚠️  Advertencia en la verificación\n")
    except Exception as e:
        print(f"⚠️  No se pudo verificar: {e}\n")
    
    # Paso 6: Mostrar instrucciones finales
    print_header("✅ SETUP COMPLETADO CON ÉXITO")
    
    print("📌 Para ejecutar el programa:\n")
    
    if system == "Windows":
        print(f"  1. Activa el entorno:")
        print(f"     {activate_cmd}\n")
        print(f"  2. Ejecuta el programa:")
        print(f"     python hand_tracking.py\n")
        print(f"  O simplemente ejecuta (si tienes run.bat):")
        print(f"     run.bat\n")
    else:
        print(f"  1. Activa el entorno:")
        print(f"     {activate_cmd}\n")
        print(f"  2. Ejecuta el programa:")
        print(f"     python hand_tracking.py\n")
        print(f"  O simplemente ejecuta (si tienes run.sh):")
        print(f"     bash run.sh\n")
    
    print("="*60)
    print("💡 TIPS:")
    print("  - Asegúrate de tener la cámara conectada")
    print("  - Presiona 'q' para salir del programa")
    print("  - Si tienes problemas, revisa el README.md")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
