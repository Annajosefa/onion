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
int lightPin = 3; 
int fanPin = 4; 
int sprinklerPin = 5; 
 
const int sensorPin1 = A0; 
const int sensorPin2 = A1; 
const int sensorPin3 = A2; 
const int sensorPin4 = A3; 
    
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


  scale.set_scale(calibration_factor);
  scale.tare();
} 
 
 
 
void loop(){ 
  if(current_command == -1){ 
    receiveCommand(); 
  } 
  else if(current_command == 0){ 
    getConditions(); 
    current_command = -1; 
  } 
 
 else if (current_command ==1){
  turnonfan();
  current_command = -1;
  }

 else if(current_command == 2){
  turnofffan();
  current_command =-1;
  }

  else if(cuurent_command == 3){
    turnonsprinkler();
    current_command= -1;
  }

  else if(current_command == 4){
    turnoffsprinkler();
    current_command= -1;
  }

  else if(current_command== 5){
    getWeight();
    Serialprinln(getWeight());
    current_command = -1;
  }
} 

 
void sendState(){ 
  DHT.read22(dhtPin); 
  String condition = String(getTemperature()) + " " + String(getHumidity()) + " " + String(getAverageMoisturePercentage()) + " " + String(getLux()) + " " + String(getProximitySensor1()) + " " + String(getProximitySensor2()) + " " + String(getProximitySensor3()) + " " + String(getProximitySensor4()) + " " + String(getProximitySensor5()); 
  sendResponse(condition); 
  
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
  int sensorAnalog; 
  sensorAnalog = {analogRead(sensorPin1), analogRead(sensorPin2), analogRead(sensorPin3), analogRead(sensorPin4)};
  float totalPercentage = 0;
for (int i=0; i<4; i++) {
  totalPercentage += ( 100 - ( (sensorAnalog/1023.00) * 100) );
}
  float averageMoisturePercentage = total percentage/4;
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
 float Lux =lightMeter.readLightLevel();
 return Lux;
}

float getWeight(){
  /*
  get current weight*/
  unit = scale.get_units(), 10;
  if (units<0)
  {
    units = 0.00
  }
  float final_weight= (units * 0.001);
  return final weight;
}

void turnonfan(){
  digitalWrite(fanPin, HIGH);
}

void  turnofffan(){
  digitalwrite(fanPin,LOW);
}

void turnonsprinkler(){
  digitalWrite(sprinklerPin, HIGH);
}

void turnofffan(){
  digitalwrite(sprinklerPin, LOW);
}