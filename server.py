from flask import Flask, request, make_response, jsonify
import json
import requests

'''
Functions of the imported modules =>
1. Flask         - to initialise and use the flask app
2. request       - to handle the requests sent to this flask server
3. make_response - creates a response object for the flask server
4. jsonify       - creates a json response object, with header set to json
5. json          - JSON is a syntax for storing and exchanging data.
6. requests      - to make requests ('GET','POST',...) from python files
'''

app = Flask(__name__)
url = 'https://api.funtranslations.com/translate/'


@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)
	print(req)
	query_result = req.get('queryResult')
	try:
		intent =    # extact intent name ( displayName ) attribute from query_result
    except AttributeError:
		return 'json error'
	print('Intent: ' + intent)
	if intent == 'Translation Init':
		fulfillment = # extact text ( fulfillmentText ) attribute from query_result 
		language = # extract language attribute from query_result
		return make_response(jsonify({'fulfillmentText': fulfillment, 'followupEventInput': {'name': 'Translate', 'parameters': {'language': language}, 'languageCode': 'en-US'}}))
	elif intent == 'Translate':
		query = # extact quert text ( queryText ) attribute from query_result 
		language = # extract language attribute passed as context from query_result
		payload = {'text': query}
		final_url = url + language + '.json'
		res = # make a post request to final_url using given data ( payload )
		if res.status_code == 200:
			text = # extract result ( translated text ) from response object
		else:
			print(res.status_code)
			text = "request overlimit"
		return # return a response object in json with fulfillmentText as attribute mapped with retreived results from API
	else:
		return # return a response object in json with fulfillmentText as attribute 

if __name__ == '__main__':
	app.run()
