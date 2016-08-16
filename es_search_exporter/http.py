#!/usr/bin/env python
"""
HTTP server for metrics
"""

import traceback
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from collector import collect_es
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from SocketServer import ForkingMixIn

class ForkingHTTPServer(ForkingMixIn, HTTPServer):
  pass

class EsSearchExporterHandler(BaseHTTPRequestHandler):
  def __init__(self, config, kerberos, tls, *args, **kwargs):
      self._config = config
      self._kerberos = kerberos
      self._tls = tls
      BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

  def do_GET(self):
    config = self._config
    url = urlparse.urlparse(self.path)
    if url.path == '/metrics':
      params = urlparse.parse_qs(url.query)
      if 'target' not in params:
        self.send_response(400)
        self.end_headers()
        self.wfile.write("Missing 'target' from parameters")
        return
      if 'search' not in params:
        self.send_response(400)
        self.end_headers()
        self.wfile.write("Missing 'search' from parameters")
        return
      search = params['search'][0]
      if search not in config['searches']:
        self.send_response(400)
        self.end_headers()
        self.wfile.write("Search {} not found in config".format(search))
        return
      try:
        output = collect_es(search, config['searches'][search], params['target'][0], self._kerberos, self._tls)
        self.send_response(200)
        self.send_header('Content-Type', CONTENT_TYPE_LATEST)
        self.end_headers()
        self.wfile.write(output)
      except:
        self.send_response(500)
        self.end_headers()
        self.wfile.write(traceback.format_exc())
    elif url.path == '/':
      self.send_response(200)
      self.end_headers()
      self.wfile.write("""<html>
      <head><title>Elasticsearch Search Exporter</title></head>
      <body>
      <h1>Elasticsearch Search Exporter</h1>
      <p>Visit <code>/metrics?target=127.0.0.1&search=example</code> to use.</p>
      </body>
      </html>""")
    else:
      self.send_response(404)
      self.end_headers()

def start_http_server(config, port, kerberos, tls):
  handler = lambda *args, **kwargs: EsSearchExporterHandler(config, kerberos, tls, *args, **kwargs)
  server = ForkingHTTPServer(('', port), handler)
  server.serve_forever()

