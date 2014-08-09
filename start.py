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





#Encoder class
class Encoder:
    def __init__(self, encoderGPIO):
        #counter variable
        self.encoder_count = 0
        #encoder GPIO (maybe we don't even need it)
        self.encoderGPIO = encoderGPIO

        #which direction (-1=cw/1=ccw)
        self.direction = 1

    def count(self):
        self.encoder_count += self.direction
        print "pin: " + str(self.encGPIO) + " count: " + str(self.enc_count)

    def change_direction(self, direction):
            self.direction = direction

#Motor class
class Motor:
    def __init__(self, motorEnableGPIO, motorSpeedGPIO, encoderGPIO):
        #Enable motor pin
        self.motorEnabledGPIO = motorEnableGPIO
        self.motorSpeedGPIO = motorSpeedGPIO
        self.encoderGPIO = encoderGPIO
        
        self.encoder = Encoder(self.encoderGPIO)
        
        
        GPIO.setup(motorEnableGPIO, GPIO.OUT, initial=GPIO.LOW)

        #motor speed pins (PWM [full_cw ... off ... full_ccw] [0 ... 50 ... 100]
        GPIO.setup(motorSpeedGPIO, GPIO.OUT)

        #setup PWM 50Hz?
        self.motorSpeedPWM = GPIO.PWM(motorSpeedGPIO, 50)

        #counter variable
        self.speed = 0
        self.enabled = False

        #which direction (1=cw/2=ccw)
        self.direction = 1
    def __exit__(self, type, value, traceback):
        self.motorSpeedPWM.stop()

    def set_speed(self, speed):
        #motor direction pins (PWM [full_cw ... off ... full_ccw] [0 ... [35-65] ... 100]
        if speed > -15 and speed < 15:
            self.set_enabled(False)
            self.motorSpeedPWM.stop()
            return
        else:
            self.set_enabled(True)

        #adjust for [0-100] duty cycle
        self.speed = speed + 50

        self.motorSpeedPWM.start(self.speed)
     
        print "Speed: " + str(self.speed)

    def set_enabled(self, enable):
        if enable == True:
            GPIO.output(self.motorEnabledGPIO, GPIO.HIGH)
        else:
            GPIO.output(self.motorEnabledGPIO, GPIO.LOW)


motor_fl = Motor(7, 15, 19)
motor_fl.set_speed(15)

motor_fr = Motor(11, 16, 21)
motor_fr.set_speed(15)

motor_b = Motor(13, 18, 23)
motor_b.set_speed(15)



#encoder gpio lookup table
#encoder_count = {19: encoder_fr.count,
 #          21: encoder_fl.count,
  #         23: encoder_b.count,
#}

#the callback function for the encoders
def encoder_callback(enc_num):

    print "pin change detected: " + str(enc_num)
    #python "switch case" (lookup) to change the right counter variable
    encoder_count[enc_num]()




#append the encoder event to it's callback function
#GPIO.add_event_detect(19, GPIO.BOTH, callback=encoder_callback, bouncetime=2)
#GPIO.add_event_detect(21, GPIO.BOTH, callback=encoder_callback, bouncetime=2)
#GPIO.add_event_detect(23, GPIO.BOTH, callback=encoder_callback, bouncetime=2)



# 'bouncetime=300' includes the bounce control written into interrupts2a.py

try:
    print "Waiting for rising edge on port 24"
    while 1:
      time.sleep(10)
      print '.'



except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit


GPIO.cleanup()           # clean up GPIO on normal exit
