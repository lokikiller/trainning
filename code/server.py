import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer, test as _test
import subprocess
from SocketServer import ThreadingMixIn

bashPath = '/bash/'
serverPath = os.path.dirname(os.path.realpath(__file__))
staticPath = '/static/'


class ThreadHttpServer(ThreadingMixIn, HTTPServer):
    pass


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            contentType = 'text/html'
            if self.path.startswith('/server/'):
                module = self.path.split('=')[1]
                output = subprocess.Popen(serverPath + bashPath + module + '.sh', shell=True, stdout=subprocess.PIPE)
                # output.communicate() return stdout & stderr
                data = output.communicate()[0]
            else:
                if self.path == '/':
                    self.path = 'index.html'
                f = open(os.path.dirname(os.path.realpath(__file__)) + staticPath + self.path)
                data = f.read()
                if self.path.startswith('/css/'):
                    contentType = 'text/css'
                f.close()

            self.send_response(200)
            self.send_header('Content-type', contentType)
            self.end_headers()
            self.wfile.write(data)
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

if __name__ == '__main__':
    server = ThreadHttpServer(('0.0.0.0', 8081), Handler)
    print 'Starting server, visiting localhost:8081'
    server.serve_forever()

