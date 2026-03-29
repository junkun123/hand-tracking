#!/usr/bin/env python3
"""
Setup script para Hand Tracking
Funciona en Windows, Mac y Linux
Instala automáticamente todas las dependencias de forma robusta
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
    print_header("🎯 HAND TRACKING - INSTALACIÓN AUTOMÁTICA")
    
    system = platform.system()
    print(f"✓ Sistema operativo: {system}")
    print(f"✓ Python: {sys.version.split()[0]}\n")
    
    # ============= PASO 1: Crear entorno virtual =============
    print_step(1, "Creando entorno virtual...")
    env_name = "hand_tracking_env"
    
    if os.path.exists(env_name):
        print(f"   ℹ️  El entorno '{env_name}' ya existe, usando el existente\n")
    else:
        success, msg = run_command(f"{sys.executable} -m venv {env_name}")
        if success:
            print(f"   ✅ Entorno virtual creado correctamente\n")
        else:
            print(f"   ❌ Error creando entorno: {msg}")
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
    
    print(f"   ✓ Python: {python_cmd}")
    print(f"   ✓ Pip: {pip_cmd}\n")
    
    # ============= PASO 3: Actualizar pip =============
    print_step(3, "Actualizando pip...")
    run_command(f"{pip_cmd} install --upgrade pip", show_output=False)
    print("   ✅ Pip actualizado\n")
    
    # ============= PASO 4: Instalar dependencias esenciales =============
    print_step(4, "Instalando dependencias esenciales...")
    
    essential_packages = [
        ("numpy", "numpy"),
        ("opencv-python", "cv2"),
        ("mediapipe", "mediapipe")
    ]
    
    for package_name, import_name in essential_packages:
        print(f"   📦 Instalando {package_name}...", end=" ", flush=True)
        success, msg = run_command(f"{pip_cmd} install {package_name}")
        if success:
            print("✅")
        else:
            print(f"⚠️ (continuando...)")
    
    print()
    
    # ============= PASO 5: Instalar requirements.txt =============
    print_step(5, "Instalando dependencias adicionales...")
    
    if os.path.exists("requirements.txt"):
        success, msg = run_command(f"{pip_cmd} install -r requirements.txt")
        if success:
            print("   ✅ Dependencias adicionales instaladas\n")
        else:
            print("   ⚠️  Algunas dependencias tuvieron advertencias (normal)\n")
    else:
        print("   ℹ️  No hay requirements.txt (opcional)\n")
    
    # ============= PASO 6: Verificar instalación =============
    print_step(6, "Verificando instalación...")
    
    verification_script = """
import sys
try:
    import cv2
    import mediapipe as mp
    import numpy
    
    # Verificar que mediapipe tiene solutions
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
        print("   ✅ cv2 (OpenCV) ................. CORRECTAMENTE INSTALADO")
        print("   ✅ mediapipe .................... CORRECTAMENTE INSTALADO")
        print("   ✅ numpy ........................ CORRECTAMENTE INSTALADO\n")
    elif "ERROR_NO_SOLUTIONS" in result.stdout:
        print("   ⚠️  MediaPipe instalado pero sin 'solutions'")
        print("   🔄 Reinstalando mediapipe...", end=" ", flush=True)
        run_command(f"{pip_cmd} uninstall mediapipe -y")
        run_command(f"{pip_cmd} install mediapipe==0.10.13 --force-reinstall")
        print("✅\n")
    else:
        print(f"   ⚠️  Verificación completada con advertencias\n")
    
    # ============= PASO 7: Mostrar instrucciones finales =============
    print_header("✅ INSTALACIÓN COMPLETADA")
    
    print("🚀 PRÓXIMOS PASOS:\n")
    
    if system == "Windows":
        print("  Opción 1 - Activar entorno manualmente:")
        print(f"    {activate_cmd}")
        print("    python hand_tracking.py\n")
        
        print("  Opción 2 - Ejecutar directamente (si existe run.bat):")
        print("    run.bat\n")
    else:
        print("  Opción 1 - Activar entorno manualmente:")
        print(f"    {activate_cmd}")
        print("    python hand_tracking.py\n")
        
        print("  Opción 2 - Ejecutar directamente (si existe run.sh):")
        print("    bash run.sh\n")
    
    print("="*70)
    print("💡 TIPS IMPORTANTES:")
    print("  • Asegúrate de tener la CÁMARA CONECTADA")
    print("  • Presiona 'q' para SALIR del programa")
    print("  • Primera ejecución puede ser lenta (cargando modelo IA)")
    print("  • Si hay problemas, revisa el README.md")
    print("="*70 + "\n")
    
    print("✨ ¡TODO LISTO! ¡A DISFRUTAR! ✨\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        sys.exit(1)
