from firebase_admin import messaging
from firebase_admin import credentials
from firebase_admin import initialize_app
 
 
cred = credentials.Certificate("account.json")
default_app = initialize_app(cred)
 
registration_tokens = [
    'dV0VKRS1QyKYYMnWWG45qk',
    'cl0KYYh3TDS25mvr6teECU:APA91bEEOt-sYsr8BQ9VgltO9YyMHslGSJEWKlg6EGhmmeFKGMxxNHtKKLD23I0a_qcoOKzJTnM0VxlH23QiQbsrD-dnoyI2j4RCHic-dKpQl_Aw4Rt0sq1DALr3X4fi0re9nD4O3BPe',
]
topic = 'notification'
response = messaging.subscribe_to_topic(registration_tokens, topic)
 
print(response.success_count, 'tokens were subscribed successfully')
 
message = messaging.MulticastMessage(
    notification=messaging.Notification(
        title='Onion Harvest',
        body='No plant detected, check for harvest',
    ),
    tokens=registration_tokens,
)
topic = topic,
response = messaging.send_multicast(message)
 
print('{0} messages were sent successfully'.format(response.success_count))

