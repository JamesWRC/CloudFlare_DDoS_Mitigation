#!/usr/bin/env python3
# import required libs

import flask
from flask import request, jsonify, abort, Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify("hello: world")

    ###                                      ###
    #   ADD MORE LATER WHEN A WEB UI IS MADE   #
    ###                                      ###


if __name__ == '__main__':
    # application.run(host='0.0.0.0', port=80, debug=True)
    app.run(host='0.0.0.0', port=80)
