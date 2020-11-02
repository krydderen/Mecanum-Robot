from time import sleep
from roboclaw_3 import Roboclaw 
import time

class MotorController(object):
    def __init__(self):
        # Initialize addresses = [0x80, 0x81]
        self.addresses = [0x80, 0x81]
        
        # Connect to roboclaw
        serial_port = "/dev/ttyS0"
        baudrate    = 38400
        self.roboclaw = Roboclaw(serial_port, baudrate)
        self.roboclaw.Open()
        self.speed = 64
        
    def forward(self, drivetime):
        
        for address in self.addresses:
            self.roboclaw.ForwardMixed(address, self.speed)
        
        sleep(drivetime)
        
        for address in self.addresses:
            self.roboclaw.ForwardMixed(address, 0)
    
    def backward(self, drivetime):
        
        for address in self.addresses:
            self.roboclaw.BackwardMixed(address, self.speed)
        
        sleep(drivetime)
        
        for address in self.addresses:
            self.roboclaw.BackwardMixed(address, 0)
    
    def right(self,drivetime):
        
        self.roboclaw.TurnRightMixed(self.addresses[0], self.speed)
        self.roboclaw.TurnLeftMixed(self.addresses[1], self.speed)
        
        sleep(drivetime)
        
        self.roboclaw.TurnRightMixed(self.addresses[0], 0)
        self.roboclaw.TurnLeftMixed(self.addresses[1], 0)

    def left(self,drivetime):
        
        self.roboclaw.TurnLeftMixed(self.addresses[0], self.speed)
        self.roboclaw.TurnRightMixed(self.addresses[1], self.speed)
        
        sleep(drivetime)
        
        self.roboclaw.TurnLeftMixed(self.addresses[0], 0)
        self.roboclaw.TurnRightMixed(self.addresses[1], 0)
        
    def diagonals(self, direction, drivetime):
        
        if direction == 'northeast' or direction == "wd":
            for address in self.addresses:  
                self.roboclaw.ForwardM1(address, self.speed)
                sleep(drivetime)
        elif direction == 'northwest' or direction == "wa":
            for address in self.addresses:  
                self.roboclaw.ForwardM2(address, self.speed)
                sleep(drivetime)
        elif direction == 'southeast' or direction == "sd":
            for address in self.addresses:  
                self.roboclaw.BackwardM2(address, self.speed)
                sleep(drivetime)
        elif direction == 'southwest' or direction == "sa":
            for address in self.addresses:  
                self.roboclaw.BackwardM1(address, self.speed)
                sleep(drivetime)
    
    def rotate(self, direction, drivetime):
        
        if direction == 'clockwise' or direction == 'e':
            for address in self.addresses:
                self.roboclaw.TurnLeftMixed(address, self.speed)
                sleep(drivetime)

        elif direction == 'counter-clockwise' or direction == 'q':
            for address in self.addresses:
                self.roboclaw.TurnRightMixed(address, self.speed)
                sleep(drivetime)
    
    def stop(self):
        for address in self.addresses:
            self.roboclaw.ForwardMixed(address, 0)
            self.roboclaw.BackwardMixed(address,0)
            self.roboclaw.TurnRightMixed(address,0)
            self.roboclaw.TurnLeftMixed(address,0)
            self.roboclaw.ForwardM1(address,0)
            self.roboclaw.ForwardM2(address,0)
            self.roboclaw.BackwardM1(address,0)
            self.roboclaw.BackwardM2(address,0)