import cv2, mediapipe as mp, pandas as pd, pickle, warnings
from sklearn.ensemble import RandomForestClassifier

warnings.filterwarnings("ignore")
hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.5)
cap = cv2.VideoCapture(3) # Ajusta el índice si tu cámara no abre

datos = []
conteo_letras = {}

print("=== ENTRENADOR DEL ABECEDARIO COMPLETO ===")
print("1. Haz una seña frente a la cámara.")
print("2. Presiona la tecla de esa letra (A-Z) unas 20-30 veces mientras mueves un poco la mano.")
print("3. Repite esto para todas las letras que quieras enseñar.")
print("4. Presiona '1' para entrenar tu IA y salir.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    res = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    mano_detectada = False
    if res.multi_hand_landmarks:
        mano_detectada = True
        for hl in res.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, hl, mp.solutions.hands.HAND_CONNECTIONS)

    # Interfaz
    cv2.putText(frame, "Haz la sena y presiona su tecla (A-Z)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.putText(frame, "Presiona '1' para GUARDAR MODELO", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Mostrar progreso
    y = 100
    for letra, cantidad in sorted(conteo_letras.items()):
        cv2.putText(frame, f"{letra}: {cantidad}", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        y += 20

    cv2.imshow("Entrenando Abecedario", frame)
    tecla = cv2.waitKey(1) & 0xFF
    
    if tecla == ord('1'):
        if datos:
            print("\nEntrenando IA... esto tomará un par de segundos.")
            df = pd.DataFrame(datos)
            modelo = RandomForestClassifier(n_estimators=100, random_state=42).fit(df.iloc[:, 1:], df.iloc[:, 0])
            with open("modelo_señas.pkl", 'wb') as f: pickle.dump(modelo, f)
            print("✅ ¡Modelo guardado con éxito! Ya conoce todas las letras que ingresaste.")
        else:
            print("\nNo tomaste ninguna foto.")
        break
    elif tecla == ord('q'): break
    
    # Si se presiona una letra y hay una mano
    elif ord('a') <= tecla <= ord('z') and mano_detectada:
        letra_presionada = chr(tecla).upper()
        for hl in res.multi_hand_landmarks:
            # MAGIA: Coordenadas relativas a la muñeca (punto 0)
            base_x, base_y, base_z = hl.landmark[0].x, hl.landmark[0].y, hl.landmark[0].z
            coords = [val for p in hl.landmark for val in (p.x - base_x, p.y - base_y, p.z - base_z)]
            
            datos.append([letra_presionada] + coords)
            conteo_letras[letra_presionada] = conteo_letras.get(letra_presionada, 0) + 1

cap.release()
cv2.destroyAllWindows()