#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   router
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''

from flask import Flask, render_template, request, json

import config
from data.collector import DataCollection
from service.transfer import Transfer

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/server/')
def server():
    module = request.args.get('module')
    return json.dumps(DataCollection(module).catch(), sort_keys=False)


@app.route('/performance/')
def performance():
    collection = request.args.get('collection')
    return json.dumps(Transfer().get_data(collection), sort_keys=False)

if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.DEBUG)
