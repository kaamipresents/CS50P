# JSON Conversion
import json

data = {"name": "Kami", "age": 25}
jstring = json.dumps(data)
pObject = json.loads(jstring)
print(pObject["name"])