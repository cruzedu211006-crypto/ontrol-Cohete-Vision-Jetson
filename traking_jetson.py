import cv2
import serial
import time
from ultralytics import YOLO

# --- CONFIGURACIÓN DEL SISTEMA ---
FUENTE_VIDEO = 0  # 0 para cámara en vivo, o cambia por "video_cohete.mp4"
PUERTO_SERIAL = '/dev/ttyTHS1'  # Puerto UART físico de la Jetson Nano
BAUD_RATE = 115200

# Inicializar comunicación con el ESP32
try:
    arduino = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=1)
    time.sleep(2)
    print("Conexión serial establecida con el controlador de servos.")
except:
    print("Error: No se detectó el hardware esclavo. Simulando ejecución...")
    arduino = None

# Cargar modelo YOLOv8 optimizado
model = YOLO('best.pt')

cap = cv2.VideoCapture(FUENTE_VIDEO)
print("Pipeline de ejecución iniciado. Presiona 'q' para salir.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Dimensiones de la pantalla para calcular el centro
    alto, ancho, _ = frame.shape
    centro_x_pantalla = ancho // 2
    centro_y_pantalla = alto // 2

    # Inferencia en tiempo real
    results = model(frame, verbose=False)
    
    # Algoritmo de Lazo Cerrado y Control Proporcional
    kp = 0.4  # Constante Proporcional de estabilidad
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Obtener centroide del bounding box detectado
            x1, y1, x2, y2 = box.xyxy[0]
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            # Calcular error respecto al centro de referencia
            error_x = cx - centro_x_pantalla
            error_y = cy - centro_y_pantalla

            # Aplicar corrección proporcional (mapeo a grados de servos)
            servo_x = int(90 + (error_x * kp))
            servo_y = int(90 + (error_y * kp))

            # Restringir límites físicos de los motores (0 a 180 grados)
            servo_x = max(0, min(180, servo_x))
            servo_y = max(0, min(180, servo_y))

            # Enviar coordenadas cinemáticas mediante UART al ESP32
            if arduino:
                cadena_control = f"{servo_x},{servo_y}\n"
                arduino.write(cadena_control.encode('utf-8'))
            
            # Dibujar telemetría visual en pantalla
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    # Mostrar FPS e interfaz gráfica
    cv2.imshow("Sistema de Control de Lazo Cerrado - Jetson", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()