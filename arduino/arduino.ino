#include <dht.h>
#include "Arduino.h"
#include <Wire.h>
#include <BH1750.h>
 
 
dht DHT;
BH1750 lightMeter;
 
int dhtPin = 6;
int proximitySensor1 = 7;
int proximitySensor2 = 8;
int proximitySensor3 = 9;
int proximitySensor4 = 10;
int proximitySensor5 = 11;
int fanPin = 5;
int sprinklerPin = 4;
 
const int sensorPin = A0;
 
String command = "";
int current_command = -1;
 
void setup() {
  Serial.begin(9600);
  pinMode(proximitySensor1, INPUT_PULLUP);
  pinMode(proximitySensor2, INPUT_PULLUP);
  pinMode(proximitySensor3, INPUT_PULLUP);
  pinMode(proximitySensor4, INPUT_PULLUP);
  pinMode(proximitySensor5, INPUT_PULLUP);
  pinMode(fanPin, OUTPUT);
  pinMode(sprinklerPin, OUTPUT);
 
  pinMode (A0, INPUT);
  Wire.begin();
  lightMeter.begin();
}
 
 
 
void loop(){
  if(current_command == -1){
    receiveCommand();
  }
  else if(current_command == 0){
    getConditions();
    current_command = -1;
  }
  else if(current_command == 1){
    turnOnFan();
  }
  else if (current_command == 2){
    turnOffFan();
  }
 
  else if(current_command == 3){
    turnOnSprinkler();
  }
  else if(current_command == 4) {
    turnOffSprinkler();
  }
}
void sendResponse(String response){
  /*
   * Send response to the Raspberry Pi
   */
  Serial.println(response);    
}
 
void receiveCommand(){
  /*
   * Get and return command from Raspberry Pi
   */
  if(Serial.available()){
    int sent = Serial.readStringUntil('\n').toInt();
    current_command = sent;
  }
}
 
void getConditions(){
  DHT.read22(dhtPin);
  String condition = String(getTemperature()) + " " + String(getHumidity()) + " " + String(getMoisturePercentage()) + " " + String(getLux()) + " " + String(getProximitySensor1()) + " " + String(getProximitySensor2()) + " " + String(getProximitySensor3()) + " " + String(getProximitySensor4()) + " " + String(getProximitySensor5());
  sendResponse(condition);
 
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
 
float getMoisturePercentage (){
  /*
   * Get current moisture level
   */
  int sensorAnalog;
  sensorAnalog = analogRead(sensorPin);
  float MoisturePercentage = ( 100 - ( (sensorAnalog/1023.00) * 100) );
  return MoisturePercentage;
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
   * Check if an object is detected on Proximity Sensor 1
=======
 int getProximitySensor2(){
  /*
   * Check if an object is detected on Proximity Sensor 2
>>>>>>> cefd6f0b6cb96a651ad7d0dff768de5faefb3e94
   */
  int state = digitalRead(proximitySensor2);
  return state;
}
 
 
int getProximitySensor3(){
  /*
   * Check if an object is detected on Proximity Sensor 1
=======
 
 int getProximitySensor3(){
  /*
   * Check if an object is detected on Proximity Sensor 3
>>>>>>> cefd6f0b6cb96a651ad7d0dff768de5faefb3e94
   */
  int state = digitalRead(proximitySensor3);
  return state;
}
 
int getProximitySensor4(){
  /*
   * Check if an object is detected on Proximity Sensor 1
   */
  int state = digitalRead(proximitySensor4);
  return state;
}
 
 
int getProximitySensor5(){
  /*
   * Check if an object is detected on Proximity Sensor 1
=======
 
int getProximitySensor5(){
  /*
   * Check if an object is detected on Proximity Sensor 5
>>>>>>> cefd6f0b6cb96a651ad7d0dff768de5faefb3e94
   */
  int state = digitalRead(proximitySensor5);
  return state;
}
 
float getLux (){
  /*
   * Get current light level
   */
 float Lux = lightMeter.readLightLevel();
 return Lux;
}
 
void turnOnFan(){
  digitalWrite(fanPin, LOW);

  sendResponse("92");
}
void turnOffFan(){
  digitalWrite(fanPin, HIGH);

  
  sendResponse("92");
}
 
void turnOnSprinkler(){
  digitalWrite(sprinklerPin,LOW);

  sendResponse("92");
}
void turnOffSprinkler(){
  digitalWrite(sprinklerPin,HIGH);

  
  sendResponse("92");
}
 
 
