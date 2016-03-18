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

from router import index

class TestRouter(object):
    def test_host_detail(self, app):
        with app.test_request_context('/host/detail/.html', method='POST'):
            assert 1==1
