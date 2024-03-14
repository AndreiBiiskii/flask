from pprint import pprint

import requests
from werkzeug.security import generate_password_hash, check_password_hash


u = input()
if u == "1":
    response = requests.post('http://localhost:5000/user/',
                             json={"password": generate_password_hash("12345"), "name": "user10", "email": "ddddd@mail.ru"})
elif u == "2":
    response = requests.patch('http://localhost:5000/user/1',
                              json={'name': 'owner'})
elif u == "3":
    response = requests.delete('http://localhost:5000/user/5')
elif u == "4":
    response = requests.get('http://localhost:5000/user/5')

elif u == "5":
    response = requests.post('http://localhost:5000/ads/',
                             json={"title": "news5", "description": "some text 5", "user_id": "6"})
elif u == "6":
    response = requests.get('http://localhost:5000/ads/1')

pprint(response.json())
print(response)
