#include <dht.h> 
#include "Arduino.h" 
#include <Wire.h> 
#include <BH1750.h> 
#include <HX711.h>
 
 
dht DHT; 
BH1750 lightMeter; 
 
HX711 scale;
float w1, w2, previous = 0;
 
 
int dhtPin = 6; 
int proximitySensor1 = 7; 
int proximitySensor2 = 8; 
int proximitySensor3 = 9; 
int proximitySensor4 = 10; 
int proximitySensor5 = 11; 
int lightPin = 3; 
int fanPin = 4; 
int sprinklerPin = 5; 
uint8_t dataPin = 12;
uint8_t clockPin = 13;
const int sensorPin1 = A0; 
const int sensorPin2 = A1; 
const int sensorPin3 = A2; 
const int sensorPin4 = A3; 
 
String command = ""; 
int current_command = -1; 
 
void setup() { 
  Serial.begin(9600); 
 
  scale.begin(dataPin, clockPin);
 
  pinMode(proximitySensor1, INPUT_PULLUP); 
  pinMode(proximitySensor2, INPUT_PULLUP); 
  pinMode(proximitySensor3, INPUT_PULLUP); 
  pinMode(proximitySensor4, INPUT_PULLUP); 
  pinMode(proximitySensor5, INPUT_PULLUP); 
 
  pinMode(fanPin, OUTPUT); 
  pinMode(sprinklerPin, OUTPUT); 
  pinMode(lightPin, OUTPUT);
 
 
  pinMode (A0, INPUT); 
  Wire.begin(); 
  lightMeter.begin();
 
 
  scale.set_scale(409.07428571);
  scale.tare(); 
 
} 
 
void loop(){ 
  if(current_command == -1){ 
    receiveCommand(); 
  } 
 
  else if(current_command == 0){ 
    sendState();
    current_command = -1; 
  } 
 
  else if (current_command == 1){
    turnOnFan();
    current_command = -1;
  }
 
  else if(current_command == 2){
    turnOffFan();
    current_command =-1;
  }
 
  else if(current_command == 3){
    turnOnSprinkler();
    current_command= -1;
  }
 
  else if(current_command == 4){
    turnOffSprinkler();
    current_command= -1;
  }
 
  else if(current_command == 5){
    turnOnLight();
    current_command = -1;
  }
 
  else if (current_command == 6){
    turnOffLight();
    current_command = -1;
  }
 
  else if (current_command == 7){
    getWeight();
    current_command = -1;
  }
 
 
} 
 
void receiveCommand(){
  if(Serial.available()){
    int sent = Serial.readStringUntil('\n').toInt();
    Serial.println("ok");
    current_command = sent;   
  }
}
 
void sendState(){ 
  /*
   * Get all conditions 
   */
 DHT.read22(dhtPin);
 String message = String(getTemperature()) + " " + String(getHumidity()) + " " + String(getAverageMoisturePercentage()) + " " + String(getLux()) + " " + String(getProximitySensor1()) + " " + String(getProximitySensor2()) + " " + String(getProximitySensor3()) + " " + String(getProximitySensor4()) + " " + String(getProximitySensor5()); 
Serial.println(message);
} 
 
float getTemperature(){ 
  /* 
   * Get current room temperature 
   */ 
  float temperature = DHT.temperature; 
  return temperature; 
 
} 
 
float getHumidity(){ 
  /* 
   * Get current humidity level 
   */ 
  float humidity = DHT.humidity; 
  return humidity; 
 
}  
 
float getAverageMoisturePercentage (){ 
  /* 
   * Get current moisture level 
   */ 
  float sensorReading1 = (analogRead(sensorPin1) / 1023) * 100;
  float sensorReading2 = (analogRead(sensorPin1) / 1023) * 100;
  float sensorReading3 = (analogRead(sensorPin1) / 1023) * 100;
  float sensorReading4 = (analogRead(sensorPin1) / 1023) * 100;

  float totalPercentage = sensorReading1 + sensorReading2 + sensorReading3 + sensorReading4;
 
  float averageMoisturePercentage = totalPercentage / 4;
  return averageMoisturePercentage; 
} 
 
int getProximitySensor1(){ 
  /* 
   * Check if an object is detected on Proximity Sensor 1 
   */ 
  int state = digitalRead(proximitySensor1); 
  return state; 
} 
 
int getProximitySensor2(){ 
  /* 
   * Check if an object is detected on Proximity Sensor 2
   */ 
  int state = digitalRead(proximitySensor2); 
  return state; 
} 
 
 
int getProximitySensor3(){ 
  /* 
   * Check if an object is detected on Proximity Sensor 3
   */ 
  int state = digitalRead(proximitySensor3); 
  return state; 
} 
 
int getProximitySensor4(){ 
  /* 
   * Check if an object is detected on Proximity Sensor 4
   */ 
  int state = digitalRead(proximitySensor4); 
  return state; 
} 
 
 
int getProximitySensor5(){ 
  /* 
   * Check if an object is detected on Proximity Sensor 5
   */ 
  int state = digitalRead(proximitySensor5); 
  return state; 
} 
 
float getLux (){ 
  /* 
   * Get current light level 
   */ 
  float Lux =lightMeter.readLightLevel();
  return Lux;
}
 
void getWeight(){
  /*
  Get cuurent weight
  */
  w1 = scale.get_units(10);
  delay(100);
  w2 = scale.get_units();
  while (abs(w1-w2)>10)
  {
    w1 = w2;
    w2 = scale.get_units();
    delay (100);
  }
  double kilogram = w1/1000;
  Serial.println(String(kilogram));
}
 
 
void turnOnFan(){
  digitalWrite(fanPin, HIGH);
}
 
void  turnOffFan(){
  digitalWrite(fanPin,LOW);
}
 
void turnOnSprinkler(){
  digitalWrite(sprinklerPin, HIGH);
}
 
void turnOffSprinkler(){
  digitalWrite(sprinklerPin, LOW);
}
 
void turnOnLight(){
  digitalWrite(lightPin, HIGH);
}
 
void turnOffLight(){
  digitalWrite(lightPin, LOW);
}
