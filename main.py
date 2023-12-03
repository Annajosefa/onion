from onionsense import OnionSense

import time
import datetime
import logging

if __name__ == '__main__':
    '''
    Entry point for program
    '''
    machine = OnionSense(logging_level=logging.DEBUG)

    paused = True

    notification_ready_1 = True
    notification_ready_2 = True
    notification_ready_3 = True
    notification_ready_4 = True
    notification_ready_5 = True
    warning_notification_ready = True

    last_notification_1 = datetime.datetime.now()
    last_notification_2 = datetime.datetime.now()
    last_notification_3 = datetime.datetime.now()
    last_notification_4 = datetime.datetime.now()
    last_notification_5 = datetime.datetime.now()
    last_warning_notification = datetime.datetime.now()

    time_light_switched = datetime.datetime.now()

    while True:
        if machine.machine_state:
            if paused:
                machine.set_light(True)
                paused = False

            time_since_last_start = datetime.datetime.now() - time_light_switched
            if time_since_last_start >= datetime.timedelta(hours=12):
                if machine.light_is_on:
                    machine.set_light(False)
                else:
                    machine.set_light(True)
                time_light_switched = datetime.datetime.now()

            parameters = machine.get_data()

            if not parameters ['success']:
                if warning_notification_ready:
                    machine.send_notification(
                        title='Component failure encountered',
                        body='A component has malfunctioned'
                    )
                else:
                   if (datetime.datetime.now() - last_warning_notification) >= datetime.timedelta(minutes=5):
                       warning_notification_ready = True
                
                continue

            if parameters['temperature'] > 25:
                machine.set_fan(True)
            else:
                machine.set_fan(False)

            if parameters['soil']< 30:
                machine.set_sprinkler(True)
            else:
                machine.set_sprinkler(False)

            machine.update_parameters(parameters)
            time.sleep(5)  

            if machine.harvest_mode:
                continue
            
            if parameters['r1'] == 0 and  notification_ready_1:
                machine.send_notification(
                    title= 'Harvest Ready',
                    body= 'Harvest is ready in Row 1. Please collect!'
                )
                notification_ready_1 = False
                last_notification_1 = datetime.datetime.now()

            if not notification_ready_1 \
                and (datetime.datetime.now() - last_notification_1) >= datetime.timedelta(minutes=30):
                notification_ready_1 = True

            if parameters['r2'] == 0 and  notification_ready_2:
                machine.send_notification(
                    title= 'Harvest Ready',
                    body= 'Harvest is ready in Row 2. Please collect!'
                )
                notification_ready_2 = False
                last_notification_2 = datetime.datetime.now()

            if not notification_ready_2 \
                and (datetime.datetime.now() - last_notification_2) >= datetime.timedelta(minutes=30):
                notification_ready_2 = True

            if parameters['r3'] == 0 and  notification_ready_3:
                machine.send_notification(
                    title= 'Harvest Ready',
                    body= 'Harvest is ready in Row 3. Please collect!'
                )
                notification_ready_3 = False
                last_notification_3 = datetime.datetime.now()

            if not notification_ready_3 \
                and (datetime.datetime.now() - last_notification_3) >= datetime.timedelta(minutes=30):
                notification_ready_3 = True

            if parameters['r4'] == 0 and  notification_ready_4:
                machine.send_notification(
                    title= 'Harvest Ready',
                    body= 'Harvest is ready in Row 4. Please collect!'
                )
                notification_ready_4 = False
                last_notification_4 = datetime.datetime.now()

            if not notification_ready_4 \
                and (datetime.datetime.now() - last_notification_4) >= datetime.timedelta(minutes=30):
                notification_ready_4 = True

            if parameters['r5'] == 0 and  notification_ready_5:
                machine.send_notification(
                    title= 'Harvest Ready',
                    body= 'Harvest is ready in Row 5. Please collect!'
                )
                notification_ready_5 = False
                last_notification_5 = datetime.datetime.now()

            if not notification_ready_5 \
                and (datetime.datetime.now() - last_notification_5) >= datetime.timedelta(minutes=30):
                notification_ready_5 = True

        else:
            if not paused:
                paused = True

            machine.set_fan(False)
            machine.set_sprinkler(False)
            machine.set_light(False)
