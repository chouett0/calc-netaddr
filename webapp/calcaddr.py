import re
import os
import sys
import openai
import functools
from flask import (
Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('calcaddr', __name__, url_prefix='/calcaddr')

class ChatGPT:
	def __init__(self):
		# ChatGPT API KEY
		if ( 'openai_key' in os.environ ):
			openai.api_key = os.environ['openai_key']
		else:
			print("[!] OpenAI API KEY is Not Set.")
			sys.exit(1)

	def exec_console(self, code):
		response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role":"user", "content":code}
			]
		)

		# print(response["choices"][0]["message"]["content"])
		if ( len(response["choices"]) > 0 ):
			if ("message" in response["choices"][0] ):
				if ( "content" in response["choices"][0]["message"] ):
					return response["choices"][0]["message"]["content"]

		else:
			return "Error"


	def calcNetworkAddr(self, addr_list):
		code = "Outputs only results for the following IP addresses: network address, broadcast address, subnet mask, and number of available IP addresses"
		for ipaddr in addr_list:
			code += " \n " +ipaddr

		#print("########## Question ##############\n"+code+"\n##################################\n\n########### Answer ###############\n")
		res = self.exec_console(code)

		return res


@bp.route('/cna', methods=('GET', 'POST'))
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
