import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe con la nueva API
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Inicializar la cámara
cap = cv2.VideoCapture(3)

print("Cámara iniciada. Presiona 'q' para salir...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al leer la cámara")
        break
    
    h, w, c = frame.shape
    
    # Voltear la imagen horizontalmente
    frame = cv2.flip(frame, 1)
    
    # Convertir BGR a RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detectar manos
    results = hands.process(rgb_frame)
    
    # Dibujar landmarks si se detectaron manos
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
    
    # Mostrar información
    cv2.putText(frame, "Presiona 'q' para salir", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow('Hand Tracking', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
print("Programa finalizado")