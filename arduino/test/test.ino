const int num = 13;

void setup() {
  // put your setup code here, to run once:
  pinMode(num, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("start");
  digitalWrite(num, LOW);
  delay(5000);
  Serial.println("on");
  digitalWrite(num, HIGH);
  delay(5000);
}
