#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   router_test
Author:     Zhou Boyu
@contact:   zby22013@163.com
@version:   $

Description:

    Changelog:

        '''

import json
import pytest
import mock

from router import index, Host, Performance
from flask import Flask

class TestRouter(object):
    def test_index(self, app):
        rv = app.test_client().get('/index.html')
        assert "index.js" in rv.data

    def test_host_detail(self, app):
        rv = app.test_client().post('/host/detail' , data=dict(hostUuid="node_135") )
        assert "detail.js" in rv.data
        assert "index.js" not in rv.data

    def test_docs(self, app):
        rv = app.test_client().get('/docs', follow_redirects=True)
        assert "API Spec" in rv.data
