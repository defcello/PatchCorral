####################################################################################################
# Copyright 2013 John Crawford
#
# This file is part of SynthServer.
#
# SynthServer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SynthServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SynthServer.  If not, see <http://www.gnu.org/licenses/>.
####################################################################################################

## @file
#  Executable for launching an HTTP server on this computer that other computers can use to
#  manipulate synthesizers through MIDI.  Intended for use with performances of the "Children of
#  Eden" musical.
#
#  Installation:
#   1. Install "pyrtmidi" using the included "setup.py".  Note that it only really compiles against
#      Python 2.X (Python 3.X has some major issues when compiling).
#
#  @date 03/07/2013

import BaseHTTPServer
import cgi
import socket
import time
import traceback
import threading



HTTP_SERVER = None

try:
  from urlparse import urlparse, parse_qs
  from webpages import ChildrenOfEden


  class HTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def address_string(self):
      host, port = self.client_address[:2]
      #return socket.getfqdn(host)
      return host

    def do_GET(self, postVals=None):
      query_components = parse_qs(urlparse(self.path).query)
      # print 'query_components = "{0}"'.format(query_components)
      if postVals is not None:
        page = ChildrenOfEden.onPost(postVals, query_components)

      self.send_response(200)
      # print 'self.path = "{0}"'.format(self.path)
      if self.path == '/style.css':
        self.send_header("Content-type", "text/css")
        self.end_headers()
        with open('style.css', 'r') as fd:
          self.wfile.write(fd.read())
      elif self.path == '/children_of_eden_by_parkbc-d2ylko8.jpg':
        self.send_header("Content-type", "application/octet-stream")
        self.end_headers()
        with open('children_of_eden_by_parkbc-d2ylko8.jpg', 'rb') as fd:
          self.wfile.write(fd.read())
      else:
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(ChildrenOfEden.getPage(self.path, postVals, query_components))

    def do_POST(self):
      # print 'HEADERS='
      # print self.headers
      form = cgi.FieldStorage(
        fp=self.rfile,
        headers=self.headers,
        environ={
          'REQUEST_METHOD':'POST',
          'CONTENT_TYPE':self.headers['Content-Type'],
        }
      )
      # print 'END'
      # print 'FORM.LIST='
      # for key in form.keys():
        # print '   {0}: {1}'.format(key, form.getlist(key))
      # print 'END'
      postVals = {}
      for key in form.keys():
        postVals[key] = form.getlist(key)
      self.do_GET(postVals)


  def run(server_class=BaseHTTPServer.HTTPServer, handler_class=HTTPRequestHandler):
    global HTTP_SERVER
    server_address = ('', 80)
    HTTP_SERVER = server_class(server_address, handler_class)
    HTTP_SERVER.serve_forever()
  serverThread = threading.Thread(target=run)
  serverThread.start()
  print '\nWaiting for HTTP server to come up...'
  while HTTP_SERVER is None:
    time.sleep(0.1)
  print '\n\nShowtime!  (^o^)/'
  print '\nPlease point web browsers to: "{}"'.format(socket.gethostbyname(socket.gethostname()))
  serverThread.join()

  if __name__ == 'main':
    run()
except:
  print traceback.print_exc()
  print
  print
  print
  print 'Press "Enter" to close...'
  raw_input()