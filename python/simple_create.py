import requests
import json



URL = 'https://eventsource.firebaseio-demo.com/.json'

msg = {
	'text': 'Test', 
	'client': 'wang'
}

to_post = json.dumps(msg)
requests.post(URL, data=to_post)


