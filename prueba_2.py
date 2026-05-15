import cv2, mediapipe as mp, pickle, warnings
warnings.filterwarnings("ignore")

try:
    with open("modelo_señas.pkl", 'rb') as f: modelo = pickle.load(f)
except FileNotFoundError:
    print("No se encontró el modelo. Ejecuta el entrenador primero.")
    exit()

hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.5)
cap = cv2.VideoCapture(3)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    letra = "..."
    info_secreta = "Buscando mano..."

    if results.multi_hand_landmarks:
        for hl in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, hl, mp.solutions.hands.HAND_CONNECTIONS)
            
            # MAGIA: Coordenadas relativas a la muñeca (punto 0)
            base_x, base_y, base_z = hl.landmark[0].x, hl.landmark[0].y, hl.landmark[0].z
            coords = [val for p in hl.landmark for val in (p.x - base_x, p.y - base_y, p.z - base_z)]
            
            try:
                probs = modelo.predict_proba([coords])[0]
                confianza = max(probs)
                letra_adivinada = str(modelo.classes_[probs.argmax()]).upper()
                info_secreta = f"IA piensa: {letra_adivinada} ({int(confianza * 100)}% segura)"
                
                # Muestra la letra si está más del 40% segura
                if confianza > 0.40: letra = letra_adivinada
            except: pass

    # HUD Visual
    cv2.putText(frame, f"Letra: {letra}", (20, 60), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255, 0), 2)
    cv2.putText(frame, info_secreta, (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.imshow("Traductor IA", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()