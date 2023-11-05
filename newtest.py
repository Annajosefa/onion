from onionsense import OnionSense

machine = OnionSense()

parameters = { 
            'soil': 25.5, 
            'humidity': 60.1, 
            'temperature': 27.40, 
            'light': 6700.0, 
            } 

machine.update_parameters(parameters)



