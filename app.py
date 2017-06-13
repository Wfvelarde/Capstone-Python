import RPi.GPIO as GPIO
import urllib2
import json
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

pwm = GPIO.PWM(18, 50)

data = urllib2.urlopen("https://sleepy-brushlands-11143.herokuapp.com/lockstatuses").read()
decoded = json.loads(data)
status = decoded[0]['status']
last_position = status
print "The current position of the lock is " + last_position

try:
        while True:
                data = urllib2.urlopen("https://sleepy-brushlands-11143.herokuapp.com/lockstatuses").read()
                decoded = json.loads(data)
                status = decoded[0]['status']
                if status != last_position:
                        print "The lock has switched to " + status
                        if status == 'open':
                                pwm.start(7.5)
                                pwm.ChangeDutyCycle(7.5)
                                time.sleep(1)
                                last_position = status
                                print "Lock is " + status
                        elif status == 'closed':
                                pwm.start(7.5)
                                pwm.ChangeDutyCycle(2.5)
                                time.sleep(1)
                                last_position = status
                                print "Lock is " + status
                else:
                        time.sleep(1)

except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()
        print "Process terminated"