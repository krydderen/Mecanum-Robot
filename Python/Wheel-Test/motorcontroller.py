from serial import Serial
from time import sleep
import RPi.GPIO as GPIO

class MotorController:
    __FULL_FORWARD    = [127  , 255]
    __FULL_REVERSE    = [1    , 128]
    __FULLSTOP        = 0
    __HALF_FORWARD    = [98   , 225]
    __HALF_REVERSE    = [30   , 158]
    __MOTORWAITTIME   = 0.002
    
    def __init__(self):
        #Configure serial 
        serial_port = "/dev/ttyS0"
        baudrate = 38400
        roboclaw = Serial(serial_port, baudrate, timeout=1)
        
        #Configure GPIO
        
        global slave_select_pins
        slave_select_pins = [23,24]
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(slave_select_pins, GPIO.OUT, initial=GPIO.LOW)
    
    def left(self, drivetime, inputspeed):
        self.fspeed = 0
        self.rspeed = 0
        
        if inputspeed   == 'HIGH':
            self.fspeed = self.__FULL_FORWARD
            self.rspeed == self.__FULL_REVERSE
        elif inputspeed == 'LOW': ##else istede førr elif??
            self.fspeed = self.__HALF_FORWARD
            self.rspeed = self.__HALF_REVERSE
        
        # REAR MOTOR 
        # Write forward for motor 1 and backward for motor 2
        GPIO.output(23, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[0]));
        self.roboclaw.write(chr(self.rspeed[1]));
        sleep(self.MOTORWAITTIME)
        GPIO.output(23, GPIO.LOW)
        
        # FRONT MOTOR 
        # Write forward for motor 1 and backward for motor 2
        GPIO.output(24, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[0]));
        self.roboclaw.write(chr(self.rspeed[1]));
        sleep(self.MOTORWAITTIME)
        GPIO.output(24, GPIO.LOW)
        
        sleep(drivetime)

    def right(self, drivetime, inputspeed):
        self.fspeed = 0
        self.rspeed = 0
        
        if inputspeed   == 'HIGH':
            self.fspeed = self.__FULL_FORWARD
            self.rspeed = self.__FULL_REVERSE
        elif inputspeed == 'LOW':
            self.fspeed = self.__HALF_FORWARD
            self.rspeed = self.__HALF_REVERSE
        
        # REAR MOTOR
        # Write forward for motor 2 and backward for motor 1
        GPIO.output(23, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[1]));
        self.roboclaw.write(chr(self.rspeed[0]));
        sleep(self.MOTORWAITTIME)
        GPIO.output(23, GPIO.LOW)
        
        # FRONT MOTOR 
        # Write forward for motor 2 and backward for motor 1
        GPIO.output(24, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[1]));
        self.roboclaw.write(chr(self.rspeed[0]));
        sleep(self.MOTORWAITTIME)
        GPIO.output(24, GPIO.LOW)
        
        sleep(drivetime)
    
    def forward(self, drivetime, inputspeed):
        self.fspeed = 0
        
        if inputspeed == 'HIGH':
            fspeed = self.__FULL_FORWARD
        elif inputspeed == 'LOW':
            fspeed = self.__HALF_FORWARD
        
        # Write forward for 1 and 2
        GPIO.output(23, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[0]));
        self.roboclaw.write(chr(self.fspeed[1]));
        sleep(self.MOTORWAITTIME)
        GPIO.output(23, GPIO.LOW)
        
        # Write forward for 1 and 2
        GPIO.output(24, GPIO.HIGH)
        self.roboclaw.write(chr(self.fspeed[0]));
        self.roboclaw.write(chr(self.fspeed[1]));
        sleep(self.MOTORWAITTIME)
        GPIO.output(24, GPIO.LOW)
        
        sleep(drivetime)
    
    def backward(self, drivetime, inputspeed):
        self.rspeed = 0
        
        if inputspeed == 'HIGH':
            self.rspeed = self.__FULL_REVERSE
        elif inputspeed == 'LOW':
            self.rspeed = self.__HALF_REVERSE
        
        # Write backward for 1 and 2
        GPIO.output(23, GPIO.HIGH)
        self.roboclaw.write(chr(self.rspeed[0]));
        self.roboclaw.write(chr(self.rspeed[1]));
        sleep(self.__MOTORWAITTIME)
        GPIO.output(23, GPIO.LOW)
        
        # Write backward for 1 and 2
        GPIO.output(24, GPIO.HIGH)
        self.roboclaw.write(chr(self.rspeed[0]));
        self.roboclaw.write(chr(self.rspeed[1]));
        sleep(self.__MOTORWAITTIME)
        GPIO.output(24, GPIO.LOW)
        
        sleep(drivetime)
        
    def stop_controller(self, pin):
        GPIO.output(pin, GPIO.HIGH)
        self.roboclaw.write(chr(self.__FULLSTOP));
        sleep(self.__MOTORWAITTIME);
        GPIO.output(pin, GPIO.LOW)
        
    def stop(self):
        self.stop_controller(slave_select_pins[0])
        self.stop_controller(slave_select_pins[1])
