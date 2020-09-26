

def send_sms_to_phone(mobile):
    r = requests.post(
        "http://api.sparrowsms.com/v2/sms/",
        data={'token' : settings.SPARROW_SMS_TOKEN,
        'from'  : settings.SMS_FROM,
        'to'    : mobile,
        'text'  : 'your mobile verification code is  ' + str(key)})

    status_code = r.status_code
    response = r.text
    response_json = r.json()
    print(status_code)
    print(response_json)
    print(key)
    return status_code
