from roboclaw_3 import Roboclaw
from time import sleep

addresses = [0x80,0x81]
roboclaw = Roboclaw("/dev/ttyS0", 38400)
roboclaw.Open()


for address in addresses:
    print('drive')
    roboclaw.ForwardMixed(address, 64)
    print('sleep1')
    sleep(1)
    print('stopping')
    roboclaw.ForwardMixed(address, 0)
    print('stopped')