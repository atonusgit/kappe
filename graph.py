# Great and fast tutorial
# https://www.youtube.com/watch?v=J_Cy_QjG6NE&ab_channel=sentdex
# sudo pip3 install dash dash-renderer dash-html-components dash-core-components plotly
# pip install --upgrade pip

import dash
from dash import dcc
from dash import html
import json
from datetime import datetime, timedelta, timezone
import requests
import os.path
from os import path
import glob
import subprocess

app = dash.Dash()
utc_offset = int(str(datetime.now(timezone.utc).astimezone().utcoffset()).split(':')[0])
utc_offset = 0 #override

names = ['kuisti', 'saunan_putket', 'keittion_putket', 'vessan_putket', 'sisalla', 'vessa', 'kasvihuone']
timestamps = {}
temperatures = {}
humidities = {}
battery_voltages = {}

x = requests.get('http://valle.fi/graph_day_range.php')
range = 2
newrange = int(x.content.decode())

if isinstance(newrange, int):
	range = newrange

logdates = []
i = 0
while i < range:
	logdates.append((datetime.now() - timedelta(i)).strftime("%y%m%d"))
	i += 1

logdates = list(reversed(logdates))

#
# Set kello
#
timestamps['kello'] = []
for logdate in logdates:
	for name in glob.glob('/home/pi/kappe/sensor_logs/' + logdate + '_kello.json'):
		with open(name) as f:
			y = json.load(f)
			for x in y:
				timestamps['kello'].append(x['timestamp'])

#
# Get raw values
#
for name in names:
	timestamps[name + "_raw"] = []
	temperatures[name + "_raw"] = []
	humidities[name + "_raw"] = []
	battery_voltages[name + "_raw"] = []

	for logdate in logdates:
		if path.exists("/home/pi/kappe/sensor_logs/" + logdate + "_" + name + ".json"):
			with open("/home/pi/kappe/sensor_logs/" + logdate + "_" + name + ".json") as f:
				y = json.load(f)
				for x in y:
					timestamps[name + "_raw"].append(x['timestamp'])
					temperatures[name + "_raw"].append(x['temperature'])
					humidities[name + "_raw"].append(x['humidity'])
					battery_voltages[name + "_raw"].append(x['battery'])

#
# Set value arrays
#
for name in names:
	timestamps[name] = []
	temperatures[name] = []
	humidities[name] = []
	battery_voltages[name] = []
	i = 0
	for kellostamp in timestamps['kello']:
		if kellostamp in timestamps[name + "_raw"]:
			date_time_obj = datetime.strptime(timestamps[name + "_raw"][i], '%d.%m.%Y %H:%M:%S') + timedelta(hours = utc_offset)
			timestamps[name].append(date_time_obj)
			temperatures[name].append(temperatures[name + "_raw"][i])
			humidities[name].append(humidities[name + "_raw"][i])
			battery_voltages[name].append(battery_voltages[name + "_raw"][i])
			i += 1
		else:
			date_time_obj = datetime.strptime(kellostamp, '%d.%m.%Y %H:%M:%S') + timedelta(hours = utc_offset)
			timestamps[name].append(kellostamp)
			temperatures[name].append("None")
			humidities[name].append("None")
			battery_voltages[name].append("None")

app.layout = html.Div(children=[
	html.H1(children='Ruuvidata'),
	dcc.Graph(
		id='temperatures',
		figure={
			'data': [
				{'x': timestamps['sisalla'], 'y': temperatures['sisalla'], 'type': 'line', 'name': 'Sisällä'},
				{'x': timestamps['kuisti'], 'y': temperatures['kuisti'], 'type': 'line', 'name': 'Kuisti'},
				{'x': timestamps['saunan_putket'], 'y': temperatures['saunan_putket'], 'type': 'line', 'name': 'Saunan putket'},
				{'x': timestamps['keittion_putket'], 'y': temperatures['keittion_putket'], 'type': 'line', 'name': 'Keittiön putket'},
				{'x': timestamps['vessan_putket'], 'y': temperatures['vessan_putket'], 'type': 'line', 'name': 'Vessan putket'},
				{'x': timestamps['vessa'], 'y': temperatures['vessa'], 'type': 'line', 'name': 'Vessa'},
				{'x': timestamps['kasvihuone'], 'y': temperatures['kasvihuone'], 'type': 'line', 'name': 'Kasvihuone'},
			],
			'layout': {
				'title': 'Lämpötilat',
				'xaxis':{
					'title':''
				},
				'yaxis':{
					 'title':'°C'
				},
				'hovermode': 'x'
			}
		}
	),
	dcc.Graph(
		id='humidities',
		figure={
			'data': [
				{'x': timestamps['sisalla'], 'y': humidities['sisalla'], 'type': 'line', 'name': 'Sisällä'},
				{'x': timestamps['kuisti'], 'y': humidities['kuisti'], 'type': 'line', 'name': 'Kuisti'},
				{'x': timestamps['saunan_putket'], 'y': humidities['saunan_putket'], 'type': 'line', 'name': 'Saunan putket'},
				{'x': timestamps['keittion_putket'], 'y': humidities['keittion_putket'], 'type': 'line', 'name': 'Keittiön putket'},
				{'x': timestamps['vessan_putket'], 'y': humidities['vessan_putket'], 'type': 'line', 'name': 'Vessan putket'},
				{'x': timestamps['vessa'], 'y': humidities['vessa'], 'type': 'line', 'name': 'Vessa'},
				{'x': timestamps['kasvihuone'], 'y': humidities['kasvihuone'], 'type': 'line', 'name': 'Kasvihuone'},
			],
			'layout': {
				'title': 'Kosteus',
				'xaxis':{
					'title':''
				},
				'yaxis':{
					 'title':'%'
				},
                                'hovermode': 'x'
			}
		}
	),
	dcc.Graph(
		id='battery_voltages',
		figure={
			'data': [
				{'x': timestamps['sisalla'], 'y': battery_voltages['sisalla'], 'type': 'line', 'name': 'Sisällä'},
				{'x': timestamps['kuisti'], 'y': battery_voltages['kuisti'], 'type': 'line', 'name': 'Kuisti'},
				{'x': timestamps['saunan_putket'], 'y': battery_voltages['saunan_putket'], 'type': 'line', 'name': 'Saunan putket'},
				{'x': timestamps['keittion_putket'], 'y': battery_voltages['keittion_putket'], 'type': 'line', 'name': 'Keittiön putket'},
				{'x': timestamps['vessan_putket'], 'y': battery_voltages['vessan_putket'], 'type': 'line', 'name': 'Vessan putket'},
				{'x': timestamps['vessa'], 'y': battery_voltages['vessa'], 'type': 'line', 'name': 'Vessa'},
				{'x': timestamps['kasvihuone'], 'y': battery_voltages['kasvihuone'], 'type': 'line', 'name': 'Kasvihuone'},
			],
			'layout': {
				'title': 'Patteri',
				'xaxis':{
					'title':'',
				},
				'yaxis':{
					 'title':'mV'
				},
                                'hovermode': 'x'
			}
		}
	)
])

if __name__ == '__main__':
	ip = subprocess.check_output("hostname -I | awk '{print $1;}'", stderr=subprocess.STDOUT, shell=True)
	app.run_server(debug=True, port=8001, host=ip.decode('utf-8').replace("\n", ""))
