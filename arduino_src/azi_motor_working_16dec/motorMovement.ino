void checkRotation() {
  float AZ_difference = 0;
  
  currentAZ = azi;

  AZ_difference = currentAZ - prevAZ;
  AZ_difference = abs(AZ_difference);
  
  if (AZ_difference >= 5) {
    motion = 0;
    Serial.println("change in deg > 3 : continue motion");

  }
  else {
    motion = 1;
  }
  prevAZ = currentAZ;
}


void cw_ccw() {
  current_azi = azi;
 
 Serial.println(motion);
 
  if (current_azi > previous_azi)    {
    
      CW = true;  //forward
       
  }
  if (current_azi < previous_azi)  {
   
      CW = false;  //forward
       
  }
  previous_azi = current_azi;
}
void switchDirection() {
  if (CW) {
    digitalWrite(bck, LOW);
    digitalWrite(fwd, HIGH);
    digitalWrite(nano_az_cw_acw_switch, HIGH);
  }
  if (!CW) {
    digitalWrite(fwd, LOW);
    digitalWrite(bck, HIGH);
    digitalWrite(nano_az_cw_acw_switch, LOW);
  }
}

void moveAziMotor(int speed, int dly) {
 if(motion == 1){
  if (speed != 0) {
    analogWrite(pwm, speed);
    delay(dly);
    analogWrite(pwm, 0);
  } else {
    analogWrite(pwm, 0);
  }
 }
}


void checkAziMotorPos() {
   
  String output = String(azi - 0.67) + " " + String(extractedData) + " " + String(azi + 0.67);
  Serial.println(output);
  if (extractedData >= (azi - 0.67) and extractedData <= (azi + 0.67)) {
    String output = String(azi - 0.67) + ">=" + String(extractedData) + "<=" + String(azi + 0.67);
    Serial.println(output);
    moveAziMotor(0, 5);
  } else {
    moveAziMotor(speed, 10);
  }
}

 

void stopMotor() {
  analogWrite(pwm, 0);
}