import os
import sys
from flask import Flask 
from webapp.calcaddr import ChatGPT

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

   @app.route('/b')
   def calc():
      gpt = ChatGPT()
      error = ""

      if ( request.method == 'POST' ):
         if ( 'ipaddrs' not in request.form ):
            error = 'No Paramater Found.'

         addr_data = request.form['ipaddrs']

         if ( addr_data is not None ):
            addr_list = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[1-3]?\d', addr_data)
            if ( len(addr_list) == 0 ):
               error = "IP Address is Not Found."

            else:
               res = gpt.calcNetworkAddr(addr_list)
               return render_template('calcaddr.html', answer=res)

         else:
            error = "IP Address is Not Set."

         flash(error)

      return render_template('calcaddr.html')


   return app 
