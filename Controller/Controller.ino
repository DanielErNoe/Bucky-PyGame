#include <string.h>

int Knapp = 2;
int xPin = 0;
int yPin = 1;

int knappStatus = 0;
int xVerdi = 0;
int yVerdi = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(100);
}

void loop() {
  // put your main code here, to run repeatedly:
  knappStatus = digitalRead(Knapp);
  xVerdi = analogRead(xPin);
  yVerdi = analogRead(yPin);
  Serial.println("b" + String(knappStatus) + "x" + String(xVerdi) + "y" + String(yVerdi));
}
