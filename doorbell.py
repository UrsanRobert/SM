"""When we approach our hand to the sensor, the buzzer will make some noise, so we can hear that someone rings. 
Also,we have 2 LED's. The green one is on when there is no visitor, while the red one is off. 
When a visitor approach his hand to the sensor, the green LED is off and the red one is on. 
Also, when we approach our hand to the sensor, an email will be sent to a specific email address with content "You have a visitor". 
When the visitor left, another email will be sent to the same email address with content "The visitor left!"
* Before you run the code, do not forget to start the pigpiod daemon * 
using "sudo pigpiod". * """
#import the libraries used
import smtplib
import time  
import pigpio 
import RPi.GPIO as GPIO
#create an instance of the pigpio library
pi = pigpio.pi()
#define the pin used by the Buzzer this pin will be used by the pigpio 
#library which takes the pins in GPIO forms we will use GPIO18, which is 
#pin 12
buzzer = 18
#set the pin used by the buzzer as OUTPUT
pi.set_mode(buzzer, pigpio.OUTPUT) 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#define the pins used by the ultrasonic module
trig = 32 
echo = 38
#set the trigger pin as OUTPUT, the echo as INPUT, the no.8 pin as OUTPUT
#and the no.10 pin as OUTPUT
GPIO.setup(trig, GPIO.OUT) 
GPIO.setup(echo, GPIO.IN) 
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
def calculate_distance():
    #set the trigger to HIGH
	GPIO.output(trig, GPIO.HIGH)
    #sleep 0.00001 s and the set the trigger to LOW
	time.sleep(0.00001) 
	GPIO.output(trig, GPIO.LOW)
    #save the start and stop times
    	start = time.time() 
	stop = time.time()
    #modify the start time to be the last time until the echo becomes 
    #HIGH
    	while GPIO.input(echo) == 0:
		start = time.time()
    #modify the stop time to be the last time until the echo becomes LOW
   	while GPIO.input(echo) == 1: 
		stop = time.time()
    #get the duration of the echo pin as HIGH
    	duration = stop - start
    #calculate the distance
    	distance = 34300/2 * duration 
	if distance < 0.5 and distance > 400: 
        	return 0
    	else:
        #return the distance
        	return distance 

GPIO.output(8, GPIO.LOW)
GPIO.output(10,GPIO.HIGH)
server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login("username","password")
ai=True
try: 
	while True : 
	
		if calculate_distance() < 15:
			if ai==True :
				msg="You have a visitor!"
				server.sendmail("sender","receiver",msg)
				GPIO.output(8, GPIO.HIGH)
				GPIO.output(10, GPIO.LOW)
				ai=False
			pi.hardware_PWM(buzzer, 500, 500000)
			time.sleep(0.05)
         #turn off the buzzer and wait 50 ms
 	  		pi.hardware_PWM(buzzer, 0, 0) 
			time.sleep(0.05)

		else:
			if ai==False:
				msg="The visitor left!"
				server.sendmail("sender","receiver",msg)
				GPIO.output(8, GPIO.LOW)
				GPIO.output(10, GPIO.HIGH)
				ai=True
			pi.hardware_PWM(buzzer,0,0)
		
		time.sleep(0.1)

except KeyboardInterrupt: 
	pass
server.quit()
#turn off the buzzer
pi.write(buzzer, 0)
#stop the connection with the daemon
pi.stop()
#clean all the used ports
GPIO.cleanup()
