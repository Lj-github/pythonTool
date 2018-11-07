# -*- coding: utf-8 -*-
# @Time    : 18/4/11 下午8:16
# @Author  : myTool
# @File    : http.py
# @Software: PyCharm

import json
from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):
  def _writeheaders(self):
    print("path")
    print self.path
    le = str(self.path).split(".").pop()
    print("le" + le)
    if le != "ico":
        with open("allCcbi.json", 'w') as f:
            json.dump(self.path[2:], f)
    print(self.path)
    print("headers")
    print self.headers
    self.send_response(200);
    self.send_header('Content-type','text/html');
    self.end_headers()
  def do_Head(self):
    self._writeheaders()
  def do_GET(self):
    self._writeheaders()
    self.wfile.write("""<!DOCTYPE HTML>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
<p>this is get!</p>
</body>
</html>"""+str(self.headers))
  def do_POST(self):
    self._writeheaders()
    length = self.headers.getheader('content-length');
    nbytes = int(length)
    data = self.rfile.read(nbytes)

    self.wfile.write("""<!DOCTYPE HTML>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
<p>this is put!</p>
</body>
</html>"""+str(self.headers)+str(self.command)+str(self.headers.dict)+data)
addr = ('',8765)
server = HTTPServer(addr,RequestHandler)
server.serve_forever()