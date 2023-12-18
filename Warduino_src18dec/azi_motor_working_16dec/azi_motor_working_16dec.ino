//AZIMUTH 16-12-2023 Working

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);

int fwd = 11;  // ForwardP
int bck = 12;  // Backward
int pwm = 10;  // Motor power

int htb = 13;  // Heartbeat

int FWD_EL = 5;
int BCK_EL = 3;
int PWM_EL = 4;

int nano_az_cw_acw_switch = 6;   // AZNano ------d5
int AZ_nanoCounterResetPin = 7;  // AZNano ------d4

int nano_ele_cw_acw_switch =25;  // ELNano ------d4
int EL_nanoCounterResetPin = 24;  // ELNano ------d5

String timeString;
String DIR_CW_ACW;

bool CW = true;
bool EL_CW = false;

String location;
String satname;
float AZ_extractedData = 0;
float EL_extractedData = 0;
float repos_amt = 0;
float azi = 229;
float ele = 0;

float currentAZ = 0;
float prevAZ = 0;
int motion = 0;
float currentELE = 0;
float prevELE = 0;
int ELEmotion = 0;

float current_azi = 0;
float previous_azi = 0;
float current_ele = 0;
float previous_ele = 0;
float AZ_difference = 0;

int speed = 35;
int ELspeed = 75;

void setup() {
  pinMode(pwm, OUTPUT);
  pinMode(fwd, OUTPUT);
  pinMode(bck, OUTPUT);
  pinMode(htb, OUTPUT);
  pinMode(FWD_EL, OUTPUT);
  pinMode(BCK_EL, OUTPUT);
  pinMode(PWM_EL, OUTPUT);


  pinMode(AZ_nanoCounterResetPin, OUTPUT);
  pinMode(nano_az_cw_acw_switch, OUTPUT);

  pinMode(EL_nanoCounterResetPin, OUTPUT);
  pinMode(nano_ele_cw_acw_switch, OUTPUT);

  Serial.begin(115200);
  Serial1.begin(115200);
  Serial2.begin(115200);
  Serial3.begin(115200);

  lcd.init();
  lcd.backlight();
  lcd.clear();

  digitalWrite(AZ_nanoCounterResetPin, HIGH);
  digitalWrite(EL_nanoCounterResetPin, HIGH);
  delay(1000);  // Nano AZ ELE Reset
  digitalWrite(AZ_nanoCounterResetPin, LOW);
  digitalWrite(EL_nanoCounterResetPin, LOW);
 
}


void loop() {
  
   
  //Serial.println(String(String(AZ_extractedData) + " | " + String(EL_extractedData)));

  serial_1_TTL();
  serial_2_NANO();
 
  serial_3_NANO();

  cw_ccw();
 
  el_cw_ccw();

  switchDirection();
 
  EL_switchDirection();

  checkAziMotorPos();
 
  checkELEMotorPos();
  
}
