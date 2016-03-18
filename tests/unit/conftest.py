#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   conftest
Author:     Zhou Boyu
@contact:   zby22013@163.com
@version:   $

Description:

        Changelog:

'''

import pytest

from flask import Flask
import router
@pytest.yield_fixture

def app(request):
    router.app.debug = True
    router.app.testing = True
    with router.app.test_request_context():
        yield router.app
