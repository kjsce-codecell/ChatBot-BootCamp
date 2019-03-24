from flask import Flask, request, make_response, jsonify
import json
import os
import requests
from pprint import pprint

app = Flask(__name__)

emojis = {
    "pos": ":)",
    "neutral": ":|",
    "neg": ":("
}

# function for responses

def fetch_result(query, lang):
    available_languages = ["english","french","dutch"]

    if lang.lower() not in available_languages:
        return "Sorry," + lang + "language not supported as of now " + emojis["neg"]

    url = 'http://text-processing.com/api/sentiment/'
    payload = {"text": query, "language": lang }
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        json_response = response.json()
        label = json_response["label"]
        probability = json_response["probability"][label]
        emoji = emojis[label]

        result = query + "is " + label + " " + emoji + " : " + str(int(probability*100))  + "%"
    else:
        result = "request overlimit"

    return result


def results(request):
    # fetch action from json
    action = request.get("queryResult")
    params = action['parameters']
    
    if len(params["language"]):
        language = params["language"]
        print("LANGUAGE "+language)
    else:
        language = "english"

    query = params["query"]
    results = fetch_result(query=query, lang=language)

    # return a fulfillment response
    response = {'fulfillmentText': results}
    return response

# create a route for webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    res = results(request.get_json(force=True))
    print(jsonify(res))
    return make_response(jsonify(res))

if __name__ == '__main__':
    app.run(port=8080, debug=True)
