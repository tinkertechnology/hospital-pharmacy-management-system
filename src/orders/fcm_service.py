import requests
import json

def send_fcm_token_for_device(serverToken, deviceToken, order_id, status):

  headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
      }

  body = {
          'notification': {'title': 'Your order #' + order_id +' status : '+status,
                            'body': 'Thank you for your purchase'
                            },
          'to':
              '/topics/all', ##for all /topics/all , for individual deviceToken is passed
          'priority': 'high',
        #   'data': dataPayLoad,
        }
  response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
  print(response.status_code)

  print(response.json())