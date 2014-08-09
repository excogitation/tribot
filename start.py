import time
import sys
import RPi.GPIO as GPIO

#pin number = gpio number! otherwise use BCM
GPIO.setmode(GPIO.BOARD)

#GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#setup the encoder pins - don't use internal pull-up/down
#there is allready an external pull-down in place
#from the 5v/3V conversion through 15k-gnd/10k-5v resistors

GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

#Enable motor pins (fr, fl, b) GPIO.LOW == 0
GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)

#motor direction pins (PWM [full_cw ... off ... full_ccw] [0 ... 50 ... 100]
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

#todo: put in motor class /drive class
#setup PWM 50Hz?
motor_fl = GPIO.PWM(15, 50)
motor_fr = GPIO.PWM(16, 50)
motor_b = GPIO.PWM(18, 50)

GPIO.output(7, GPIO.HIGH)
GPIO.output(11, GPIO.HIGH)
GPIO.output(13, GPIO.HIGH)

motor_fl.start(35)
motor_fr.start(35)
motor_b.start(35)



#Encoder class
class Encoder:
    def __init__(self, encGPIO):
        #counter variable
        self.enc_count = 0
        #encoder GPIO (maybe we don't even need it)
        self.encGPIO = encGPIO

        #which direction (1=cw/2=ccw)
        self.direction = 1

    def count(self):
        self.enc_count += self.direction
        print "pin: " + str(self.encGPIO) + " count: " + str(self.enc_count)

    def change_dir(self, direction):
        if direction == "cw":
            self.direction = 1
        elif direction == "ccw":
            self.direction = -1
        else:
            print "what direction is that supposed to be?"


# instantiate the three encoder objects
encoder_fr = Encoder(19)
encoder_fl = Encoder(21)
encoder_b = Encoder(23)

encoder_fr.change_dir("ccw")

#encoder gpio lookup table
encoder_count = {19: encoder_fr.count,
           21: encoder_fl.count,
           23: encoder_b.count,
}

#the callback function for the encoders
def encoder_callback(enc_num):

    print "pin change detected: " + str(enc_num)
    #python "switch case" (lookup) to change the right counter variable
    encoder_count[enc_num]()




#append the encoder event to it's callback function
GPIO.add_event_detect(19, GPIO.BOTH, callback=encoder_callback, bouncetime=2)
GPIO.add_event_detect(21, GPIO.BOTH, callback=encoder_callback, bouncetime=2)
GPIO.add_event_detect(23, GPIO.BOTH, callback=encoder_callback, bouncetime=2)



# 'bouncetime=300' includes the bounce control written into interrupts2a.py

try:
    print "Waiting for rising edge on port 24"
    while 1:
      time.sleep(100)
      print '.'



except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    motor_fr.stop()
    motor_fb.stop()
    motor_b.stop()

GPIO.cleanup()           # clean up GPIO on normal exit
