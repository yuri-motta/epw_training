
int analogX = 4;
int analogY = 5;

int X = 0;
int Y = 0;


void setup() {
  Serial.begin(9600); // use the same baud-rate as the python side
}
void loop() {

  X = analogRead(analogX);
  Y = analogRead(analogY);
  
  Serial.print("X:"); // write a string
  Serial.println(X); // write a string

  Serial.print("Y:"); // write a string
  Serial.println(Y); // write a string
  
  delay(100);
}
