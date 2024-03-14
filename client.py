from pprint import pprint

import requests

u = input()
if u == "1":
    response = requests.post('http://localhost:5000/user/',
                             json={"password": "12345", "name": "user_4"})
elif u == "2":
    response = requests.patch('http://localhost:5000/user/10',
                              json={'name': 'owner'})
elif u == "3":
    response = requests.delete('http://localhost:5000/user/20')
elif u == "4":
    response = requests.get('http://localhost:5000/user/20')

# print((response.json())['error'])
pprint(response.text)
print(response.status_code)
