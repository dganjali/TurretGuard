#include <Servo.h>

Servo myServo;
int servoPin = 9;
int currentPos = 90;
#define kP 1

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');

    int dx = 0;
    int dy = 0;
    int fire = 0;

    //"dx:4;dy:7;F:3\n"

    int aIndex = input.indexOf("dx:");
    int eIndex = input.indexOf("dy:");
    int fIndex = input.indexOf("F:");

    int semicolon1 = input.indexOf(';');
    int semicolon2 = input.indexOf(';', semicolon1 + 1);

    if (aIndex != -1 && eIndex != -1 && fIndex != -1) {
      String aValue = input.substring(aIndex + 2, semicolon1);
      dx = aValue.toInt();
      dx = (dx + 180)/2;

      String eValue = input.substring(eIndex + 2, semicolon2);
      dy = eValue.toInt();

      String fValue = input.substring(fIndex + 2);
      fire = fValue.toInt();

      Serial.print("dx: ");
      Serial.println(dx);
      Serial.print("dy: ");
      Serial.println(dy);
      Serial.print("Fire: ");
      Serial.println(fire);

    myServo.write(kP*dx);
      
    }
  }
}
