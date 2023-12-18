String ver = "AZ ENCODER 18 DEC 2023";

const int phototransistorPin = 2;  // You can change the pin number based on your connection
volatile int encoderCount = 0;
volatile bool lastState = HIGH;
int cw_acw_pin = 4;       //d25 ----mega
int counterResetPin = 5;  //d24----mega

bool cw = true;
bool reset = false;

void setup() {
  pinMode(phototransistorPin, INPUT);
  pinMode(cw_acw_pin, INPUT);
  pinMode(counterResetPin, INPUT);

  Serial.begin(115200);
  Serial.println(ver);
}

void loop() {
  if (digitalRead(counterResetPin) == HIGH) {
    encoderCount = 0;
  }

  if (digitalRead(cw_acw_pin) == HIGH) {
    cw = true;
  } else {
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
    if (cw) {
      encoderCount++;
    } else {
      encoderCount--;
    }
    //Serial.println("Make detected");
  }

  // Check for a falling edge
  if (currentState == LOW && lastState == HIGH) {
    if (cw) {
      encoderCount++;
    } else {
      encoderCount--;
    }
    //Serial.println("Break detected");
  }

  // Check if encoderCount has changed
  static int previousEncoderCount = encoderCount;
  if (encoderCount != previousEncoderCount) {
    // Update the previous value
    previousEncoderCount = encoderCount;

    if (encoderCount > 270) {
      encoderCount = 0;
    }
    if (encoderCount < 0) {
      encoderCount = 270;
    }
    double AZ_Angle = encoderCount * 1.3333333333;

    String outputString = "AA|" + String(AZ_Angle, 2) + "|ZZ~";
    Serial.println(outputString);
    delay(7);
    Serial.println(outputString);
    delay(13);
    Serial.println(outputString);
    delay(17);
  }

  // Update the last state
  lastState = currentState;
}
