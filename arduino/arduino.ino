#include<dht.h>
#include "Arduino.h"
#include <Wire.h>
#include <BH1750.h>
 
 
dht DHT;
BH1750 lightMeter;
 
int dhtPin = 8;
int proximitySensor1 = 7;
const int sensorPin = A0;
 
String command = "";
int current_command = -1;
 
void setup() {
  Serial.begin(9600);
  pinMode(proximitySensor1, INPUT);
  pinMode (A0, INPUT);
  Wire.begin();
  lightMeter.begin();
}
 
void loop (){
  if(current_command == -1){
    receiveCommand();
  }
 
  else if(current_command == 0){
    getConditions();
    current_command = -1;
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
    Serial.println("ok");
    current_command = sent;
  }
}
 
void getConditions(){
  DHT.read22(dhtPin);
  String condition = String(getTemperature()) + " " + String(getHumidity()) + " " + String(getMoisturePercentage()) + " " + String(getLux()) + " " + String(getProximitySensor1());
  sendResponse("92");
  Serial.println(condition);
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
 
float getLux (){
  /*
   * Get current light level
   */
 float Lux = lightMeter.readLightLevel();
 return Lux;
}
