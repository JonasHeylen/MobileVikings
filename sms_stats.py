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

def usage():
    print("Usage: %s <username> <password> [<page>]" % sys.argv[0])


def main(argv):
    if (len(argv) < 2) or (len(argv) > 3):
        usage()
        sys.exit(2)
    username = argv[0]
    password = argv[1]
    page = 1
    if len(argv) == 3:
        page = int(argv[2])
    mv = MobileVikings(username, password)
    now = datetime.now()
    history = mv.call_history(from_date=now-timedelta(days=30), until_date=now, page=page)
    writer = csv.writer(sys.stdout)
    writer.writerow(["Timestamp", "Number", "Incoming"])
    for sms in [x for x in history if x["is_sms"]]:
        writer.writerow([sms["start_timestamp"], sms["to"], sms["is_incoming"]])

if __name__ == "__main__":
    main(sys.argv[1:])

