# -*- coding: utf-8 -*-

from flask import Flask, request, g, url_for, render_template
import datetime
import os
from dateutil import parser

import flask_sijax
import pandas as pd
import pygal
from pytz import timezone
import pytz
from pygal.style import Style, CleanStyle
import urllib
from influxdb import DataFrameClient

# configuration
DATABASE = 'example'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

path = os.path.join(',', os.path.dirname(__file__), 'static/js/')
app = Flask(__name__)
app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = '/static/js/json2.js'
app.config.from_object(__name__)
flask_sijax.Sijax(app)

def connect_db():
	return DataFrameClient('localhost', 8086, 'root', 'root', app.config['DATABASE'])

@app.before_request
def before_request():
	g.db = connect_db()

def createChart(data):
	df = data["weatherParams"]
	df.index = df.index.tz_convert(timezone('Asia/Katmandu'))
	df = df.reset_index()
	bar_chart = pygal.Line(width=1200, height=600, explicit_size=True, title="testing", style=CleanStyle, disable_xml_declaration=True, x_label_rotation=20, dots_size=5, stroke_style={'width':3}, show_x_guides=True)
	bar_chart.x_labels = df["index"]
	bar_chart.add('Temps in C', df["temperature"])
	bar_chart.add('Humidity in %', df["humidity"])
	bar_chart.add('Soil Moisture in units', df["soilMoisture"]/10)
	bar_chart.interpolate = 'cubic'
	return bar_chart

@app.route('/dataDisplay')
def dataDisplay():
	g.db.switch_database('weatherData')
	data = g.db.query('select * from weatherParams;')
	bar_chart = createChart(data) 
	return render_template('altIndex.html', bar_chart=bar_chart)

if __name__ == '__main__':
	app.run(port=9500)
