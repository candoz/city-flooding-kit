#define LED 13
#define BUTTON 7

int button_state = 0;
bool was_low = true;

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(BUTTON, INPUT);
  Serial.begin(9600);
}

void loop() {
  button_state = digitalRead(BUTTON);

  if (Serial.available()) {
    char incoming = Serial.read();
    if (incoming == 'H') {
      digitalWrite(LED, HIGH);
    }
    if (incoming == 'L') {
      digitalWrite(LED, LOW);
    }
  }

  if (button_state == HIGH) {
    if (was_low == true) {
      Serial.print('B');  // (B)utton pressed once
      was_low = false;
    }
  }
  else {
    was_low = true;
  }

}
