import requests
import json

url = "https://api.funtranslations.com/translate/"
# Replace with any other to translate accordingly
str="yoda.json"
api_url=url+str
text = "This is the text to be translated"
data = json.dumps({"text":text})
res = requests.post(
                    api_url,
                    data=data
                   )
print(res.text)
