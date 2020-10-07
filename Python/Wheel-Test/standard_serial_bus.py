from serial import Serial
from time import sleep
import RPi.GPIO as GPIO

def run_controller(pin, speed):
    
    GPIO.output(pin, GPIO.HIGH)
    #sleep(.2);
    roboclaw.write(chr(speed));
    #sleep(run_time)
    
def forward():
    global slave_select_pins
    #Controller 1 full backward
    run_controller(slave_select_pins[0], 63)
    run_controller(slave_select_pins[0], 191)
    #Controller 2 full forward
    run_controller(slave_select_pins[1], 1)
    run_controller(slave_select_pins[1], 128)
    
def stop_controller(pin):
    GPIO.output(pin, GPIO.HIGH)
    roboclaw.write(chr(0));
    sleep(.001);
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
        
        GPIO.output(23, GPIO.HIGH)
        #sleep(.2);
        #Forward 1
        roboclaw.write(chr(127));
        #Backward 1
        #roboclaw.write(chr(1));
        #Forward 2
        #roboclaw.write(chr(255));
        #Backward 2
        #roboclaw.write(chr(128));
        #It gotta slee??
        sleep(0.001)
        GPIO.output(23, GPIO.LOW)
        
        GPIO.output(24, GPIO.HIGH)
        #sleep(.2);
        #Forward 1
        roboclaw.write(chr(127));
        #Backward 1
        #roboclaw.write(chr(1));
        #Forward 2
        #roboclaw.write(chr(255));
        #Backward 2
        #roboclaw.write(chr(128));
        #GPIO.output(24, GPIO.LOW)
        sleep(0.001)
        GPIO.output(24, GPIO.LOW)
        sleep(1)
        
        stop()
        sleep(2)
        
    GPIO.cleanup()