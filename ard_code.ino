#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define RST_PIN 9
#define SS_PIN 10
#define SERVO_PIN 3
#define GREEN_LED_PIN 4
#define RED_LED_PIN 6

MFRC522 rfid(SS_PIN, RST_PIN);
Servo gateServo;

void smoothMove(int fromAngle, int toAngle, int stepDelay = 15) {
  if (fromAngle < toAngle) {
    for (int pos = fromAngle; pos <= toAngle; pos++) {
      gateServo.write(pos);
      delay(stepDelay);
    }
  } else {
    for (int pos = fromAngle; pos >= toAngle; pos--) {
      gateServo.write(pos);
      delay(stepDelay);
    }
  }
}

void setup() {
  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init();

  gateServo.attach(SERVO_PIN);
  gateServo.write(0);  // Start closed

  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);

  digitalWrite(GREEN_LED_PIN, LOW);
  digitalWrite(RED_LED_PIN, HIGH);  // Red ON when door closed

  delay(500);
  Serial.println("READY");
}

void loop() {
  // === Handle RFID ===
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    Serial.print("UID: ");
    for (byte i = 0; i < rfid.uid.size; i++) {
      if (rfid.uid.uidByte[i] < 0x10) Serial.print("0");
      Serial.print(rfid.uid.uidByte[i], HEX);
    }
    Serial.println();

    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
    delay(1000);
  }

  // === Handle Raspberry Pi Serial Command ===
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "OPEN") {
      Serial.println("OK");

      digitalWrite(RED_LED_PIN, LOW);     // Turn off red LED
      digitalWrite(GREEN_LED_PIN, HIGH);  // Turn on green LED

      smoothMove(0, 80);                  // Open gate
      delay(3000);                       // Wait 10 seconds
      smoothMove(80, 0);                  // Close gate

      digitalWrite(GREEN_LED_PIN, LOW);   // Turn off green LED
      digitalWrite(RED_LED_PIN, HIGH);    // Turn red LED back on
    }
  }
}
