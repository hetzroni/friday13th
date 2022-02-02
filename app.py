#!/usr/bin/env python3

from datetime import datetime
from enum import Enum

import dateutil.parser
import pytz
from flask import Flask, render_template, request



INDEX_TEMPLATE = """
<p>Inserted data: {data}</p>
<p>Server time: {now:%Y-%m-%d %H:%M:%S}</p>
<p>Browser time: {browser_time:%Y-%m-%d %H:%M:%S}</p>
<p>Browser time zone: {timezone}</p>
<p>Today is: {day_of_week} the {day_of_month}</p>
"""


def th(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))


class Weekday(Enum):
    Sunday = 6
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5

    @staticmethod
    def from_datetime(when):
        return Weekday(when.weekday())


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/getTime", methods=['GET'])
def getTime():
    now = datetime.now()
    day_of_week=Weekday.from_datetime(now).name
    data = request.args.get("d")
    timezone = request.args.get("tz")
    browser_time = dateutil.parser.parse(request.args.get("t")).astimezone(pytz.timezone(timezone))
    day_of_month = th(now.day)
    return INDEX_TEMPLATE.format(**locals())
