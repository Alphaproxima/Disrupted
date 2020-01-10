import Adafruit_DHT
import dweepy
import time

sensor = Adafruit_DHT.DHT11
gpio = 4

while True:
   humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

   if humidity is not None and temperature is not None:
	print(‘Temp={0:0.1f}*C Humidity={1:0.1f}%’.format(temperature, humidity))
   else:
	print(‘ Failed to get reading, Try again’)

   # Send the data to Cloud
   dweepy.dweet_for(‘Humid’, {‘Temp’: temperature})
   dweepy.dweet_for(‘Humid’, {‘Humid’: humidity})

   # Please check and access dweet.io/follow/Humid
