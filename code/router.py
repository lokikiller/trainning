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

import httplib
import os

from flask import Flask, render_template, request, json

import config
from service.transfer import Transfer

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/server/')
def server():
    hostIp = os.environ.get('SERVER_HOST')
    if not hostIp:
        hostIp = '0.0.0.0'

    hostPort = os.environ.get('SERVER_PORT')
    if not hostPort:
        hostPort = '27100'

    module = request.args.get('module')
    conn = httplib.HTTPConnection(hostIp + ':' + hostPort)
    conn.request('GET', '/server/?module=' + module)
    data = conn.getresponse().read()
    conn.close()
    return data


@app.route('/performance/')
def performance():
    collection = request.args.get('collection')
    return json.dumps(Transfer().get_data(collection), sort_keys=False)


if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.DEBUG)
