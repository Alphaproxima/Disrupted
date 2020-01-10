import time
import RPi.GPIO as GPIO
import dweepy

# Set GPIO IO mode, 
# pin based on gpio number  
GPIO.setmode(IO.BCM)

# Turn off the warning to run the pi
GPIO.setwarnings(False) 
# Set the GPIO Pin
GPIO_TRIGGER = 23
GPIO_ECHO = 24

# Set GPIO as IN/OUT 
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN) 

# Create a function for calculating the distance
def distance():
	
	#Set trigger high
	GPIO.output(GPIO_TRIGGER, True)

	#Set trigger after 0.01ms to Low
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)

	StartTime = time.time()
	StopTime = time.time()

	#Save the start time
	while GPIO.input(GPIO_ECHO)==0:
		StartTime = time.time()

	#Save the time of arrive
	while GPIO.input(GPIO_ECHO)==1:
		StopTime = time.time()

	#Time difference between start and arrival
	TimeElapsed = StopTime – StartTime
	
	#Multiply with the speed of sound (34300 cm/s)
	#Divide by two, because go and back waves
	distance = (TimeElapsed *343000)/2

	return distance

# Loop forever until interrupted
if __name__ == ‘__main__’:
	try:
		while True:
			dist = distance()
			print(“Measured Distance = %.1f cm” % dist)
			
			#Upload the data to the cloud
			dweepy.dweep_for(‘workshop’, {‘distance’:dist})

			#Upload for 2 seconds
			time.sleep(2)

	# Reset by pressing ctrl+c
	except KeyboardInterrupt:
		print(“Measurement stopped”)
		GPIO.cleanup()
