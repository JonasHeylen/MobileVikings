#!/usr/bin/env python

import web
from pymongo import Connection

urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())
render = web.template.render('templates/')

class hello:        
    def GET(self, name):
        mongo = Connection()
        db = mongo.vikingstats
        daily = db.daily
        data = daily.find()
        for day in data:
            print(day['value']['sms'])
        return render.graph()

if __name__ == "__main__":
    app.run()

