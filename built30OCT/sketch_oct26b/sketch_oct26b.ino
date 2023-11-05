#include "LiquidCrystal.h"

const int rs = A5, en = A7, d4 = A10, d5 = A11, d6 = A12, d7 = A13;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

unsigned long previousMillis = 0;
const long interval = 1000;

void setup() {
  
  // Set up pins for LCD backlight, read/write, VCC, and GND
  pinMode(A15, OUTPUT);  // PIN 16 BLK
  pinMode(A14, OUTPUT);  // PIN 15 BLA
  pinMode(A6, OUTPUT);   // PIN 5 RW
  pinMode(A4, OUTPUT);   // PIN 2 VCC
  pinMode(A3, OUTPUT);   // PIN 1 GND

  digitalWrite(A15, LOW);  // PIN 16 BLK (Negative)
  digitalWrite(A14, HIGH); // PIN 15 BLA (Positive)P
  digitalWrite(A6, LOW);   // PIN 5 RW (Negative)
  digitalWrite(A4, HIGH);  // PIN 2 VCC (Positive)
  digitalWrite(A3, LOW);   // PIN 1 GND (Negative)

  
  lcd.begin(20, 4);
  Serial.begin(115200);
  Serial2.begin(115200);
 
}
 

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    if (Serial2.available() > 0) {
      String data = Serial2.readStringUntil('\n'); // Read data from Serial
      Serial.println(data);

      // Split the data into individual variables
      String time;
      String date;
      float azi;
      float ele;

      int timePos = 0;
      int datePos = 9;
      int aziPos = 18;
      int elePos = 25;

      if (data.length() >= elePos) {
        time = data.substring(timePos, datePos - 1);
        date = data.substring(datePos, aziPos - 1);
        azi = data.substring(aziPos, elePos - 1).toFloat() ;
        ele = data.substring(elePos).toFloat()  ;

        Serial.println("Parsed successfully");
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Time: " + time);
        lcd.setCursor(0, 1);
        lcd.print("Date: " + date);
        lcd.setCursor(0, 2);
        lcd.print("Azi: " + String(azi, 2)); // Display azi with 2 decimal places
        lcd.setCursor(0, 3);
        lcd.print("Ele: " + String(ele, 2)); // Display ele with 2 decimal places
      }
    }
  }
}
