#include <Servo.h>

Servo myServo;
int currentPos = 90;
#define kP 2.5

// Motor control pins
#define RPWM 5
#define LPWM 6
#define R_EN 7
#define L_EN 8
#define servoPin 9

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);

  // Set motor control pins as outputs
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(R_EN, OUTPUT);
  pinMode(L_EN, OUTPUT);

  // Enable both sides
  digitalWrite(R_EN, HIGH);
  digitalWrite(L_EN, HIGH);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');

    int dx = 90;
    int dy = 0;
    int fire = 0;

    //"dx:4;dy:7;F:3\n"

    int aIndex = input.indexOf("dx:");
    int eIndex = input.indexOf("dy:");
    int fIndex = input.indexOf("F:");

    int semicolon1 = input.indexOf(';');
    int semicolon2 = input.indexOf(';', semicolon1 + 1);

    if (aIndex != -1 && eIndex != -1 && fIndex != -1) {
      String aValue = input.substring(aIndex + 3, semicolon1);
      dx = aValue.toInt();

      String eValue = input.substring(eIndex + 3, semicolon2);
      dy = eValue.toInt();

      String fValue = input.substring(fIndex + 2);
      fire = fValue.toInt();

      myServo.write((2 * dx + 180) / 2);

      if (fire >= 0.9 && abs(dx) < 5) {
        // Spin motor forward at full speed
        analogWrite(RPWM, 255);
        analogWrite(LPWM, 0);
        delay(900); // Adjust time as needed
        analogWrite(RPWM, 0);
        analogWrite(LPWM, 0);
      }
    }
  }
}