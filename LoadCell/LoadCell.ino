int sensor = A0;
int value = 0;

void setup(){
  pinMode(sensor, INPUT);
  Serial.begin(9600);
}

void loop(){
  value = analogRead(sensor);
  Serial.println(value);
  delay(100);
}
