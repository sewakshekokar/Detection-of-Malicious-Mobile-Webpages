# C. Code for Creating a Server
import json
from flask import Flask, request
import predict  # This should be the file containing `retrive_pred`

app = Flask(__name__)

@app.route('/abc', methods=['POST'])
def hello_world():
    url_data = request.json
    url = url_data['url']
    result = predict.retrive_pred(url)
    return json.dumps(result)

if __name__ == '__main__':
    app.run()
