# 🎯 Hand Tracking with MediaPipe

Programa simple y efectivo para detectar y rastrear manos en tiempo real usando la cámara web. Utiliza MediaPipe de Google para un reconocimiento preciso de 21 puntos clave por mano.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey)

## ✨ Características

- ✅ Detección de hasta 2 manos simultáneamente
- ✅ Rastrea 21 puntos de referencia por mano en tiempo real
- ✅ Dibuja esqueleto de la mano automáticamente
- ✅ Funciona sin lag en tiempo real
- ✅ Compatible con Windows, Mac y Linux
- ✅ Instalación automática con un comando

## 📋 Requisitos previos

- **Python 3.8** o superior
- **Cámara web** conectada
- **Windows, Mac o Linux**

## 🚀 Instalación rápida (3 pasos)

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/junkun123/hand-tracking.git
cd hand-tracking
```

### 2️⃣ Ejecutar el setup (instala todo automáticamente)
```bash
python setup.py
```

El script automáticamente:
- Crea el entorno virtual
- Instala todas las dependencias
- Verifica que todo funcione correctamente

### 3️⃣ Ejecutar el programa
```bash
python hand_tracking.py
```

¡Y listo! Ya está detectando tus manos.

## 📖 Uso

```bash
python hand_tracking.py
```

**Controles:**
- **Q** → Salir del programa
- **Mueve tu mano** frente a la cámara para ver el trackeo en tiempo real

## 📁 Estructura del proyecto

```
hand-tracking/
├── hand_tracking.py          # Programa principal
├── setup.py                  # Setup automático (Windows/Mac/Linux)
├── run.bat                   # Ejecutar en Windows (opcional)
├── run.sh                    # Ejecutar en Mac/Linux (opcional)
├── requirements.txt          # Dependencias
├── README.md                 # Este archivo
└── .gitignore               # Archivos ignorados en Git
```

## 📦 Dependencias

| Librería | Versión | Propósito |
|----------|---------|----------|
| mediapipe | 0.10.13 | Detección de manos |
| opencv-python | Latest | Captura de cámara |
| numpy | Latest | Procesamiento de datos |

## 🛠️ Solución de problemas

### ❌ Error: "No module named 'mediapipe'"
```bash
# Reinstala las dependencias
python setup.py
```

### ❌ Error: "Camera not found"
- Verifica que tu cámara esté conectada
- Cierra otras aplicaciones que usen la cámara
- En Windows, ve a Configuración → Privacidad → Cámara

### ❌ Error: "AttributeError: module 'mediapipe' has no attribute 'solutions'"
- Ejecuta nuevamente el setup.py
- Asegúrate de tener Python 3.8 o superior

## 💡 Tips

- **Primera ejecución**: Puede ser lenta mientras carga el modelo (es normal)
- **Mejor detección**: Asegúrate de tener buena iluminación
- **Rendimiento**: Si la cámara va lenta, reduce la resolución de tu webcam

## 🎓 Aprendiendo el código

### Estructura básica de `hand_tracking.py`:

```python
1. Importar librerías (cv2, mediapipe, numpy)
2. Inicializar MediaPipe Hands
3. Abrir cámara web
4. Loop principal:
   - Capturar frame
   - Detectar manos
   - Dibujar puntos y conexiones
   - Mostrar en pantalla
5. Liberar recursos
```

## 🔧 Personalización

### Cambiar número de manos detectadas
En `hand_tracking.py`, línea ~12:
```python
hands = mp_hands.Hands(
    max_num_hands=2,  # Cambia a 1, 2, 3, etc.
    ...
)
```

### Cambiar sensibilidad de detección
```python
hands = mp_hands.Hands(
    min_detection_confidence=0.5,    # Rango: 0.0 a 1.0
    min_tracking_confidence=0.5,     # Aumenta para ser más estricto
    ...
)
```

## 📚 Recursos útiles

- [MediaPipe Hands Documentation](https://mediapipe.dev/solutions/hands)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Python Official](https://www.python.org/)

## 📝 Notas importantes

- Este proyecto usa **MediaPipe v0.10.13** por compatibilidad
- Los modelos de IA se descargan automáticamente
- El programa usa la cámara predeterminada del sistema (índice 0)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:
1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit cambios (`git commit -am 'Agrega mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**junkun123** - [@junkun123](https://github.com/junkun123)

## 🐛 Reportar bugs

Si encuentras un bug, por favor abre un [Issue](https://github.com/junkun123/hand-tracking/issues) con:
- Descripción del problema
- Sistema operativo
- Versión de Python
- Pasos para reproducir

---

**¿Tienes dudas?** Abre un issue o revisa la documentación de MediaPipe. 🚀
