#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   module
Author:     Hao Tingyi / Zhou Boyu
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''

class ModuleException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)