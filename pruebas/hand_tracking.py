import cv2
import mediapipe as mp
import pickle
import warnings

# ── Ocultar advertencia de Protobuf ──────────────────────────────────────────
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf.symbol_database")

# ── Configuración ────────────────────────────────────────────────────────────
CAMERA_INDEX = 3 # Asegúrate de que sea el índice correcto de tu cámara
ARCHIVO_MODELO = "modelo_señas.pkl"

# 1. Cargar el modelo que acabas de entrenar
try:
    with open(ARCHIVO_MODELO, 'rb') as f:
        modelo = pickle.load(f)
    print("✅ Modelo de IA cargado correctamente.")
except FileNotFoundError:
    print(f"❌ Error: No se encontró '{ARCHIVO_MODELO}'.")
    exit()

# 2. Inicializar MediaPipe (solo para extraer los puntos)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False, 
    max_num_hands=1,         # Evaluamos una mano a la vez para mayor velocidad
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7
)

# 3. Iniciar la cámara
cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print("No se encontró ninguna cámara. Verifica el índice.")
    exit()

print("🎥 Cámara iniciada. Haz señas del abecedario frente a la cámara.")
print("Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret: break

    # Espejar la imagen para que sea como un espejo natural
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Procesar la imagen buscando manos
    results = hands.process(rgb_frame)
    letra_detectada = "Esperando seña..."

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Dibujar las líneas y puntos sobre la mano
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Extraer exactamente las 63 coordenadas (X, Y, Z de los 21 puntos)
            coordenadas = []
            for punto in hand_landmarks.landmark:
                coordenadas.extend([punto.x, punto.y, punto.z])
            
            # Pasarle las coordenadas a tu modelo para que adivine la letra
            try:
                prediccion = modelo.predict([coordenadas])[0]
                letra_detectada = str(prediccion).upper()
            except Exception as e:
                # Si hay algún pequeño error temporal en el tamaño de los datos, lo ignoramos
                pass 

    # 4. Interfaz Gráfica (HUD)
    h, w = frame.shape[:2]
    
    # Barra de fondo oscura
    cv2.rectangle(frame, (0, h - 80), (w, h), (0, 0, 0), -1)
    
    # Texto de la letra
    color_texto = (0, 255, 180) if letra_detectada != "Esperando seña..." else (200, 200, 200)
    cv2.putText(frame, f"Letra: {letra_detectada}", (10, h - 30),
                cv2.FONT_HERSHEY_DUPLEX, 1.2, color_texto, 2, cv2.LINE_AA)
    
    # Texto de ayuda
    cv2.putText(frame, "Presiona 'q' para salir", (10, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2, cv2.LINE_AA)

    # Mostrar la ventana
    cv2.imshow("Traductor Local de Senas", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpieza final
cap.release()
cv2.destroyAllWindows()
hands.close()