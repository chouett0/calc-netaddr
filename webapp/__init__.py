import os
import sys
from flask import Flask 

def create_app(test_config=None):
   app = Flask(__name__, instance_relative_config=True)

   if ( test_config is None ):
      if ( 'secret_key' not in os.environ ):
         print('[!] SECRET KEY IS NOT SET.')
         sys.exit(1)
         
      secret_key = os.environ['secret_key']
      app.config.from_pyfile('config.py', silent=True)
      app.config.from_mapping(SECRET_KEY=secret_key)

   else:
      app.config.from_mapping(test_config)


   try:
      os.makedirs(app.instance_path)

   except OSError:
      pass

   from . import calcaddr
   app.register_blueprint(calcaddr.bp)

   @app.route('/test')
   def test():
      return "OK"

   return app 
