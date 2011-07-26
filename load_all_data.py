#!/usr/bin/env python

# Copyright (c) 2011 Jonas Heylen <jonas.heylen@gmail.com>
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

import csv
import sys

from mobilevikings import MobileVikings
from datetime import datetime, timedelta

from pymongo import Connection

def usage():
    print("Usage: %s <username> <password>" % sys.argv[0])


def main(argv):
    if (len(argv) != 2):
        usage()
        sys.exit(2)
    username = argv[0]
    password = argv[1]

    print("Creating MongoDB connection")
    mongo = Connection()
    db = mongo.vikingstats
    history_collection = db.history

    print("Creating MobileVikings interface")
    mv = MobileVikings(username, password)
    now = datetime.now()

    for page in range(1, 21): # max 20 pages
        print("Calling MobileVikings usage API for page " + str(page))
        history = mv.call_history(from_date=now-timedelta(days=30), until_date=now, page=page)
        for entry in history:
            result = history_collection.find_one({"start_timestamp": entry["start_timestamp"]})
            if result == None:
                print("- Inserting entry (" + str(entry["start_timestamp"]) + ")")
                print(entry)
                history_collection.insert(entry)
            else:
                print("- Already stored (" + str(entry["start_timestamp"]) + ")")
        if len(history) < 100:
            print("Last page")
            break

if __name__ == "__main__":
    main(sys.argv[1:])

