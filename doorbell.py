""" * Before you run the code, do not forget to start the pigpiod daemon * 
using "sudo pigpiod". * """
#import the libraries used
import smtplib
import time  
import pigpio 
import RPi.GPIO as GPIO
from threading import Thread
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
server.login("testsm9920","testsm20*")
ai=True
try: 
	while True : 
	
		if calculate_distance() < 15:
			if ai==True :
				msg="You have a visitor!"
				server.sendmail("testsm9920@gmail.com","ursan_robert@yahoo.com",msg)
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
				server.sendmail("testsm9920@gmail.com","ursan_robert@yahoo.com",msg)
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
