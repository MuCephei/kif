from twilio.rest import Client


def send_text(user_info, body=None):
    client = Client(user_info['AccountSID'], user_info['Auth'])

    client.messages.create(to=user_info['to_num'],
                           from_=user_info['from_num'],
                           body=body)
