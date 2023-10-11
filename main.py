import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import messaging

import datetime
import serial
import time


cred = credentials.Certificate('account.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

parameters_ref = db.collection('parameters')
rows_ref = db.collection('rows')
harvests_ref = db.collection('harvests')
users_ref= db.collection('users')

arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)


notif_row1 = False
notif_row1_start = datetime.datetime.now()
 
notif_row2= False
notif_row2_start = datetime.datetime.now()

notif_row3 = False
notif_row3_start = datetime.datetime.now()

notif_row4 = False
notif_row4_start = datetime.datetime.now()

notif_row5 = False
notif_row5_start = datetime.datetime.now()

def get_conditions():
    while True:
        arduino.write(bytes('0\n','utf-8'))
        response = arduino.readline().decode('utf-8').rstrip()
        if response and response !='92':
            return response
        
def turn_on_fan():
    while True:
        arduino.write(bytes('1/n','utf-8'))
        response = arduino.readline().decode('utf-8').rstrip()
        if response:
            return response
        
def turn_off_fan():
    while True:
        arduino.write(bytes('2/n','utf-8'))
        response = arduino.readline().decode('utf-8').rstrip()
        if response:
            return response
        
def turn_on_sprinkler():
    while True:
        arduino.write(bytes('3/n','utf-8'))
        response = arduino.readline().decode('utf-8').rstrip()
        if response:
            return response

def turn_off_sprinkler():
    while True:
        arduino.write(bytes('4/n','utf-8'))
        response = arduino.readline().decode('utf-8').rstrip()
        if response:
            return response

        
def get_keys():
    keys = []
    users = users_ref.stream()
    
    for user in users:
        keys.append(user.id)
    return keys

def send_notification(title, body):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title= title,
            body= body,
        ),
        tokens= get_keys()
    )

if __name__ == '__main__':

    while True:
        response = get_conditions()
        data = response.split(' ')
        print (data)
        print (response)
        temperature = float(data[0])
        humidity = float(data[1])
        soil_moisture = float(data[2])*100
        lux = float(data[3])
        proximity_sensor_1 = int(data[4])
        proximity_sensor_2 = int(data[5])
        proximity_sensor_3 = int(data[6])
        proximity_sensor_4 = int(data[7])
        proximity_sensor_5 = int(data[8])
        
        if temperature > 26:
           print(turn_on_fan())
        else:
            temperature < 25
            print(turn_off_fan())
           
        if humidity > 50:
           print(turn_on_fan())
        else:
            humidity < 70
            print(turn_off_fan())

        if soil_moisture < 60:
            print(turn_on_sprinkler())  
        elif soil_moisture > 60:
           print(turn_off_sprinkler())
        
        if proximity_sensor_1 == 1:
            if not notif_row1:
                send_notification(
                    'Harvest Ready',
                    'Row 1 is ready to harvest. Please check'
                )
                notif_row1 = True
                notif_row1_start = datetime.datetime.now()

        if (datetime.datetime.now()- notif_row1_start) >= datetime.timedelta(minutes = 30):
            notif_row1= False

        if proximity_sensor_2 == 1:
           if not notif_row2:
                send_notification(
                    'Harvest Ready',
                    'Row 2 is ready to harvest. Please check'
                )
                notif_row2 = True
                notif_row2_start = datetime.datetime.now()
            

        if (datetime.datetime.now()- notif_row2_start) >= datetime.timedelta(minutes = 30):
            notif_row2= False
            
        if proximity_sensor_3 == 1:
            if not notif_row3:
                send_notification(
                    'Harvest Ready',
                    'Row 3 is ready to harvest. Please check'
                )
                notif_row3 = True
                notif_row3_start = datetime.datetime.now()
            

        if (datetime.datetime.now()- notif_row3_start) >= datetime.timedelta(minutes = 30):
            notif_row3= False

        if proximity_sensor_4 == 1:
            if not notif_row4:
                send_notification(
                    'Harvest Ready',
                    'Row 4 is ready to harvest. Please check'
                )
                notif_row4 = True
                notif_row4_start = datetime.datetime.now()
            

        if (datetime.datetime.now()- notif_row4_start) >= datetime.timedelta(minutes = 30):
            notif_row4= False

        if proximity_sensor_5 == 1:
          if not notif_row5:
                send_notification(
                    'Harvest Ready',
                    'Row 5 is ready to harvest. Please check'
                )
                notif_row5 = True
                notif_row5_start = datetime.datetime.now()
            

        if (datetime.datetime.now()- notif_row5_start) >= datetime.timedelta(minutes = 30):
            notif_row5= False

        data = {
            'soil': soil_moisture,
            'humidity': humidity,
            'temperature': temperature,
            'light': lux,
            'created_at': datetime.datetime.now(tz=datetime.timezone.utc)
        }
        parameters_ref.add(data)
        
        rows = {
            'r1': bool(proximity_sensor_1),
            'r2': bool(proximity_sensor_2),
            'r3': bool(proximity_sensor_3),
            'r4': bool(proximity_sensor_4),
            'r5': bool(proximity_sensor_5),
            'created_at': datetime.datetime.now(tz=datetime.timezone.utc)
        }
        rows_ref.add(rows)

        time.sleep(5)