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
    re = request.get_data().decode("utf-8").replace("%252C", "%2C").replace("%3D", "=")
    tickers = re[2:].split("%2C")

    for t in tickers:
        print(t)

    wms = tickers[-1].split("%5E")
    del tickers[-1]
    k = 0

    for i in wms:
        if k != 0:
            wms[k] = "^" + i
        k += 1

    tickers = tickers + wms

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
