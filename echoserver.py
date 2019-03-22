from flask import Flask,request,jsonify
from werkzeug.datastructures import ImmutableMultiDict


app=Flask(__name__)

@app.route('/', methods=['GET'])
def respond():
  #Accept data from query string herew
  data=request.args.to_dict()
  return jsonify({"reply":"Token is 1234567"})

@app.route('/', methods=['POST'])
def verify():
  data=request.data
  return data

if __name__ == '__main__':
  app.run()
