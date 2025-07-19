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

// Button pin
#define buttonPin 4
bool systemEnabled = false;

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);

  // Motor setup
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(R_EN, OUTPUT);
  pinMode(L_EN, OUTPUT);
  digitalWrite(R_EN, HIGH);
  digitalWrite(L_EN, HIGH);

  // Button setup
  pinMode(buttonPin, INPUT_PULLUP);  // active LOW
}

void loop() {
  // Wait for a one-time button press
  if (!systemEnabled) {
    if (digitalRead(buttonPin) == LOW) {
      delay(50);  // debounce
      if (digitalRead(buttonPin) == LOW) {
        systemEnabled = true;
        Serial.println("System Enabled");
      }
    }
    return; // Exit loop() until systemEnabled is true
  }

  // 🔁 Once enabled, this runs forever
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');

    int dx = 90;
    int dy = 0;
    int fire = 0;

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
        analogWrite(RPWM, 255);
        analogWrite(LPWM, 0);
        delay(900);
        analogWrite(RPWM, 0);
        analogWrite(LPWM, 0);
      }
    }
  }
}
