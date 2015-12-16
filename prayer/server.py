#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import sqlite3
from urlparse import parse_qs

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
  userid = 0
  #Handler for the GET requests
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()
    # Send the html message
    if self.path.startswith('/get_user'):
      fields = self.extract_fields('/get_user')
      connection = sqlite3.connect('database.db')
      cursor = connection.cursor()
      print(fields)
      cursor.execute('select * from Users where userID = ' + fields['id'][0] + ';')
      user1 = cursor.fetchone()
      print(user1)
    else:
      self.wfile.write("Hello World!")
    return

  def do_POST(self):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    fields = self.extract_fields('/create_user')
    cursor.execute(format("INSERT INTO Pizza_Users VALUES(%d, %s, %s, %s)", userid, fields['name'], fields['location'], fields['prayerRequest']))
    userid += 1
    connection.commit()
    return

  def extract_fields(self, prefix):
    if self.path.startswith(prefix):
      parameters = self.path.split('/')[2]
      fields = parse_qs(parameters)
      return fields

try:
  #Create a web server and define the handler to manage the
  #incoming request
  server = HTTPServer(('', PORT_NUMBER), myHandler)
  print 'Started httpserver on port ' , PORT_NUMBER
  
  #Wait forever for incoming htto requests
  server.serve_forever()

except KeyboardInterrupt:
  print '^C received, shutting down the web server'
  server.socket.close()