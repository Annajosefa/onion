import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import datetime
import serial
import time

import RPi.GPIO as GPIO


cred = credentials.Certificate('account.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

parameters_ref = db.collection('parameters')
rows_ref = db.collection('rows')
harvests_ref = db.collection('harvests')
docs = db.collection('users')

exhaust_pin = 17
sprinkler_pin = 27
light_pin = 22
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
GPIO.setmode(GPIO.BCM)
GPIO.setup(exhaust_pin, GPIO.OUT)
GPIO.setup(sprinkler_pin, GPIO.OUT)
GPIO.setup(light_pin, GPIO.OUT)

exhaust_open = False
sprinkler_open = False
light_open = False

def get_conditions():
    while True:
        arduino.write(bytes('0\n','utf-8'))
        response = response = arduino.readline().decode('utf-8').rstrip()
        if response:
            return response

if __name__ == '__main__':

    while True:
        response = get_conditions()
        data = response.split(' ')
        temperature = float(data[0])
        humidity = float(data[1])
        soil_moisture = float(data[2])*100
        lux = float(data[3])
        proximity_sensor_1 = int(data[4])
        proximity_sensor_2 = int(data[5])
        proximity_sensor_3 = int(data[6])
        proximity_sensor_4 = int(data[7])
        proximity_sensor_5 = int(data[8])
        
        if temperature > 25:
            if not exhaust_open:
                exhaust_open = True
                GPIO.output(exhaust_pin, GPIO.HIGH)
        else:
            if exhaust_open:
                exhaust_open = False
                GPIO.output(exhaust_pin, GPIO.LOW)

        if humidity > 50:
            if not exhaust_open:
                exhaust_open = True
                GPIO.output(exhaust_pin, GPIO.HIGH)
        else:
            if exhaust_open:
                exhaust_open = False
                GPIO.output(exhaust_pin, GPIO.LOW)

        if soil_moisture < 50:
            if not sprinkler_open:
                    sprinkler_open = True
                    GPIO.output(sprinkler_pin, GPIO.HIGH)
        elif soil_moisture > 60:
            if sprinkler_open:
                sprinkler_open = False
                GPIO.output(sprinkler_pin, GPIO.LOW)

        if lux > 5400:
            if not light_open:
                light_open = True
                GPIO.output(light_pin, GPIO.HIGH)
        else:
            if light_open:
                light_open = True
                GPIO.output(light_pin, GPIO.LOW)
        
        if proximity_sensor_1 == 1:
            # Send notification
            pass

        if proximity_sensor_2 == 1:
            # Send notification
            pass

        if proximity_sensor_3 == 1:
            # Send notification
            pass

        if proximity_sensor_4 == 1:
            # Send notification
            pass

        if proximity_sensor_5 == 1:
            # Send notification
            pass

        data = {
            'soil': soil_moisture,
            'humidity': humidity,
            'temperature': temperature,
            'light': lux,
            'created_at': datetime.datetime.now(tz=datetime.timezone.utc)
        }
        parameters_ref.add(data)
        
        rows = {
            'r1': proximity_sensor_1,
            'r2': proximity_sensor_2,
            'r3': proximity_sensor_3,
            'r4': proximity_sensor_4,
            'r5': proximity_sensor_5,
            'created_at': datetime.datetime.now(tz=datetime.timezone.utc)
        }
        rows_ref.add(rows)

        docs =  db.collection('users').stream()
        fcm_keys = []
        for doc in docs:
            fcm_keys.append(doc.to_dict()['key'])
        time.sleep(5)