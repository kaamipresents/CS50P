# requests + JSON
import requests
import json

r = requests.get('https://jsonplaceholder.typicode.com/todos/1')
pObject = json.loads(r)
print(r.status_code)
print(pObject['title'])
