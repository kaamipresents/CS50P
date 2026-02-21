import requests
import json

r = requests.get('https://itunes.apple.com/search?entity=song&limit=1&term=weezer')
response = r.json()
print(json.dumps(response, indent=2))


# print(response['results'][0]['trackName'])