const int phototransistorPin = 2;  // You can change the pin number based on your connection
volatile int encoderCount = 0;
volatile bool lastState = HIGH;
int cw_acw_pin = 5; //d6 ----mega
int counterResetPin = 4 ; //d7 ----mega

bool cw = true ;
bool reset = false ; 

void setup() {
  pinMode(phototransistorPin, INPUT);
  pinMode(cw_acw_pin , INPUT);
  pinMode(counterResetPin , INPUT);

  Serial.begin(115200);
}

void loop() {
  // Print the encoder count to the serial port
  //Serial.print("Encoder Count: ");
  //Serial.println(encoderCount);

  if (digitalRead(counterResetPin) == HIGH){
    encoderCount = 0;
  } 

  if(digitalRead(cw_acw_pin) == HIGH){
    cw = true ;
  }
  else{
    cw = false;
  }
  // Add any other code you need in the loop here
  updateEncoder();

  delay(30);  // Adjust the delay as needed to control the rate of serial output
}

void updateEncoder() {
  // Read the current state of the phototransistor
  bool currentState = digitalRead(phototransistorPin);
 
  // Check for a rising edge
  if (currentState == HIGH && lastState == LOW) {
    if (cw){
      encoderCount++;
    }else {
      encoderCount--;
    }
    //Serial.println("Make detected");
  }

  // Check for a falling edge
  if (currentState == LOW && lastState == HIGH) {
    if (cw){
      encoderCount++;
    }else {
      encoderCount--;
    }
    //Serial.println("Break detected");
  }
 
  if (encoderCount > 270){
    encoderCount = 0;
  }
  if (encoderCount < 0){
    encoderCount = 270;
  }
  double AZ_Angle = encoderCount * 1.3333333333;
 
  String outputString = "AA|" + String(AZ_Angle, 2) + "|ZZ~";

  Serial.println(outputString);
  // Update the last state
  lastState = currentState;
}
