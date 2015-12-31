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
from service.transfer import Transfer

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/host/list')
def host_list():
    return json.dumps(Transfer().get_hosts())

@app.route('/host/detail', methods=['POST'])
def host_detail():
    uuid = request.form['hostUuid']
    return render_template('detail.html', uuid=uuid)

@app.route('/performance/')
def performance():
    collection = request.args.get('collection')
    uuid = request.args.get('uuid')
    return json.dumps(Transfer().get_data(uuid, collection), sort_keys=False)

if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.DEBUG)
