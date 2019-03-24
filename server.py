from flask import Flask, request, make_response, jsonify
import json
import requests
import random

app = Flask(__name__)
url = 'http://numbersapi.com/'


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(req)
    intent = req.get('queryResult').get('intent').get('displayName')
    print(intent)
    if intent == 'Default Welcome Intent':
        return make_response(jsonify({'fulfillmentText': 'Welcome detetcted'}))

    elif intent == 'numbers':
        # Extarct the text
        qtype = req.get('queryResult').get('parameters').get('type')
        num = req.get('queryResult').get('parameters').get('number')
        if qtype == 'random':
            q = ['trivia', 'math', 'year']
            qtype = random.choice(q)

        # Send a API request
        final_url = url + str(int(num)) + '/' + qtype + '?json'
        print(final_url)
        res = requests.get(final_url)
        # Extract response
        print(res.json())
        text = res.json()["text"]

        # Return
        return make_response(jsonify({'fulfillmentText': text}))

    return make_response(jsonify({'fulfillmentText': 'Apna Time Aega'}))


if __name__ == '__main__':
    app.run()
