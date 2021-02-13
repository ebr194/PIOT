import requests
import json
import os
#This is the code from the tutorial used for both bluetooth file and monitor and notify
# ACCESS_TOKEN = "zzz"
ACCESS_TOKEN = "o.qDZQiVGVJmguLjdCPxrSXN2o1Vu14LG8"

def send_notification_via_pushbullet(title, body):
    """ Sending notification via pushbullet.
        Args:
            title (str) : Title of text.
            body (str) : Body of text.
    """
    data = { "type": "note", "title": title, "body": body }

    response = requests.post("https://api.pushbullet.com/v2/pushes", data = json.dumps(data),
        headers = { "Authorization": "Bearer " + ACCESS_TOKEN, "Content-Type": "application/json" })

    if(response.status_code != 200):
        raise Exception()