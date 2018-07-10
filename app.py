from flask import Flask, request
import flask
from flask_cors import CORS, cross_origin
import json
from dynamic import genfile
from multiprocessing import Process

app = Flask(__name__)
CORS(app)

nyse_dict = eval(open("nyse_dict.txt").read())
nyse_list = list(nyse_dict.keys())


@app.route('/postData', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_data():
    print(request.get_data().decode("utf-8"))
    numbers = request.get_data().decode("utf-8").split("v%5B%5D=")
    numbers.pop(0)
    for n, i in enumerate(numbers):
        if "&" in i:
            numbers[n] = i.replace("&", '')

    gen_graph(numbers)

    return json.dumps({'status': 'OK'})


@app.before_request
def before():
    pass


@app.after_request
def after(response):
  print(response.status)
  print(response.headers)
  print(response.get_data())
  return response


if __name__ == '__main__':
    app.run()


def gen_graph(codes):

    for code in codes:
        print(code)

    Process(target=genfile, args=[codes]).start()
