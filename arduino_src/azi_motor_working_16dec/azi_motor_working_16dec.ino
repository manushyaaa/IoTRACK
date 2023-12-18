//AZIMUTH 16-12-2023 Working

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define GROUP_SIZE 10

LiquidCrystal_I2C lcd(0x27, 20, 4);

int fwd = 11;                 // ForwardP
int bck = 12;                 // Backward
int htb = 13;                 // Heartbeat
int pwm = 10;                 // Motor power
int nano_az_cw_acw_switch = 6;        //Nano ------d5
int nanoCounterResetPin = 7;  // Nano ------d4

String timeString;
String DIR_CW_ACW;

bool CW = true;

String location;
String satname;
float extractedData = 0;
float repos_amt = 0;
float azi = 0;
float ele = 0;
String userInput;

  float currentAZ = 0 ;
  float prevAZ = 0 ; 
  int  motion = 0 ; 


float current_azi = 0;
float previous_azi = 0;
float AZ_difference = 0;
 
int speed = 80;

void setup() {
  pinMode(pwm, OUTPUT);
  pinMode(fwd, OUTPUT);
  pinMode(bck, OUTPUT);
  pinMode(htb, OUTPUT);
  pinMode(nanoCounterResetPin, OUTPUT);
  pinMode(nano_az_cw_acw_switch , OUTPUT);

  Serial.begin(115200);
  Serial1.begin(115200);
  Serial2.begin(115200);

  lcd.init();

  lcd.backlight();
  lcd.clear();

  digitalWrite(nanoCounterResetPin, HIGH);
  delay(1000);  // Nano
  digitalWrite(nanoCounterResetPin, LOW);
}


void loop() {

  serial_1_TTL();
  serial_2_NANO();
 
  cw_ccw();  
  switchDirection();
  // String output =   String(extractedData) + " | " + String(azi) + " | " + String(CW_ACW);
  // Serial.println(output);

  checkAziMotorPos();
   

  // userInputSerial();
 
}
