# -*- coding: utf-8 -*-

from flask import Flask, request, g, url_for, render_template
import datetime
import flask_sijax
import os
from dateutil import parser

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import urllib
import StringIO
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
	plt.style.use('ggplot')
	df = data["weatherParams"].reset_index()
	fig, ax = plt.subplots()
	fig.set_size_inches(8.9,5.0)
	fig.set_dpi(80)
	fig.set_tight_layout(True)
	plt.xticks(rotation=70)
	ax.plot(df["index"], df["humidity"], label="HT")
	ax.plot(df["index"], df["temperature"], label="HT")
	ax.legend()
	plt.savefig("static/tempFiles/dataChart.svg", format='svg', transparent=False, bbox_inches='tight', pad_inches=0)
	return "http://localhost:9500/static/tempFiles/dataChart.svg"

@app.route('/dataDisplay')
def dataDisplay():
	g.db.switch_database('weatherData')
	data = g.db.query('select * from weatherParams;')
	svgPic = createChart(data) 
	return render_template('index.html', svgPic=svgPic)

if __name__ == '__main__':
	app.run(port=9500)
