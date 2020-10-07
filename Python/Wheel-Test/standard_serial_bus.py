from serial import Serial
from time import sleep
import RPi.GPIO as GPIO

global roboclaw
global HALF_FORWARD
global HALF_REVERSE
global FULL_FORWARD
global FULL_REVERSE
global FULLSTOP
global MOTORWAITTIME

FULL_FORWARD = [127  , 255]
FULL_REVERSE = [1    , 128]
FULLSTOP    = 0
HALF_FORWARD = [98   , 225]
HALF_REVERSE = [30   , 158]
MOTORWAITTIME = 0.002

def motion():
    global MOTORWAITTIME
    global FULL_FORWARD
    global FULL_REVERSE
    global HALF_FORWARD
    global HALF_REVERSE
    fspeed = 0
    rspeed = 0
    
    if inputspeed == 'HIGH':
        fspeed = FULL_FORWARD
        rspeed = FULL_REVERSE
    elif inputspeed == 'LOW':
        fspeed = HALF_FORWARD
        rspeed = HALF_REVERSE
        
    # REAR MOTOR
    GPIO.output(23, GPIO.HIGH)
    #Forward 1
    roboclaw.write(chr(FULL_FORWARD[0])); # RIGHT 
    #Forward 2
    roboclaw.write(chr(FULL_FORWARD[1])); # LEFT
    #Backward 1
    roboclaw.write(chr(FULL_REVERSE[0])); # RIGHT 
    #Backward 2
    roboclaw.write(chr(FULL_REVERSE[1])); # LEFT 
    
    sleep(MOTORWAITTIME)
    GPIO.output(23, GPIO.LOW)
    
    # FRONT MOTOR 
    GPIO.output(24, GPIO.HIGH)
    #Forward 1
    roboclaw.write(chr(FULL_FORWARD[0])); # LEFT 
    #Forward 2
    roboclaw.write(chr(FULL_FORWARD[1])); # RIGHT
    #Backward 1
    roboclaw.write(chr(FULL_REVERSE[0])); # LEFT
    #Backward 2
    roboclaw.write(chr(FULL_REVERSE[1])); # RIGHT 

    sleep(MOTORWAITTIME)
    GPIO.output(24, GPIO.LOW)
    sleep(1)
    
def left(drivetime, inputspeed):
    global MOTORWAITTIME
    global FULL_FORWARD
    global FULL_REVERSE
    global HALF_FORWARD
    global HALF_REVERSE
    fspeed = 0
    rspeed = 0
    
    if inputspeed == 'HIGH':
        fspeed = FULL_FORWARD
        rspeed = FULL_REVERSE
    elif inputspeed == 'LOW':
        fspeed = HALF_FORWARD
        rspeed = HALF_REVERSE
    
    # REAR MOTOR
    GPIO.output(23, GPIO.HIGH)
    #Forward 1
    roboclaw.write(chr(fspeed[0])); # RIGHT X
    #Backward 2
    roboclaw.write(chr(rspeed[1])); # LEFT X
    
    sleep(MOTORWAITTIME)
    GPIO.output(23, GPIO.LOW)
    
    # FRONT MOTOR 
    GPIO.output(24, GPIO.HIGH)
    #Forward 1
    roboclaw.write(chr(fspeed[0])); # LEFT X
    #Backward 2
    roboclaw.write(chr(rspeed[1])); # RIGHT X

    sleep(MOTORWAITTIME)
    GPIO.output(24, GPIO.LOW)
    sleep(drivetime)

