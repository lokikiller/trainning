#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   server
Author:     Hao Tingyi
@contact:   lokikiller@126.com
@version:   $

Description:

Changelog:

'''

# !/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
from collector import DataCollection
import json


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class MainHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            contentType = 'text/html'
            module = self.path.split('=')[1]
            data = DataCollection(module).catch()

            self.send_response(200)
            self.send_header('Content-type', contentType)
            self.end_headers()
            self.wfile.write(json.dumps(data, sort_keys=False))

        except IOError:
            self.send_error(404, 'Module Not Found: %s' % self.path)


if __name__ == '__main__':
    server = ThreadedHTTPServer(('0.0.0.0', 27100), MainHandler)
    server.serve_forever()
