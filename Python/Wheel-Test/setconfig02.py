from roboclaw_3 import Roboclaw
from time import sleep

if __name__ == "__main__":
    
    address = 0x82
    roboclaw = Roboclaw("/dev/ttyS0", 38400)
    roboclaw.Open()
    
    config = roboclaw.GetConfig(address)
    print(config)
    
    input()
    
    pack = 0x0003
    baud = 0x0060
    addr = 0x0100
    mum  = 0x8000
    test = 0x8163
    print('setting config ', pack | baud | addr | mum)
    #roboclaw.SetConfig(address, (pack | baud | addr | mum))
    roboclaw.SetConfig(address,test)
    
    print('new settings')
    print(roboclaw.GetConfig(address))
    
    """while True:
        
        roboclaw.ForwardM1(address,64)
        sleep(2)
        roboclaw.ForwardM1(address,0)
        sleep(2)
        
        roboclaw.ForwardM2(address, 64)
        sleep(2)
        roboclaw.ForwardM2(address,0)
        sleep(2)"""
    
    