#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   spec
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''

from flask import Flask, render_template, request, json, redirect
import config
from service.transfer import Transfer
from flask_restful_swagger import swagger
from flask.ext.restful import Api, Resource, fields

app = Flask(__name__, static_folder='./static')

api = swagger.docs(Api(app), apiVersion='0.1',
                   resourcePath='/',
                   produces=["application/json"],
                   api_spec_url='/api/monitor',
                   description='SaDev4 Linux Monitor API')


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/host/detail', methods=['POST'])
def host_detail():
    uuid = request.form['hostUuid']
    return render_template('detail.html', uuid=uuid)


@app.route('/docs')
def docs():
    return redirect('/static/docs.html')


@swagger.model
class HostItem:
    resource_fields = {
        'hostIP': fields.String,
        'hostCPU': fields.Float,
        'hostLoad': fields.String,
        'hostMemory': fields.Float
    }


class Host(Resource):
    @swagger.operation(
        notes='Get Host List With Metadata',
        responseClass=HostItem,
        nickname='host/list',
        responseMessages=[
            {
                "code": 200,
                "message": "Get host list success!"
            },
            {
                "code": 500,
                "message": "Server Error"
            }
        ]
    )
    def get(self):
        """Get host list

        Get host list, which installed our monitor agent, will show cpu load
        and memory data in the list.
        """
        return Transfer().get_hosts(), 200, {
            'Access-Control-Allow-Origin': '*'}


@swagger.model
class PerformanceItem:
    resource_fields = {
        'name': fields.String,
        'time': fields.DateTime,
        'data': fields.List
    }


class Performance(Resource):
    @swagger.operation(
        notes='Get Performance Data',
        responseClass=PerformanceItem,
        nickname='performance',
        parameters=[
            {
                "name": "uuid",
                "description": "The ID of the Host",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "query"
            },
            {
                "name": "collection",
                "description": "The collection name of query",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Get data success!"
            },
            {
                "code": 400,
                "message": "Bad request parameter"
            },
            {
                "code": 404,
                "message": "Collections not found in database"
            },
            {
                "code": 500,
                "message": "Server Error"
            }
        ]
    )
    def get(self):
        """Get Performance Data

        Get performance data from database. Required uuid which is host-name/IP
        and collection which is the collection name in database. When the
        collection is not found in database, will return status 404.
        """
        collection = request.args.get('collection')
        uuid = request.args.get('uuid')
        return Transfer().get_data(uuid, collection), 200, {
            'Access-Control-Allow-Origin': '*'}


api.add_resource(Host, '/host/list')
api.add_resource(Performance, '/performance')

if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.DEBUG)
