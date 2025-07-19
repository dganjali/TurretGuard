#include <Servo.h>

Servo myServo;
int servoPin = 9;
int currentPos = 90; // Start at midpoint

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);
  myServo.write(currentPos);  // Initial position
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');

    int azimuth = 0;
    int elevation = 0;
    int fire = 0;

    int aIndex = input.indexOf("A:");
    int eIndex = input.indexOf("E:");
    int fIndex = input.indexOf("F:");

    int semicolon1 = input.indexOf(';');
    int semicolon2 = input.indexOf(';', semicolon1 + 1);

    if (aIndex != -1 && eIndex != -1 && fIndex != -1) {
      String aValue = input.substring(aIndex + 2, semicolon1);
      azimuth = aValue.toInt();

      String eValue = input.substring(eIndex + 2, semicolon2);
      elevation = eValue.toInt();

      String fValue = input.substring(fIndex + 2);
      fire = fValue.toInt();

      Serial.print("Azimuth: ");
      Serial.println(azimuth);
      Serial.print("Elevation: ");
      Serial.println(elevation);
      Serial.print("Fire: ");
      Serial.println(fire);

      // Movement logic
      if (azimuth > 2 && currentPos > 0) {
        currentPos -= 1;
      } else if (azimuth < -2 && currentPos < 180) {
        currentPos += 1;
      } else if (azimuth == 0) {
        // Gently return to center if not already centered
        if (currentPos < 90) {
          currentPos += 1;
        } else if (currentPos > 90) {
          currentPos -= 1;
        }
      }

      // Write to servo only if changed
      myServo.write(currentPos);
      Serial.print("Servo position: ");
      Serial.println(currentPos);
    }
  }
}
