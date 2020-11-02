from roboclaw_3 import Roboclaw
from time import sleep

addresses = [0x81,0x80]
roboclaw = Roboclaw("/dev/ttyS0", 38400)
roboclaw.Open()


for address in addresses:
    print('drive')
    roboclaw.ForwardM1(address, 32)
    print('sleep1')
    sleep(1)
    print('stopping')
    roboclaw.ForwardM1(address, 0)
    print('stopped')