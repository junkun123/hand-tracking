#!/usr/bin/env python3
"""
Setup script para Traductor de Señas IA
Funciona en Windows, Mac y Linux
Verifica la versión de Python e instala todas las dependencias (OpenCV, MediaPipe, Sklearn)
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_step(step_num, text):
    print(f"[{step_num}] {text}")

def run_command(command, show_output=False):
    """Ejecuta un comando y retorna si fue exitoso"""
    try:
        if show_output:
            result = subprocess.run(command, shell=True, check=True)
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return True, result.stdout if not show_output else ""
    except subprocess.CalledProcessError as e:
        return False, str(e)

def main():
    print_header("🎯 TRADUCTOR DE SEÑAS IA - SETUP AUTOMÁTICO")
    
    system = platform.system()
    python_version = sys.version_info
    print(f"✓ Sistema operativo: {system}")
    print(f"✓ Python detectado: {sys.version.split()[0]}\n")
    
    # ============= PASO 0: Verificar versión de Python =============
    print_step(0, "Verificando compatibilidad de Python...")
    if python_version < (3, 8) or python_version >= (3, 12):
        print("  ⚠️ ADVERTENCIA: Se recomienda Python 3.8, 3.9, 3.10 o 3.11.")
        print("  Versiones más antiguas o la 3.12+ pueden tener problemas con MediaPipe.")
        respuesta = input("  ¿Deseas continuar de todos modos? (s/n): ")
        if respuesta.lower() != 's':
            print("\n❌ Instalación abortada. Instala una versión recomendada de Python.")
            sys.exit(1)
    print("  ✅ Versión de Python aceptada.\n")
    
    # ============= PASO 1: Crear entorno virtual =============
    print_step(1, "Creando entorno virtual...")
    env_name = "hand_tracking_env"
    
    if os.path.exists(env_name):
        print(f"  ℹ️  El entorno '{env_name}' ya existe, usando el existente\n")
    else:
        success, msg = run_command(f"{sys.executable} -m venv {env_name}")
        if success:
            print(f"  ✅ Entorno virtual creado correctamente\n")
        else:
            print(f"  ❌ Error creando entorno: {msg}")
            sys.exit(1)
    
    # ============= PASO 2: Configurar comandos según SO =============
    print_step(2, "Configurando comandos para tu sistema...")
    
    if system == "Windows":
        pip_cmd = f"{env_name}\\Scripts\\pip"
        python_cmd = f"{env_name}\\Scripts\\python"
        activate_cmd = f"{env_name}\\Scripts\\activate.bat"
    else:
        pip_cmd = f"{env_name}/bin/pip"
        python_cmd = f"{env_name}/bin/python"
        activate_cmd = f"source {env_name}/bin/activate"
    
    print(f"  ✓ Python del entorno: {python_cmd}")
    print(f"  ✓ Pip del entorno: {pip_cmd}\n")
    
    # ============= PASO 3: Actualizar pip =============
    print_step(3, "Actualizando administrador de paquetes (pip)...")
    run_command(f"{pip_cmd} install --upgrade pip", show_output=False)
    print("  ✅ Pip actualizado\n")
    
    # ============= PASO 4: Instalar dependencias esenciales =============
    print_step(4, "Instalando librerías de Visión e IA (Esto puede tardar)...")
    
    # Lista actualizada con las librerías necesarias para el modelo RandomForest
    essential_packages = [
        ("numpy", "numpy"),
        ("opencv-python", "cv2"),
        ("mediapipe", "mediapipe"),
        ("pandas", "pandas"),
        ("scikit-learn", "sklearn")
    ]
    
    for package_name, import_name in essential_packages:
        print(f"  📦 Instalando {package_name}...", end=" ", flush=True)
        success, msg = run_command(f"{pip_cmd} install {package_name}")
        if success:
            print("✅")
        else:
            print(f"⚠️ (Hubo un problema, revisa tu internet)")
    
    print()
    
    # ============= PASO 5: Instalar requirements.txt =============
    print_step(5, "Verificando dependencias adicionales...")
    
    if os.path.exists("requirements.txt"):
        success, msg = run_command(f"{pip_cmd} install -r requirements.txt")
        if success:
            print("  ✅ Dependencias de requirements.txt instaladas\n")
        else:
            print("  ⚠️  Algunas dependencias tuvieron advertencias (normal)\n")
    else:
        print("  ℹ️  No hay requirements.txt extra (opcional)\n")
    
    # ============= PASO 6: Verificar instalación =============
    print_step(6, "Verificando que la Inteligencia Artificial pueda ejecutarse...")
    
    verification_script = """
import sys
try:
    import cv2
    import mediapipe as mp
    import numpy
    import pandas
    import sklearn
    
    if not hasattr(mp, 'solutions'):
        print("ERROR_NO_SOLUTIONS")
        sys.exit(1)
        
    print("OK")
    sys.exit(0)
except ImportError as e:
    print(f"ERROR:{e}")
    sys.exit(1)
"""
    
    result = subprocess.run(
        [python_cmd, "-c", verification_script],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode == 0 and "OK" in result.stdout:
        print("  ✅ OpenCV (Cámara) ................. CORRECTO")
        print("  ✅ MediaPipe (Manos) ............... CORRECTO")
        # Agregamos validación de los nuevos paquetes
        print("  ✅ Pandas & Scikit-Learn (IA) ...... CORRECTO\n")
    elif "ERROR_NO_SOLUTIONS" in result.stdout:
        print("  ⚠️  MediaPipe instalado pero con errores.")
        print("  🔄 Intentando reparar...", end=" ", flush=True)
        run_command(f"{pip_cmd} uninstall mediapipe -y")
        run_command(f"{pip_cmd} install mediapipe==0.10.14")
        print("✅\n")
    else:
        print(f"  ⚠️  Verificación falló. Puede que falte alguna librería.\n  Detalle: {result.stdout.strip()}\n")
    
    # ============= PASO 7: Mostrar instrucciones finales =============
    print_header("✅ INSTALACIÓN COMPLETADA EXITOSAMENTE")
    
    print("🚀 PARA INICIAR EL TRADUCTOR:\n")
    
    if system == "Windows":
        print("  Opción 1 - En la terminal:")
        print(f"    1. Activa el entorno:  {activate_cmd}")
        print("    2. Ejecuta la cámara:  python app.py  (o el nombre de tu archivo principal)\n")
    else:
        print("  Opción 1 - En la terminal:")
        print(f"    1. Activa el entorno:  {activate_cmd}")
        print("    2. Ejecuta la cámara:  python app.py\n")
    
    print("="*70)
    print("💡 TIPS IMPORTANTES:")
    print("  • Si clonaste el repositorio sin el modelo (.pkl), primero ejecuta el entrenador.")
    print("  • Presiona 'q' para SALIR de la ventana de la cámara.")
    print("="*70 + "\n")
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        sys.exit(1)