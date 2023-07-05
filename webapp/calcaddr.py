import re
import os
import sys
import openai
import functools
from flask import (
Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('calcaddr', __name__, url_prefix='/calcaddr')

"""
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

"""

class CalcIPAddress:
	def __init__(self):
		self.subnet_bin	= ''
		self.netaddr_bin	= ''
		self.bcaddr_bin	= ''

		self.subnet		= ''
		self.netaddr	= ''
		self.bcaddr		= ''

		self.ip_bin		= ''
		self.prefix 	= ''
		self.can_use_ip = 0

	## サブネット
	def calcSubnet(self):
		self.subnet		= ''

		self.subnet_bin = '1'*int(self.prefix) + '0'*(32 - self.prefix)
		for i in range(0, 32, 8):
			if ( i == 24 ):
				self.subnet += str(int('0b' + self.subnet_bin[i:i+8], 0))
			else:
				self.subnet += str(int('0b' + self.subnet_bin[i:i+8], 0)) + '.'



	## ネットワークアドレス
	def calcNetworkAddress(self):
		self.netaddr	= ''

		self.netaddr_bin = bin(int('0b' + self.subnet_bin, 0) & int('0b' + self.ip_bin, 0))[2:].zfill(32)
		for i in range(0, 32, 8):
			if ( i == 24 ):
				self.netaddr += str( int('0b' + self.netaddr_bin[i:i+8], 0) )
			else:
				self.netaddr += str( int('0b' + self.netaddr_bin[i:i+8], 0) ) + '.'


	## ブロードキャストアドレス
	def calcBroadcastAddress(self):
		self.bcaddr		= ''

		self.can_use_ip = int('0b' + str(('1'*(32 - self.prefix)).zfill(32)), 0) - 1
		self.bcaddr_bin = bin(int('0b' + self.netaddr_bin, 0) | int('0b' + str(('1'*(32 - self.prefix)).zfill(32)), 0))[2:].zfill(32)
		for i in range(0, 32, 8):
			if ( i == 24 ):
				self.bcaddr += str( int('0b' + self.bcaddr_bin[i:i+8], 0) )
			else:
				self.bcaddr += str( int('0b' + self.bcaddr_bin[i:i+8], 0) ) + '.'


	def calc(self, addr_list):
		result = "## Result\n"

		for addr in addr_list:
			self.ip_bin = ''
			self.can_use_ip = 0

			prefix = re.findall('\d+\.\d+\.\d+\.\d+\/(\d+)', addr)
			if ( len(prefix) <= 0 ):
				result += "[!] Invalid IP Address Prefix: {}\n\n".format(addr)
				continue

			else:
				self.prefix = int(prefix[0])

			ip_addr = [x for x in addr.split('/')[0].split('.')]
			if ( len(ip_addr) < 4 ):
				result += "[!] Invalid IP Address: {}\n\n".format(addr)
				continue

			for ip in ip_addr:
				self.ip_bin += bin(int(ip))[2:].zfill(8)

			print('[*] address list: {}'.format(addr_list))
			print('[*] ip address(bin): {}'.format(self.ip_bin))
			print('[*] Prefix: {}'.format(self.prefix))

			self.calcSubnet()
			self.calcNetworkAddress()
			self.calcBroadcastAddress()

			result += 'IP Address: {}\nSubnet Mask: {}\nNetwork Address: {}\nBroadcast Address: {}\nCan Use IP Address: {}\n\n'.format(addr, self.subnet, self.netaddr, self.bcaddr, self.can_use_ip)

		return result


@bp.route('/calc', methods=('GET', 'POST'))
def calc():
#	gpt = ChatGPT()
	calc_ip = CalcIPAddress()
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
#				res = gpt.calcNetworkAddr(addr_list)
				res = calc_ip.calc(addr_list)
				return render_template('calcaddr.html', answer=res)

		else:
			error = "IP Address is Not Set."

		flash(error)

	return render_template('calcaddr.html')
