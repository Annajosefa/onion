from onionsense import OnionSense
import time

machine = OnionSense()
while True:
    parameters = machine.get_data()
    print(parameters)
    time.sleep(7)




