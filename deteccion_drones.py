import cv2
from ultralytics import YOLO

# 1. Cargar el modelo que acabas de entrenar
# (Asegúrate de que best.pt esté en la misma carpeta que este script)
print("Cargando el cerebro del dron...")
modelo = YOLO('best (1).pt')

# 2. Encender la cámara web de tu laptop
# El '0' suele ser la cámara web integrada. Si usas una externa, intenta con '1' o '2'.
cap = cv2.VideoCapture(0)

print("¡Cámara encendida! Presiona la tecla 'q' para salir.")

# 3. Bucle en tiempo real
while True:
    # Leer el cuadro actual de la cámara
    ret, frame = cap.read()
    if not ret:
        print("No se pudo acceder a la cámara.")
        break

    # 4. Pedirle a la IA que busque drones en la imagen
    # verbose=False evita que la terminal se llene de texto innecesario
    resultados = modelo(frame, verbose=False)

    # 5. Dibujar los resultados en la imagen
    # Esto dibuja automáticamente los cuadros (bounding boxes) sobre lo que detecta
    frame_anotado = resultados[0].plot()

    # Mostrar la ventana con el video en vivo
    cv2.imshow("Prueba YOLOv8 - Cazador de Drones", frame_anotado)

    # Salir si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Apagar la cámara y cerrar ventanas al terminar
cap.release()
cv2.destroyAllWindows()