// Esempio 01: accendi il led appena è premuto il pulsante
 
#define LED 13                // LED collegato al pin digitale 13
#define BUTTON 7              // pin di input dove è collegato il pulsante
int buttonState = 0;// si userà val per conservare lo stato del pin di input
 
 
void setup() {
  pinMode(LED, OUTPUT);       // imposta il pin digitale come output
  pinMode(BUTTON, INPUT);   // imposta il pin digitale come input
  Serial.begin(9600);
}
 
void loop() {
  buttonState = digitalRead(BUTTON);
  if (Serial.available()) {
    char incoming = Serial.read();
    Serial.print(""+incoming);
    if (incoming == "1") {
      digitalWrite(LED, HIGH);
    }
  }

  if (buttonState == HIGH){
    digitalWrite(LED, LOW);
    Serial.print("0");
  }

  
}
