from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
from dynamic import genfile
from multiprocessing import Process

app = Flask(__name__)
CORS(app)


@app.route('/postData', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_data():
    print(request.get_data().decode("utf-8"))
    tickers = request.get_data().decode("utf-8").split("v%5B%5D=")
    tickers.pop(0)
    for n, i in enumerate(tickers):
        if "&" in i:
            tickers[n] = i.replace("&", '')
    gen_graph(tickers)
    return json.dumps({'status': 'OK'})


@app.before_request
def before():
    pass


@app.after_request
def after(response):
  print(response.status)
  print(response.headers)
  return response


if __name__ == '__main__':
    app.run()


def gen_graph(codes):
    Process(target=genfile, args=[codes]).start()
