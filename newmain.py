import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import messaging

import datetime
import serial
import time

class OnionSense:

    def __init__(self) :
         '''
        Initialize a machine object
        '''
         cred = credentials.Certificate('account.json')
         app = firebase_admin.initialize_app(cred)
         db = firestore.client()
         
         parameters_ref = db.collection('parameters')
         rows_ref = db.collection('rows')
         harvests_ref = db.collection('harvests')
         users_ref= db.collection('users')
         arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)

    def send_command(self, command: int):
        '''
        Send command to Arduino
        can be used to explicitly invoke Arduino operation without calling specific functions\n

        Parameters:
        command(int): Command to send
        '''
        if(command in self.available_commands):
            self.arduino.write(bytes(str(command)+'\n','utf-8'))
        else:
            raise Exception('Unknown command')
    
    def get_arduino_response(self)->str:
        '''
        Get arduino serial response

        Returns:
        response(str): Arduino response
        '''
        try:
            response = self.arduino.readline().decode('utf-8').rstrip
        except UnicodeDecodeError:
            response = self.arduino.readline().decode('utf-8').rstrip
        return response
    

    
    def get_data(self)-> dict:
        '''
        Get current data from sensors

        Returns:
        parameters(dict): Parameters including message indicating succes or fail
        '''
        self.send_command(0)
        response = self.get_arduino_response()

        while not response:
            self.get_arduino_response()

        data = response.split()
        try:
             humidity = float(data[1])
             soil_moisture = float(data[2])*100
             lux = float(data[3])
             proximity_sensor_1 = int(data[4])
             proximity_sensor_2 = int(data[5])
             proximity_sensor_3 = int(data[6])
             proximity_sensor_4 = int(data[7])
             proximity_sensor_5 = int(data[8])
             
             parameters = {
                 'soil': soil_moisture,
                 'humidity': humidity,
                 'temperature': temperature,
                 'light': lux,
                 'r1': (proximity_sensor_1),
                 'r2': (proximity_sensor_2),
                 'r3': (proximity_sensor_3),
                 'r4': (proximity_sensor_4),
                 'r5': (proximity_sensor_5),
                 'success': True
             }
             
        except:
            parameters = {
             'success':False
             }
        return parameters
    


    def update_parameters(self, parameters:dict):
        '''
        Add new parameter entry in firebase

        Parameters:
        parameters(dict): Dict containing parameters\n
        Sample format:
            parameters = {\n
            'soil': soil_moisture, \n
            'humidity': humidity, \n
            'temperature': temperature, \n
            'light': lux, \n
            }
        '''
        data = {
            'soil': parameters['soil'],
            'humidity':parameters['humidity'],
            'temperature': parameters['temperature'],
            'light': parameters ['lux'],
            'created_at': datetime.datetime.now(tz=datetime.timezone.utc)
        }
        self.parameter_reference.add(data)



    def update_harvest_rows(self, parameters: dict):
        '''
        [To Update]

        Add/ update harvest rows entry in firebase

        Parameters:
        parameters(dict): Dict containing harvest rows \n
        Sample format:
            parameters = {\n
                'r1': proximity_sensor_1, \n
                'r2': proximity_sensor_2, \n
                'r3': proximity_sensor_3, \n
                'r4': proximity_sensor_4, \n
                'r5': proximity_sensor_5, \n
        }
        '''

        data = {
            'r1': parameters['proximity_sensor_1'],
            'r2': parameters['proximity_sensor_2'],
            'r3': parameters['proximity_sensor_3'],
            'r4': parameters['proximity_sensor_4'],
            'r5': parameters['proximity_sensor_5'],
            'created_at': datetime.datetime.now(tz=datetime.timezone.utc)
        }
        self.row_reference.add(data)



    def add_harvest(self, amount:float):
        '''
        Add a new harvest entry in firebase

        Parameters:
        amount(float): Amount of harvest in kg
        '''
        data = {
            'amount': amount,
            'created_at': datetime.datetime.now(tz=datetime.timezone.utc)
        }
        self.parameter_reference.add(data)
    


    def _get_user_token(self)-> list:
        '''
        Get all existing user tokens from firebase

        Returns:
        tokens (list): List of all retrieved tokens
        '''
        tokens = []
        users = self.user_reference.stream()
        for user in users:
            tokens.append(user.id)
        return tokens
    

    def send_notification(self, title: str, body: str):
        '''
        Send a notification to all users

        Parameters:
        title(str): Title message
        body(str): Message content
        '''
        message = messaging.MulticastMessage(
            notification = messaging.Notification(
                title = title,
                body= body,
            ),
            tokens = self._get_user_tokens()
        )

    
    def turn_on_fan(self):
        '''
        Explicit function calling turnOnFan in arduino
        '''
        self.send_command(1)


    def turn_off_fan(self):
        '''
        Explicit function calling turnOffFan in arduino
        '''
        self.send_command(2)

    def turn_on_sprinkler(self):
        '''
        Explicit function turnOnSprinkler in arduino
        '''
        self.send_command(3)

    def turn_off_sprinkler(self):
        '''
        Explicit function turnOffSprinkler
        '''
        self.send_command(4)

    def get_internet_datetime(self)-> datetime.datetime:
        '''
        Get datetime from internet

        Returns:
        datetime(datetime.datetime): Current datetime
        '''
        response = urlopen('http://just-the-time.appspot.com/')
        datetime_str = response.read().strip().decode('utf-8')
        _datetime = datetime.datetime.striptime(datetime_str,'%Y-%m-%d %H:%M:%S')
        _datetime = datetime + datetime.timedelta(hours = 8)
        return _datetime
    

 