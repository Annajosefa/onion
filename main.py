import serial
import time

import RPi.GPIO as GPIO

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
        print(response)
        data = response.split(' ')
        print(data)
        temperature = float(data[0])
        humidity = float(data[1])
        soil_moisture = float(data[2])
        lux = float(data[3])
        proximity_sensor_1 = int(data[4])
        
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
