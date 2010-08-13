#!/usr/bin/env python

import sys
from urllib2 import *
from xml.etree import ElementTree

class MobileVikings:
	"""Mobile Vikings API for Python"""

	baseurl	= 'https://mobilevikings.com/api/1.0/rest/mobilevikings/'

	def __init__(self, username, password):
		"""Initialize the Mobile Vikings API with a username and password"""
		self.username = username
		self.password = password

	@staticmethod
	def urlopen_with_auth(url, username, password):
		"""Helper function to use urllib2.urlopen with HTTP basic authentication"""
		password_manager = HTTPPasswordMgrWithDefaultRealm()
		password_manager.add_password(None, url, username, password)
		handler = HTTPBasicAuthHandler(password_manager)
		opener = build_opener(handler)
		return opener.open(url)

	def sim_balance(self):
		"""Get the current SIM balance for the logged in user"""
		res = MobileVikings.urlopen_with_auth(self.baseurl + 'sim_balance.xml', self.username, self.password)
		xml = ElementTree.parse(res)
		return {"credits": float(xml.find('credits').text),
				"sms": int(xml.find('sms').text),
				"data": int(xml.find('data').text)}

	def call_history(self):
		"""Get the call history from the logged in user"""
		res = MobileVikings.urlopen_with_auth(self.baseurl + 'call_history.xml', self.username, self.password)
		xml = ElementTree.parse(res)

	def top_up_history(self):
		"""Get the top up history from the logged in user"""
		res = MobileVikings.urlopen_with_auth(self.baseurl + 'top_up_history.xml', self.username, self.password)
		xml = ElementTree.parse(res)
		topups = xml.findall('topup')

def usage():
	print "Usage: %s <username> <password>" % sys.argv[0]


def main(argv):
	if len(argv) != 2:
		usage()
		sys.exit(2)
	username = argv[0]
	password = argv[1]
	
	mv = MobileVikings(username, password)
	
	balance = mv.sim_balance()
	print("""Credits: %s EUR
SMS: %s
Data: %s MB""" % (balance['credits'], balance['sms'], balance['data']/(1024*1024)))

	call_history = mv.call_history()

	top_up_history = mv.top_up_history()


if __name__ == '__main__':
	main(sys.argv[1:])