def right(drivetime, inputspeed):
    global MOTORWAITTIME
    global FULL_FORWARD
    global FULL_REVERSE
    global HALF_FORWARD
    global HALF_REVERSE
    fspeed = 0
    rspeed = 0
    
    if inputspeed == 'HIGH':
        fspeed = FULL_FORWARD
        rspeed = FULL_REVERSE
    elif inputspeed == 'LOW':
        fspeed = HALF_FORWARD
        rspeed = HALF_REVERSE
    
    # REAR MOTOR
    GPIO.output(23, GPIO.HIGH)
    #Forward 1
    #roboclaw.write(chr(FULL_FORWARD[0])); # RIGHT x
    #Forward 2
    roboclaw.write(chr(FULL_FORWARD[1])); # LEFT
    #Backward 1
    roboclaw.write(chr(FULL_REVERSE[0])); # RIGHT 
    #Backward 2
    #roboclaw.write(chr(FULL_REVERSE[1])); # LEFT x
    
    sleep(MOTORWAITTIME)
    GPIO.output(23, GPIO.LOW)
    
    # FRONT MOTOR 
    GPIO.output(24, GPIO.HIGH)
    #Forward 1
    #roboclaw.write(chr(FULL_FORWARD[0])); # LEFT x
    #Forward 2
    roboclaw.write(chr(FULL_FORWARD[1])); # RIGHT
    #Backward 1
    roboclaw.write(chr(FULL_REVERSE[0])); # LEFT
    #Backward 2
    #roboclaw.write(chr(FULL_REVERSE[1])); # RIGHT x

    sleep(MOTORWAITTIME)
    GPIO.output(24, GPIO.LOW)
    sleep(drivetime)

def run_controller(pin, speed):
    
    GPIO.output(pin, GPIO.HIGH)
    #sleep(.2);
    roboclaw.write(chr(speed));
    #sleep(run_time)
    
def forward(drivetime, inputspeed):
    global MOTORWAITTIME
    global FULL_FORWARD
    global HALF_FORWARD
    fspeed = 0
    
    if inputspeed == 'HIGH':
        fspeed = FULL_FORWARD
    elif inputspeed == 'LOW':
        fspeed = HALF_FORWARD
    
    GPIO.output(23, GPIO.HIGH)
    #Forward 1
    roboclaw.write(chr(fspeed[0]));
    #Forward 2
    roboclaw.write(chr(fspeed[1]));
    sleep(MOTORWAITTIME)
    GPIO.output(23, GPIO.LOW)
    
    GPIO.output(24, GPIO.HIGH)
    #Forward 1
    roboclaw.write(chr(fspeed[0]));
    #Forward 2
    roboclaw.write(chr(fspeed[1]));
    sleep(MOTORWAITTIME)
    GPIO.output(24, GPIO.LOW)
    sleep(drivetime)
    
def backward(drivetime):
    global MOTORWAITTIME
    global FULL_REVERSE
    global HALF_REVERSE
    
    GPIO.output(23, GPIO.HIGH)
    #Backward 1
    roboclaw.write(chr(HALF_REVERSE[0]));
    #Backward 2
    roboclaw.write(chr(HALF_REVERSE[1]));
    sleep(MOTORWAITTIME)
    GPIO.output(23, GPIO.LOW)
    
    GPIO.output(24, GPIO.HIGH)
    #Backward 1
    roboclaw.write(chr(HALF_REVERSE[0]));
    #Backward 2
    roboclaw.write(chr(HALF_REVERSE[1]));
    sleep(MOTORWAITTIME)
    GPIO.output(24, GPIO.LOW)
    sleep(drivetime)
        
def stop_controller(pin):
    global MOTORWAITTIME
    GPIO.output(pin, GPIO.HIGH)
    roboclaw.write(chr(0));
    sleep(MOTORWAITTIME);
    GPIO.output(pin, GPIO.LOW)
    
def stop():
    
    stop_controller(slave_select_pins[0])
    stop_controller(slave_select_pins[1])

if __name__ == "__main__":
    
    #GPIO.cleanup()
    
    #Configure serial
    
    serial_port = "/dev/ttyS0"
    baudrate = 38400
    roboclaw = Serial(serial_port, baudrate, timeout=1)
    
    #Configure GPIO
    
    global slave_select_pins
    slave_select_pins = [23,24]
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(slave_select_pins, GPIO.OUT, initial=GPIO.LOW)
    
    while(1):
        #GPIO.cleanup()
        
        #forward(1, 'LOW')
        #stop()
        #sleep(0.5)
        #left(1, 'LOW')
        right(1,'LOW')
        
        stop()
        sleep(2)
        
    GPIO.cleanup()