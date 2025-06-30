#include <Servo.h>

Servo thumbServo;
Servo indexServo;
Servo middleServo;
Servo ringServo;
Servo pinkyServo;

String fingerData = "";  
void setup() {
  Serial.begin(9600);

  thumbServo.attach(3);    // PWM pin D3
  indexServo.attach(4);    // PWM pin D5
  middleServo.attach(5);   // PWM pin D6
  ringServo.attach(6);     // PWM pin D7
  pinkyServo.attach(7);    // PWM pin D4

}

void loop() {
  if (Serial.available()) {
    char ch = Serial.read();
    if (ch == '\n') {
      if (fingerData.length() == 5) {
        setFingerPositions(fingerData);
      }
      fingerData = ""; 
    } else {
      fingerData += ch; 
    }
  }
}

void setFingerPositions(String fingers) {
  // Curl = 0° (closed), Open = 90° (neutral)
  thumbServo.write(fingers[0] == '1' ? 160 : 0);
  indexServo.write(fingers[1] == '1' ? 180 : 0);
  middleServo.write(fingers[2] == '1' ? 0 : 180);
  ringServo.write(fingers[3] == '1' ? 0 : 180);
  pinkyServo.write(fingers[4] == '1' ? 180 : 0);
}
