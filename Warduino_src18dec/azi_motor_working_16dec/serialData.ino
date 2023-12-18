void serial_1_TTL() {
   
  if (Serial1.available() > 0) {
    currentAZ = azi ;
    String receivedString = Serial1.readStringUntil('\n');  // Read until newline character
    Serial.println(receivedString);
    int space1 = receivedString.indexOf(' ');
    int space2 = receivedString.indexOf(' ', space1 + 1);
    int space3 = receivedString.indexOf(' ', space2 + 1);
    int space4 = receivedString.indexOf(' ', space3 + 1);
    int space5 = receivedString.indexOf(' ', space4 + 1);
    int space6 = receivedString.indexOf(' ', space5 + 1);
    int space7 = receivedString.indexOf(' ', space6 + 1);

    timeString = receivedString.substring(0, space1);

    azi = receivedString.substring(space1 + 1, space2).toFloat();
    ele = receivedString.substring(space2 + 1, space3).toFloat();

    satname = receivedString.substring(space3 + 1, space4);

    DIR_CW_ACW = receivedString.substring(space4 + 1, space5);
    repos_amt = receivedString.substring(space5 + 1, space6).toFloat();

    lcd.setCursor(14, 0);
    lcd.print(repos_amt);

    lcd.setCursor(0, 0);
    lcd.print(timeString);

    lcd.setCursor(0, 1);
    lcd.print(satname);

    lcd.setCursor(0, 3);
    String str_a = String(azi) + " " + String(ele);
    lcd.print(str_a);

    checkRotation();
    ELEcheckRotation();
 

  }
}


void serial_2_NANO() {
    if (Serial2.available() > 0) {
        String AZreceivedData = Serial2.readStringUntil('~');

        if (AZreceivedData.indexOf("AA|") != -1 && AZreceivedData.indexOf("|ZZ") != -1) {
            int startIdx = AZreceivedData.indexOf("AA|");
            int endIdx = AZreceivedData.indexOf("|ZZ");

            AZ_extractedData = AZreceivedData.substring(startIdx + 3, endIdx).toFloat();

            lcd.setCursor(0, 2);
            String output = " " + String(AZ_extractedData) + " ";
            lcd.print(output);
        } else {
            Serial.println(String("Warning AZ : Data integrity check failed : " + String(AZreceivedData)));
        }
    }
}



void serial_3_NANO() {
    if (Serial3.available() > 0) {
        String ELreceivedData  = Serial3.readStringUntil('~');
        if (ELreceivedData.indexOf("EE|") != -1 && ELreceivedData.indexOf("|LL") != -1) {
            int startIdx = ELreceivedData.indexOf("EE|");
            int endIdx = ELreceivedData.indexOf("|LL"); 

            EL_extractedData = ELreceivedData.substring(startIdx + 3, endIdx).toFloat();

            lcd.setCursor(10, 2);
            String output = " " + String(EL_extractedData) + " ";
            lcd.print(output);
        } else {
            Serial.println(String("Warning ELE : Data integrity check failed : " + String(ELreceivedData)));
        }
    }
}

 