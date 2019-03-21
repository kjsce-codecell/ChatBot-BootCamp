from flask import Flask, request, make_response, jsonify
import json
import requests

app = Flask(__name__)
url = 'https://api.funtranslations.com/translate/'

@app.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True)
  print(req)
  try:
    intent = req.get('queryResult').get('intent').get('displayName')
  except AttributeError:
    return 'json error'
  print('Intent: ' + intent)
  if intent == 'Translation Init':
    fulfillment = req.get('queryResult').get('fulfillmentText')
    language = req.get('queryResult').get('parameters').get('Language')[0]
    return make_response(jsonify({'fulfillmentText': fulfillment,'followupEventInput': {'name': 'Translate','parameters':{'language':language},'languageCode': 'en-US'}}))
  elif intent == 'Translate':
    query = req.get('queryResult').get('queryText')
    language = req.get('queryResult').get('parameters').get('language')
    payload = {'text':query}
    final_url = url + language + '.json'
    res = requests.post(final_url,params=payload)
    if res.status_code == 200:
      text = res.json()["contents"]["translated"]
    else:
      print(res.status_code)
      text = "request overlimit"
    return make_response(jsonify({'fulfillmentText': text}))
  else:
    return make_response(jsonify({'fulfillmentText': 'Apna Time Aega'}))

if __name__ == '__main__':
  app.run()