#include <ESP32Servo.h>

// Instanciar los 4 servomotores del mecanismo cruciforme del cohete
Servo servoX1;
Servo servoX2; // Pareja en espejo del eje X
Servo servoY1;
Servo servoY2; // Pareja en espejo del eje Y

void setup() {
  // Iniciar puerto serial a la misma velocidad que la Jetson Nano
  Serial.begin(115200);
  
  // Asignar los pines GPIO correspondientes de salida PWM
  servoX1.attach(12);
  servoX2.attach(13);
  servoY1.attach(14);
  servoY2.attach(15);
  
  // Posición inicial segura (Home a 90 grados)
  servoX1.write(90);
  servoX2.write(90);
  servoY1.write(90);
  servoY2.write(90);
}

void loop() {
  // Escuchar constantemente el puerto UART esperando la cadena de control
  if (Serial.available() > 0) {
    String datosRecibidos = Serial.readStringUntil('\n');
    
    // Decodificar la cadena de texto con formato "GradosX,GradosY"
    int comaIndex = datosRecibidos.indexOf(',');
    if (comaIndex != -1) {
      String strX = datosRecibidos.substring(0, comaIndex);
      String strY = datosRecibidos.substring(comaIndex + 1);
      
      int anguloX = strX.toInt();
      int anguloY = strY.toInt();
      
      // --- CINEMÁTICA INVERSA Y CONFIGURACIÓN EN ESPEJO (CRUCIFORME) ---
      servoX1.write(anguloX);
      servoX2.write(180 - anguloX); // Movimiento complementario opuesto para torque
      
      servoY1.write(anguloY);
      servoY2.write(180 - anguloY); // Movimiento complementario opuesto para torque
    }
  }
}