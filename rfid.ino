#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define SS_PIN 10  // SDA (SS) to Digital Pin 10
#define RST_PIN 9  // RST to Digital Pin 9
#define BUZZER_PIN 2  // Buzzer connected to Digital Pin 2
#define LED_PIN 3     // LED connected to Digital Pin 3

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance
LiquidCrystal_I2C lcd(0x27, 16, 2); // Set LCD address to 0x27, 16 chars, 2 lines

void setup() {
  Serial.begin(9600);     // Start Serial Monitor
  SPI.begin();            // Start SPI Communication
  mfrc522.PCD_Init();     // Initialize MFRC522
  lcd.init();             // Initialize the LCD
  lcd.backlight();        // Turn on the LCD backlight
  pinMode(BUZZER_PIN, OUTPUT); // Set buzzer pin as output
  pinMode(LED_PIN, OUTPUT);    // Set LED pin as output

  lcd.setCursor(0, 0);
  lcd.print("Scan your card");
  Serial.println("Show your card:");
}

void loop() {
  // Look for new cards
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // Show UID on serial monitor
  Serial.println();
  Serial.print("UID tag: ");
  String content = "";

  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }

  content.toUpperCase();
  Serial.println();

  lcd.clear();
  lcd.setCursor(0, 0);

  // Change these UIDs as per your RFID card/tag
  if (content.substring(1) == "59 53 45 18" || 
      content.substring(1) == "24 65 3A A7") {
    Serial.println("Authorized Access");
    lcd.print("Present");
    digitalWrite(LED_PIN, LOW); // Ensure LED is off for authorized access
  } else {
    Serial.println("Access Denied");
    lcd.print("Access Denied");
    // Activate buzzer and LED for unauthorized access
    digitalWrite(BUZZER_PIN, HIGH);
    digitalWrite(LED_PIN, HIGH); // Turn on LED
    delay(1000); // Buzzer sounds and LED stays on for 1 second
    digitalWrite(BUZZER_PIN, LOW);
    digitalWrite(LED_PIN, LOW); // Turn off LED
  }

  delay(2000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Scan your card");
}