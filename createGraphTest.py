from influxdb import DataFrameClient
import pandas as pd
import matplotlib.pyplot as plt

client = DataFrameClient('localhost', 8086, 'root', 'root', 'weatherData')
client.switch_database('weatherData')
data = client.query('select * from weatherParams;')
df = data["weatherParams"].reset_index()

plt.style.use('ggplot')
fig, ax = plt.subplots()
fig.set_size_inches(8.9,5.0)
fig.set_dpi(80)
fig.set_tight_layout(True)
plt.xticks(rotation=70)
ax.plot(df["index"], df["humidity"], label="HT")
ax.legend()
plt.show()
