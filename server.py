from flask import Flask, request, make_response, jsonify
import json
import requests

app = Flask(__name__)
url = 'https://api.funtranslations.com/translate/'
final_url = ''
@app.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True)
  print(json.dumps(req, indent=4, sort_keys=True))
  print(req['queryResult'])
  try:
    intent = req.get('queryResult').get('intent').get('displayName')
  except AttributeError:
    return 'json error'
  print('Intent: ' + intent)
  if intent == 'Translation Init':
    fulfillment = req.get('queryResult').get('fulfillmentText')
    global final_url
    final_url = url +req.get('queryResult').get('parameters').get('Language')[0]+'.json'
    print(final_url) 
    return make_response(jsonify({'fulfillmentText': fulfillment,'followupEventInput': {'name': 'Translate','languageCode': 'en-US'}}))
  elif intent == 'Translate':
    query = req.get('queryResult').get('queryText')
    print(query,'*****',final_url)
    payload = {'text':query}
    res = requests.post(final_url,params=payload)
    text = res.json()["contents"]["translated"]
    return make_response(jsonify({'fulfillmentText': text}))
  else:
    return make_response(jsonify({'fulfillmentText': 'Apna Time Aega'}))
if __name__ == '__main__':
  app.run()