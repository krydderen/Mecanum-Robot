from serial import Serial
from time import sleep
import RPi.GPIO as GPIO
import math

class MotorController(object):
    
    
    
    def __init__(self):
        #Configure serial 
        serial_port = "/dev/ttyS0"
        baudrate = 38400
        self.roboclaw = Serial(serial_port, baudrate, timeout=1)
        
        #Configure GPIO
        
        global slave_select_pins
        slave_select_pins = [23,24]
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(slave_select_pins, GPIO.OUT, initial=GPIO.LOW)
        
        self.__FULL_FORWARD    = [127  , 255]
        self.__FULL_REVERSE    = [1    , 123]
        self.__FULL_STOP       =  0
        self.__HALF_FORWARD    = [98   , 225]
        self._HALF_REVERSE    = [30   , 158]
        self.__MOTOR_WAIT_TIME =  0.02
        self.__FORWARD_SPEED   = [98   , 225]
        self.__REVERSE_SPEED   = [30   , 158]
    
    def speed_change(self, newspeed):
        claw_forward = [65, 127, 193, 255] #min, max values for channel 1. min, max for channel 2 
        claw_reverse = [63, 1, 191, 128]
        claw_range = 62
        minmax = [0,100]
        minmax_range = minmax[1]-minmax[0]
        if newspeed == 0:
            self.__FORWARD_SPEED = [0, 0]
            self.__REVERSE_SPEED = [0, 0]
            return
        elif newspeed in range(1,9):
            newspeed = 10
            
        self.__FORWARD_SPEED = [(((newspeed)*claw_range)/minmax_range)+claw_forward[0],
                                    (((newspeed)*claw_range)/minmax_range)+claw_forward[2]]
        self.__REVERSE_SPEED = [(((-newspeed)*claw_range)/minmax_range)+claw_reverse[0],
                                    (((-newspeed)*claw_range)/minmax_range)+claw_reverse[2]]
        
        print(self.__FORWARD_SPEED)
        print(self.__REVERSE_SPEED)
        
    def left(self, drivetime, inputspeed):
        self.fspeed = self.__FORWARD_SPEED
        self.rspeed = self.__REVERSE_SPEED
        
        # REAR MOTOR 
        # Write forward for motor 1 and backward for motor 2
        GPIO.output(23, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[0]));
        self.roboclaw.write(chr(self.rspeed[1]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(23, GPIO.LOW)
        
        # FRONT MOTOR 
        # Write forward for motor 1 and backward for motor 2
        GPIO.output(24, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[0]));
        self.roboclaw.write(chr(self.rspeed[1]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(24, GPIO.LOW)
        
        sleep(drivetime)

    def right(self, drivetime, inputspeed):
        self.fspeed = self.__FORWARD_SPEED
        self.rspeed = self.__REVERSE_SPEED
        
        # REAR MOTOR
        # Write forward for motor 2 and backward for motor 1
        GPIO.output(23, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[1]));
        self.roboclaw.write(chr(self.rspeed[0]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(23, GPIO.LOW)
        
        # FRONT MOTOR 
        # Write forward for motor 2 and backward for motor 1
        GPIO.output(24, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[1]));
        self.roboclaw.write(chr(self.rspeed[0]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(24, GPIO.LOW)
        
        sleep(drivetime)
    
    def wddiagonal(self, drivetime, inputspeed):
        self.fspeed = self.__FORWARD_SPEED
        self.rspeed = self.__REVERSE_SPEED
        
        # REAR MOTOR
        # Write forward for motor 2 
        GPIO.output(23, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[1]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(23, GPIO.LOW)
        
        # FRONT MOTOR 
        # Write forward for motor 2
        GPIO.output(24, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[1]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(24, GPIO.LOW)
        
        sleep(drivetime)
        
    def wadiagonal(self, drivetime, inputspeed):
        self.fspeed = self.__FORWARD_SPEED
        self.rspeed = self.__REVERSE_SPEED
        
        # REAR MOTOR
        # Write forward for motor 2 
        GPIO.output(23, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[0]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(23, GPIO.LOW)
        
        # FRONT MOTOR 
        # Write forward for motor 2
        GPIO.output(24, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[0]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(24, GPIO.LOW)
        
        sleep(drivetime)
        
    def sadiagonal(self, drivetime, inputspeed):
        self.fspeed = self.__FORWARD_SPEED
        self.rspeed = self.__REVERSE_SPEED
        
        # REAR MOTOR
        # Write forward for motor 2 
        GPIO.output(23, GPIO.HIGH)
        self.roboclaw.write(chr(self.rspeed[1]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(23, GPIO.LOW)
        
        # FRONT MOTOR 
        # Write forward for motor 2
        GPIO.output(24, GPIO.HIGH)
        self.roboclaw.write(chr(self.rspeed[1]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(24, GPIO.LOW)
        
        sleep(drivetime)
        
    def sddiagonal(self, drivetime, inputspeed):
        self.fspeed = self.__FORWARD_SPEED
        self.rspeed = self.__REVERSE_SPEED
        
        # REAR MOTOR
        # Write forward for motor 2 
        GPIO.output(23, GPIO.HIGH)
        self.roboclaw.write(chr(self.rspeed[0]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(23, GPIO.LOW)
        
        # FRONT MOTOR 
        # Write forward for motor 2
        GPIO.output(24, GPIO.HIGH)
        self.roboclaw.write(chr(self.rspeed[0]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(24, GPIO.LOW)
        
        sleep(drivetime)
    

    def forward(self, drivetime, inputspeed):
        self.fspeed = self.__FORWARD_SPEED
        
        # Write forward for 1 and 2
        GPIO.output(23, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[0]));
        self.roboclaw.write(chr(self.fspeed[1]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(23, GPIO.LOW)
        
        # Write forward for 1 and 2
        GPIO.output(24, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[0]));
        self.roboclaw.write(chr(self.fspeed[1]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(24, GPIO.LOW)
        
        sleep(drivetime)
    
    def fforward(self, drivetime = 1, inputspeed = 'LOW'):
        self.fspeed = 0
        
        if inputspeed == 'HIGH':
            self.fspeed = self.__FULL_FORWARD
        elif inputspeed == 'LOW':
            self.fspeed = self.__HALF_FORWARD        
        
        # Write forward for 1 and 2
        GPIO.output(23, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[0]));
        self.roboclaw.write(chr(self.fspeed[1]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(23, GPIO.LOW)
        
        # Write forward for 1 and 2
        GPIO.output(24, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[0]));
        self.roboclaw.write(chr(self.fspeed[1]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(24, GPIO.LOW)
        
        sleep(drivetime)
        
    def backward(self, drivetime, inputspeed):
        self.rspeed = self.__REVERSE_SPEED
        
        # Write backward for 1 and 2
        GPIO.output(23, GPIO.HIGH)
        self.roboclaw.write(chr(self.rspeed[0]));
        self.roboclaw.write(chr(self.rspeed[1]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(23, GPIO.LOW)
        
        # Write backward for 1 and 2
        GPIO.output(24, GPIO.HIGH)
        self.roboclaw.write(chr(self.rspeed[0]));
        self.roboclaw.write(chr(self.rspeed[1]));
        sleep(self.__MOTOR_WAIT_TIME)
        GPIO.output(24, GPIO.LOW)
        
        sleep(drivetime)
        
    def stop_controller(self, pin):
        GPIO.output(pin, GPIO.HIGH)
        self.roboclaw.write(chr(self.__FULL_STOP));
        sleep(self.__MOTOR_WAIT_TIME);
        GPIO.output(pin, GPIO.LOW)
        
    def stop(self):
        self.stop_controller(slave_select_pins[0])
        self.stop_controller(slave_select_pins[1])

    def rotate(self, drivetime, direction, inputspeed):
        self.fspeed = self.__FORWARD_SPEED
        self.rspeed = self.__REVERSE_SPEED
        
        if direction == 'CLOCKWISE':
            # REAR MOTOR left motor forward and right motor backward
            GPIO.output(23, GPIO.HIGH)
            self.roboclaw.write(chr(self.rspeed[1])); # RIGHT X
            self.roboclaw.write(chr(self.fspeed[0])); # LEFT X
            sleep(self.__MOTOR_WAIT_TIME)
            GPIO.output(23, GPIO.LOW)
            
            # FRONT MOTOR left motor forward and right motor backward
            GPIO.output(24, GPIO.HIGH)
            self.roboclaw.write(chr(self.fspeed[1])); # LEFT X
            self.roboclaw.write(chr(self.rspeed[0])); # RIGHT 
            sleep(self.__MOTOR_WAIT_TIME)
            GPIO.output(24, GPIO.LOW)
            sleep(drivetime)
            
        elif direction == 'COUNTER_CLOCKWISE':
            # REAR MOTOR left motor forward and right motor backward
            GPIO.output(23, GPIO.HIGH)
            self.roboclaw.write(chr(self.fspeed[1])); # RIGHT X
            self.roboclaw.write(chr(self.rspeed[0])); # LEFT X
            sleep(self.__MOTOR_WAIT_TIME)
            GPIO.output(23, GPIO.LOW)
            
            # FRONT MOTOR left motor forward and right motor backward
            GPIO.output(24, GPIO.HIGH)
            self.roboclaw.write(chr(self.rspeed[1])); # LEFT X
            self.roboclaw.write(chr(self.fspeed[0])); # RIGHT 
            sleep(self.__MOTOR_WAIT_TIME)
            GPIO.output(24, GPIO.LOW)
            sleep(drivetime)