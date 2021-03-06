#!/usr/bin/env python

# Copyright (c) 2010-2011 Jonas Heylen <jonas.heylen@gmail.com>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are 
# permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this list of
#   conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, this list of
#   conditions and the following disclaimer in the documentation and/or other materials
#   provided with the distribution.
# * Neither the name of the owner nor the names of its contributors may be used to endorse
#   or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


import sys
from datetime import datetime, timedelta
from urllib2 import *
from xml.etree import ElementTree

class MobileVikings(object):
    """Mobile Vikings API for Python
    https://mobilevikings.com/api/2.0/doc/"""

    baseurl    = "https://mobilevikings.com/api/2.0/basic/"
    dateformat = "%Y-%m-%dT%H:%M:%S"
    dateformat_output = "%Y-%m-%d %H:%M:%S"
    dateformat_topup = "%Y-%m-%d %H:%M:%S"

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
        try:
            return opener.open(url)
        except HTTPError as e:
            if e.code == 401:
                raise AuthenticationException(e)
            else:
                raise NetworkException(e)
        except URLError as e:
            raise NetworkException(e)

    def sim_balance(self):
        """Get the current SIM balance for the logged in user"""
        res = MobileVikings.urlopen_with_auth(self.baseurl + "sim_balance.xml", self.username, self.password)
        xml = ElementTree.parse(res)
        return {"credits": float(xml.find("credits").text),
                "sms": int(xml.find("sms").text),
                "sms_mv": int(xml.find("sms_super_on_net").text),
                "data": int(xml.find("data").text),
                "valid_until": datetime.strptime(xml.find("valid_until").text,
                    self.dateformat_topup),
                "is_expired": xml.find("is_expired").text.lower() == "true"}

    def call_history(self, from_date=None, until_date=None, page_size=100, page=1):
        """Get the call history from the logged in user"""
        
        if from_date is None:
            from_date = datetime.now() - timedelta(weeks=1)
        args = "?from_date=" + from_date.strftime(self.dateformat)

        if until_date is not None:
            args += "&until_date=" + until_date.strftime(self.dateformat)

        args += "&page_size=" + str(page_size)
        args += "&page=" + str(page)

        res = MobileVikings.urlopen_with_auth(self.baseurl + "usage.xml" + args, 
                self.username, self.password)
        xml = ElementTree.parse(res)
        result = []
        for calldata in xml.findall("resource"):
            try:
                result.append({
                    "from": calldata.find("from").text,
                    "start_timestamp": datetime.strptime(calldata.find("start_timestamp").text,
                        self.dateformat_output),
                    "end_timestamp": datetime.strptime(calldata.find("end_timestamp").text,
                        self.dateformat_output),
                    "duration_call": calldata.find("duration_call").text,
                    "duration_connection": calldata.find("duration_connection").text,
                    "duration_human": calldata.find("duration_human").text,
                    "to": calldata.find("to").text,
                    "is_incoming": calldata.find("is_incoming").text.lower() == "true",
                    "is_voice": calldata.find("is_voice").text.lower() == "true",
                    "is_sms": calldata.find("is_sms").text.lower() == "true",
                    "is_mms": calldata.find("is_mms").text.lower() == "true",
                    "is_data": calldata.find("is_data").text.lower() == "true",
                    "price": float(calldata.find("price").text),
                    "balance": float(calldata.find("balance").text)
                })
            except Exception as e:
                print("Failed to parse entry: " + ElementTree.tostring(calldata))
                print(e)
        return result

    def top_up_history(self):
        """Get the top up history from the logged in user"""
        res = MobileVikings.urlopen_with_auth(self.baseurl + "top_up_history.xml", self.username, self.password)
        xml = ElementTree.parse(res)
        return [{
                "on": datetime.strptime(topup.find("on").text, self.dateformat),
                "id": topup.find("id").text,
                "subscription_id": topup.find("subscription_id").text,
                "amount": float(topup.find("amount").text),
                "method": topup.find("method/clean").text,
                "method_pretty": topup.find("method/pretty").text,
                "status": topup.find("status/clean").text,
                "status_pretty": topup.find("status/pretty").text
            } for topup in xml.findall("topup")]

class NetworkException(Exception):
    def __init__(self, causedby):
        self.causedby = causedby

    def __str__(self):
        return "Could not connect to Mobile Vikings API: " + str(self.causedby)
        
class AuthenticationException(NetworkException):
    def __str__(self):
        return "Invalid username or password"

def usage():
    print("Usage: %s <username> <password>" % sys.argv[0])


def main(argv):
    if len(argv) != 2:
        usage()
        sys.exit(2)
    username = argv[0]
    password = argv[1]
    
    try:
        mv = MobileVikings(username, password)

        balance = mv.sim_balance()
        print("=== Balance ===")
        print("Credits: %s EUR - SMS: %s - SMS (MV): %s - Data: %s MB - Valid until: %s\n"
                % (balance["credits"], balance["sms"], balance["sms_mv"],
            balance["data"]/(1024*1024), balance["valid_until"]))

        twodaysago = datetime.now() - timedelta(days=2)
        yesterday = datetime.now() - timedelta(days=1)
        now = datetime.now()
        call_history_yesterday = mv.call_history(twodaysago, yesterday)
        call_history_today = mv.call_history(yesterday, now)
        print("=== Call History ===")
        print("#### Yesterday:")
        for call in call_history_yesterday:
            print(call)
        print("#### Today:")
        for call in call_history_today:
            print(call)
        print("")

        top_up_history = mv.top_up_history()
        print("=== Top-ups ===")
        for topup in top_up_history:
            print("%s - %s EUR (%s) - %s" % (topup["on"], topup["amount"],
                topup["method_pretty"], topup["status_pretty"]))
    except NetworkException as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])

