import cherrypy
import pandas as pd
import json
import os

import myprocessor
from auth_util import decrypt_auth_token
from auth_util import generate_pair

p = myprocessor.MyProcessor()

port = '8080'

if 'PORT' in os.environ:
  port = os.environ['PORT']


#https://towardsdatascience.com/build-your-own-python-restful-web-service-840ed7766832

cherrypy.config.update({
'server.socket_host': '0.0.0.0',
'server.socket_port': int(port)})
class MyWebService(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()

    def generatepair(self):
      (publickey, privatekey) = generate_pair()

      responseData = {
        'publickey': publickey.decode('ASCII'),
        'privatekey': privatekey.decode('ASCII')
      }

      #return (publickey, privatekey)
      return responseData

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()

    def decrypttoken(self):
      data = cherrypy.request.json
      auth = decrypt_auth_token(data.get("encryptedtoken"), data.get("publickey"), data.get("privatekey"))

      responseData = {
          'success': True,
          'token': auth.decode('ASCII')
      }

      #print("token (decrypted): %s" % auth)
      return responseData
   
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()

    def process(self):
      data = cherrypy.request.json
      df = pd.DataFrame(data)
      output = p.run(df)
      return output.to_json()

if __name__ == '__main__':
    config = {'server.socket_host': '0.0.0.0'}
    cherrypy.config.update(config)
    cherrypy.quickstart(MyWebService())