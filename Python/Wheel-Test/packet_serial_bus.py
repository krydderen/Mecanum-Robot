from roboclaw_3 import Roboclaw 
from time import sleep

# addresses = [0x80,0x81,0x82,0x83]
address = 0x80
roboclaw = Roboclaw("/dev/ttyS0", 38400)
roboclaw.Open()


roboclaw.ForwardM1(address,64)
sleep(2)
roboclaw.ForwardM1(address,0)
sleep(2)