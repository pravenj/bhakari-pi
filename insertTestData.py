from influxdb import InfluxDBClient

json_body = [
    {
        "measurement": "weatherParams",
        "tags": {
            "host": "greenhouse1",
            "region": "Biratnagar"
        },
        "fields": {
            "temperature": 0.42,
            "humidity":75,
            "soilMoisture":525
        }
    }
]

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'weatherData')
client.switch_database('weatherData')
client.write_points(json_body)

