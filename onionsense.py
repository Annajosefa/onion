import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import messaging
from urllib.request import urlopen

import datetime
import serial
import RPi.GPIO as GPIO
import time
import threading
import logging

class OnionSense:


    def __init__(self, logging_level: int = logging.INFO):
        '''
        Initialize a machine object

        Parameters:
        logging_level (int) : Logging level (use logging)
        '''
        self.__initialize_logger(logging_level)

        cred = credentials.Certificate('account.json')
        app = firebase_admin.initialize_app(cred)
        db = firestore.client()
        self.logger.info('Database initialized')
        
        self.parameter_reference = db.collection('parameters')
        self.row_reference = db.collection('rows')
        self.harvest_reference = db.collection('harvests')
        self.user_reference = db.collection('users')
        self.state_reference = db.collection('states').document('current')
        self.state_reference.on_snapshot(self._on_state_change)

        self.arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
        self.logger.info('Arduino initialized successfully')

        # Enter all available commands here
        self.available_commands = [0, 1, 2, 3, 4, 5, 6, 7] 

        self.light_is_on = False
        self.fan_is_on = False
        self.sprinkler_is_on = False
        self.machine_state = False
        self.harvest_mode = False
        self.harvest_toggle_button_pin = 27
        self.confirm_weight_pin = 22
        self.button_pin = 17
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(self.harvest_toggle_button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(self.confirm_weight_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.button_pin, GPIO.RISING, callback = self._switch_state, bouncetime = 2000)
        GPIO.add_event_detect(self.harvest_toggle_button_pin, GPIO.RISING, callback = self._toggle_harvest_mode, bouncetime = 2000)
        GPIO.add_event_detect(self.confirm_weight_pin, GPIO.RISING, callback = self._confirm_harvest, bouncetime = 2000)
        self.logger.info('GPIO related initialized successfully')

        initial_state = {
            'power': False,
            'fan': False,
            'light': False,
            'sprinkler': False
        }
        self.state_reference.update(initial_state)
        self.logger.info('All parameters set to False')
        self.firebase_logger.info(f'[state][current](update) : {initial_state}')



    def __initialize_logger(self, logging_level):
        format = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s.')
        main_handler = logging.FileHandler('onionsense.log')
        main_handler.setFormatter(format)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(main_handler)
        self.logger.setLevel(logging_level)

        firebase_handler = logging.FileHandler('firebase.log')
        firebase_handler.setFormatter(format)
        self.firebase_logger = logging.getLogger('firebase')
        self.firebase_logger.addHandler(firebase_handler)
        self.logger.setLevel(logging_level)



    def send_command(self, command: int):
        '''
        Send command to Arduino
        can be used to explicitly invoke Arduino operation without calling specific functions\n

        Parameters:
        command(int): Command to send
        '''
        self.logger.debug(f'Sent command to Arduino: {command}')
        if(command in self.available_commands):
            while True:
                self.arduino.write(bytes(str(command)+'\n','utf-8'))
                time.sleep(0.5)
                response = self.get_arduino_response()
                if (response  == 'ok'):
                    break
        else:
            raise Exception('Unknown command')
    


    def get_arduino_response(self) -> str:
        '''
        Get arduino serial response

        Returns:
        response(str): Arduino response
        '''
        try:
            response = self.arduino.readline().decode('utf-8').rstrip()
        except UnicodeDecodeError:
            response = self.arduino.readline().decode('utf-8').rstrip()
        self.logger.debug(f'Got response from arduino: {response}')
        return response
    

    
    def get_data(self) -> dict:
        '''
        Get current data from sensors

        Returns:
        parameters(dict): Parameters including message indicating succes or fail
        '''
        self.send_command(0)
        response = self.get_arduino_response()

        while not response:
            response = self.get_arduino_response()

        data = response.split()
        try:
            temperature = float(data[0])
            humidity = float(data[1])
            soil_moisture = float(data[2]) 
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
                'r1': proximity_sensor_1,
                'r2': proximity_sensor_2,
                'r3': proximity_sensor_3,
                'r4': proximity_sensor_4,
                'r5': proximity_sensor_5,
                'success': True
            }
        except:
            parameters ={
                'success':False
            }
        
        self.logger.debug(f'Got parameters from Arduino: {parameters}')
        return parameters
    
    def get_weight(self):
        '''
        Explicit function calling weight in arduino
        '''
        self.send_command(7)
        time.sleep(1)
        response = self.get_arduino_response()
        try: 
            weight = float(response)
        except Exception as e:
            self.logger.warn(f'Got response: {response}')
            self.logger.error(f'Exception: {e}')
            while not response:
                response = self.get_arduino_response()
                if response:
                    weight = float(response)
                    break 
        self.logger.debug(f'Got weight: {weight}')
        if weight <= 0:
            return self.get_weight()
        self.logger.debug(f'Got final weight: {weight}')
        return weight/1000
        


    def update_parameters(self, parameters: dict):
        '''
        Add new parameter entry in firebase

        Parameters:
        parameters(dict): Dict containing parameters\n
        Sample format:
            ```python
            parameters = {
            'soil': soil_moisture,
            'humidity': humidity,
            'temperature': temperature,
            'light': lux,
            }
            ```
        '''
        data = {
            'soil': parameters['soil'],
            'humidity':parameters['humidity'],
            'temperature': parameters['temperature'],
            'light': parameters ['light'],
            'created_at': datetime.datetime.now(tz=datetime.timezone.utc)
        }
        self.parameter_reference.add(data)
        self.logger.info(f'Parameters updated: {data}')
        self.firebase_logger.info(f'[parameters](update) : {data}')



    def update_harvest_rows(self, parameters: dict):
        '''
        Add/ update harvest rows entry in firebase

        Parameters:
        parameters(dict): Dict containing harvest rows \n
        Sample format:
            ```python
            parameters = {
                'r1': proximity_sensor_1,
                'r2': proximity_sensor_2,
                'r3': proximity_sensor_3,
                'r4': proximity_sensor_4,
                'r5': proximity_sensor_5,
            ```
        }
        '''

        data = {
            'r1': bool(parameters['r1']),
            'r2': bool(parameters['r2']),
            'r3': bool(parameters['r3']),
            'r4': bool(parameters['r4']),
            'r5': bool(parameters['r5']),
            'created_at': datetime.datetime.now(tz=datetime.timezone.utc)
        }
        self.row_reference.document('current').set(data)
        self.logger.info(f'Rows updated: {data}')
        self.firebase_logger.info(f'[rows](update) : {data}')



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
        self.harvest_reference.add(data)
        self.logger.info(f'Harvest added: {amount}')      
        self.firebase_logger.info(f'[harvest](add) : {amount}')      
        


    def _get_user_tokens(self) -> list:
        '''
        Get all existing user tokens from firebase

        Returns:
        tokens (list): List of all retrieved tokens
        '''
        tokens = []
        users = self.user_reference.stream()
        for user in users:
            tokens.append(user.id)
        self.firebase_logger.info(f'[users]: {tokens}')
        return tokens
    

    def send_notification(self, title: str, body: str):
        '''
        Send a notification to all users

        Parameters:
        title (str): Title message
        body (str): Message content
        '''
        message = messaging.MulticastMessage(
            notification = messaging.Notification(
                title=title,
                body=body,
            ),
            tokens = self._get_user_tokens()
        )
        messaging.send_multicast(message)
        self.logger.info(f'Notification sent: [{title}]({body})')


    
    def set_power(self, state: bool):
        '''
        Set power/machine state

        Parameters (bool) : Machine state
        '''
        if state and not self.machine_state:
            self.machine_state = True
            self.state_reference.update({
                'power': True,
                'updated_at': datetime.datetime.now(tz=datetime.timezone.utc)
            })
            self.logger.info(f'Power state set to True')
        if not state and self.machine_state:
            self.machine_state = False
            self.state_reference.update({
                'power': False,
                'updated_at': datetime.datetime.now(tz=datetime.timezone.utc)
            })
            self.logger.info(f'Power state set to False')



    def set_fan(self, state: bool):
        '''
        Turn fan on or off

        Parameters:
        state (bool) : Fan state
        '''
        if state and not self.fan_is_on:
            self.send_command(1)
            self.fan_is_on = True
            self.state_reference.update({
                'fan': True,
                'updated_at': datetime.datetime.now(tz=datetime.timezone.utc)
            })
            self.logger.info(f'Fan state set to True')
        if not state and self.fan_is_on:
            self.send_command(2)
            self.fan_is_on = False
            self.state_reference.update({
                'fan': False,
                'updated_at': datetime.datetime.now(tz=datetime.timezone.utc)
            })
            self.logger.info(f'Fan state set to False')



    def set_sprinkler(self, state: bool):
        '''
        Turn sprinkler on or off

        Parameters:
        state (bool) : Sprinkler state
        '''
        if state and not self.sprinkler_is_on:
            self.send_command(3)
            self.sprinkler_is_on = True
            self.state_reference.update({
                'sprinkler': True,
                'updated_at': datetime.datetime.now(tz=datetime.timezone.utc)
            })
            self.logger.info(f'Sprinkler state set to True')
        if not state and self.sprinkler_is_on:
            self.send_command(4)
            self.sprinkler_is_on = False
            self.state_reference.update({
                'sprinkler': False,
                'updated_at': datetime.datetime.now(tz=datetime.timezone.utc)
            })
            self.logger.info(f'Sprinkler state set to False')



    def set_light(self, state: bool):
        '''
        Turn light on or off

        Parameters:
        state (bool) : Light state
        '''
        if state and not self.light_is_on:
            self.send_command(5)
            self.light_is_on = True
            self.state_reference.update({
                'light': True,
                'updated_at': datetime.datetime.now(tz=datetime.timezone.utc)
            })
            self.logger.info(f'Light state set to True')
        if not state and self.light_is_on:
            self.send_command(6)
            self.light_is_on = False
            self.state_reference.update({
                'light': False,
                'updated_at': datetime.datetime.now(tz=datetime.timezone.utc)
            })
            self.logger.info(f'Light state set to False')



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
    


    def _switch_state(self, channel):
        '''
        Callback function for toggling power state
        '''
        self.machine_state = not self.machine_state
        self.state_reference.update({
            'power': self.machine_state,
            'updated_at': datetime.datetime.now(tz=datetime.timezone.utc)
        })
        self.logger.info(f'[Callback] Power state set to {self.machine_state}')



    def _toggle_harvest_mode(self, channel):
        '''
        Callback function for toggling harvest mode
        '''
        if self.machine_state:
            self.harvest_mode = not self.harvest_mode
            self.logger.info(f'[Callback] Harvest mode set to {self.harvest_mode}')
        else:
            self.logger.info(f'[Callback] Tried toggling harvest mode but not powered on')



    def _confirm_harvest(self, channel):
        '''
        Callback function for confirming harvest value
        '''
        if self.harvest_mode:
            weight = self.get_weight()
            self.add_harvest(weight)
            self.logger.info(f'[Callback] Weight confirmed: {weight}')
        else:
            self.logger.info(f'[Callback] Tried confirm weight but not on harvest mode')


    
    def _on_state_change(self, doc_snapshot, changes, read_time):
        '''
        Callback function for detected changes in
        state coming from Firebase
        '''
        state = doc_snapshot[-1].to_dict()
        self.firebase_logger.info(f'[states][current](read) : {state}')
        self.set_power(state['power'])
        self.set_fan(state['fan'])
        self.set_light(state['light'])
        self.set_sprinkler(state['sprinkler'])
        
    