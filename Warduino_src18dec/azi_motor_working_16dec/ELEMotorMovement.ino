void ELEcheckRotation() {
  float ELE_difference = 0;

  currentELE = ele;

  ELE_difference = currentELE - prevELE;
  ELE_difference = abs(ELE_difference);
  if (currentELE > prevELE and EL_extractedData >= 90 or EL_extractedData <=0 ){
     ELEmotion = 0;
  }
  else{
    ELEmotion = 1;
  }
  if(currentELE < 0 or EL_extractedData < 0 or currentELE > 90 or EL_extractedData > 91){
    ELEmotion = 0;
  }
  else {
    ELEmotion = 1;
  }
  prevELE = currentELE;
}

void el_cw_ccw() {
  current_ele = ele;
  if (current_ele > previous_ele) {
    EL_CW = false;  //forward
  }
  if (current_ele < previous_ele) {
    EL_CW = true;  //backward
  }
  previous_ele = current_ele;
}
void EL_switchDirection() {
  if (EL_CW) {
    digitalWrite(BCK_EL, LOW);
    digitalWrite(FWD_EL, HIGH);
    digitalWrite(nano_ele_cw_acw_switch, LOW);
  }
  if (!EL_CW) {
    digitalWrite(FWD_EL, LOW);
    digitalWrite(BCK_EL, HIGH);
    digitalWrite(nano_ele_cw_acw_switch, HIGH);
  }
}

void moveELEMotor(int ELspeed, int dly) {
  if (ELEmotion) {
    if (ELspeed != 0) {
      analogWrite(PWM_EL, ELspeed);
      delay(dly);
      analogWrite(PWM_EL, 0);
    } else {
      analogWrite(PWM_EL, 0);
    }
  }
}

void checkELEMotorPos() {

  //String output = String(ele - 0.67) + " " + String(EL_extractedData) + " " + String(ele + 0.67);
  //Serial.println(output);
  if (EL_extractedData >= (ele - 0.67) and EL_extractedData <= (ele + 0.67)) {
    //String output = String(ele - 0.67) + ">=" + String(EL_extractedData) + "<=" + String(ele + 0.67);
    //Serial.println(output);
    moveELEMotor(0, 0);
  } else {
    moveELEMotor(ELspeed, 50);
  }
}
