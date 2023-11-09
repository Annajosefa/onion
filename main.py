from onionsense import OnionSense

import time
import datetime

if __name__ == '__main__':
    '''
    Entry point for program
    '''
    machine = OnionSense()

    fan_is_on = False
    sprinkler_is_on = False
    light_is_on = False

    paused = True

    notification_ready_1 = True
    notification_ready_2 = True
    notification_ready_3 = True
    notification_ready_4 = True
    notification_ready_5 = True

    last_notification_1 = datetime.datetime.now()
    last_notification_2 = datetime.datetime.now()
    last_notification_3 = datetime.datetime.now()
    last_notification_4 = datetime.datetime.now()
    last_notification_5 = datetime.datetime.now()

    time_light_switched = datetime.datetime.now()



    while True:
        if machine.machine_state:
            machine.turn_on_light()
            paused = False
            light_is_on = True

            time_since_last_start = datetime.datetime.now() - time_light_switched
            if time_since_last_start >= datetime.timedelta(hours=12):
                if light_is_on:
                    machine.turn_off_light()
                    light_is_on = False
                else:
                    machine.turn_on_light()
                    light_is_on = True
                time_light_Switched = datetime.datetime.now()


            parameters = machine.get_data()
            print(parameters)
            if not parameters ('success'):
                continue

            if parameters['temperature'] > 25:
                if not fan_is_on:
                    machine.turn_on_fan()
                    fan_is_on = True

            else:
                if fan_is_on:
                    machine.turn_off_fan()
                    fan_is_on = False

            if parameters['soil']< 30:
                if not sprinkler_is_on:
                    machine.turn_on_sprinkler()
                    sprinkler_is_on = True

            else:
                if sprinkler_is_on:
                    machine.turn_off_sprinkler()
                    sprinkler_is_on = False

            if parameters['r1'] == 0 and  notification_ready_1:
                machine.send_notification(
                    title= 'Harvest Ready',
                    body= 'Harvest is ready in Row 1. Please collect!'
                )
                notification_ready_1 = False
                last_notification_1 = datetime.date.now()

            if not notification_ready_1 \
                and (datetime.datetime.now() - last_notification_1) >= datetime.timedelta(minutes=30):
                notification_ready_1 = True



            if parameters['r2'] == 0 and  notification_ready_2:
                machine.send_notification(
                    title= 'Harvest Ready',
                    body= 'Harvest is ready in Row 2. Please collect!'
                )
                notification_ready_2 = False
                last_notification_2 = datetime.date.now()

            if not notification_ready_2 \
                and (datetime.datetime.now() - last_notification_2) >= datetime.timedelta(minutes=30):
                notification_ready_2 = True



            if parameters['r3'] == 0 and  notification_ready_3:
                machine.send_notification(
                    title= 'Harvest Ready',
                    body= 'Harvest is ready in Row 3. Please collect!'
                )
                notification_ready_3 = False
                last_notification_3 = datetime.date.now()

            if not notification_ready_3 \
                and (datetime.datetime.now() - last_notification_3) >= datetime.timedelta(minutes=30):
                notification_ready_3 = True


                
            if parameters['r4'] == 0 and  notification_ready_4:
                machine.send_notification(
                    title= 'Harvest Ready',
                    body= 'Harvest is ready in Row 4. Please collect!'
                )
                notification_ready_4 = False
                last_notification_4 = datetime.date.now()

            if not notification_ready_4 \
                and (datetime.datetime.now() - last_notification_4) >= datetime.timedelta(minutes=30):
                notification_ready_4 = True



            if parameters['r5'] == 0 and  notification_ready_5:
                machine.send_notification(
                    title= 'Harvest Ready',
                    body= 'Harvest is ready in Row 5. Please collect!'
                )
                notification_ready_5 = False
                last_notification_5 = datetime.date.now()

            if not notification_ready_5 \
                and (datetime.datetime.now() - last_notification_5) >= datetime.timedelta(minutes=30):
                notification_ready_5 = True

            machine.update_parameters(parameters)

            time.sleep(7)  
        else:
            if not paused:
                paused = True

            if fan_is_on:
                machine.turn_off_fan()
                fan_is_on= False

            if sprinkler_is_on:
                machine.turn_off_sprinkler()
                sprinkler_is_on = False

            if light_is_on:
                machine.turn_off_light()
                light_is_on = False

            print('onionsense')          
