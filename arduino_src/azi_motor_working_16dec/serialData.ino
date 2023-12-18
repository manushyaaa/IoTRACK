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

  }
}


void serial_2_NANO(){
  if (Serial2.available() > 0) {
        String receivedData = Serial2.readStringUntil('~');
        
        int startIdx = receivedData.indexOf("AA|");
        int endIdx = receivedData.indexOf("|ZZ");
        if (startIdx != -1 && endIdx != -1) {
            extractedData = receivedData.substring(startIdx + 3, endIdx).toFloat();
            lcd.setCursor(0,2);
            String output = " " + String(extractedData) + " ";
            lcd.print(output);
        }
    }
}

// void userInputSerial(){
//   if (Serial.available() > 0) {
//     // Read the entire line until a newline character is encountered
//    userInput = Serial.readStringUntil('\n');
//    stopAngle = userInput.toFloat();

//     // Print the received input
//     Serial.print("Set degree to : ");
//     Serial.println(userInput);
    
//   }
// }