import time
import grovepi
from influxdb import InfluxDBClient
#from numbers import Number
temp_humidity=3
gas_sensor = 0
relay=4

grovepi.pinMode(temp_humidity,"INPUT")
grovepi.pinMode(gas_sensor,"INPUT")
grovepi.pinMode(relay,"OUTPUT")

# Generates the necessary payload to post
# temperature data into the InfluxDB

capture_interval = 5.0 # Every 5 seconds

client = InfluxDBClient('localhost','8086','root','root','testdb')
while True:
   try:
        # Get temperature and humidity sensor value
        [temp,humidity] = grovepi.dht(temp_humidity,1)

	print("Temp.: {0}".format(temp))
        print("Humidity: {0}".format(humidity))

	json_body = [
	{
	"measurement": "WeatherData",
	"tags": {
	"Project": "Green-house"
	},
	"fields": {
	   "Temperature": temp,
	   "Humidity": humidity,
      		 }
	}
	]
	if (temp>0 and temp<100) and (humidity>0 and humidity<100): 
		print("Temp.: {0}".format(temp))
		client.write_points(json_body)
	        if humidity > 65 or temp > 14:
	       	    grovepi.digitalWrite(relay,0)
		else:
	            grovepi.digitalWrite(relay,1)
	time.sleep(capture_interval)
   except KeyboardInterrupt:
        grovepi.digitalWrite(relay,1)
        break
   except IOError:
        print ("Error")
