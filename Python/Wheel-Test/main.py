# Importing packages
import logging
import pygame
from roboclaw_3 import Roboclaw
from time import sleep

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("brom brom")

rc = Roboclaw("/dev/ttyS0", 38400)
addresses = [0x80,0x81]
sleep(0.2)
speed = 64
rc.Open()

logging.basicConfig(format='%(asctime)s - %(message)s',level=logging.DEBUG)
x = 50
y = 50
width = 40
height = 60
vel = 5*2
drive_time = 0.2
drive_speed = 'LOW'
stopped = False
run = True
pygame.init()
while run:
    # if server.isconnected():
    #     connected = True

    pygame.time.delay(100)

    currentevents = pygame.event.get()

    for event in currentevents:
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    move = False

    # # Change motor speed to high or low.
    # if keys[pygame.K_t]:
    #     if drive_speed == 'LOW':
    #         drive_speed = 'HIGH'
    #         logging.debug('Drive speed is now HIGH')
    #     elif drive_speed == 'HIGH':
    #         drive_speed = 'LOW'
    #         logging.debug('Drive speed is now LOW')

    if (keys[pygame.K_w] and keys[pygame.K_d]) or (keys[pygame.K_UP] and keys[pygame.K_RIGHT]):
        logging.debug('wd')
        move = True
        y -= vel
        x += vel
        # mc.wddiagonal(drivetime = drive_time, inputspeed = drive_speed)
    elif (keys[pygame.K_w] and keys[pygame.K_a]) or (keys[pygame.K_UP] and keys[pygame.K_LEFT]):
        logging.debug('wa')
        move = True
        y -= vel
        x -= vel
        # mc.wadiagonal(drivetime = drive_time, inputspeed = drive_speed)
    elif (keys[pygame.K_s] and keys[pygame.K_d]) or (keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]):
        logging.debug('sd')
        move = True
        y += vel
        x += vel
        # mc.sddiagonal(drivetime = drive_time, inputspeed = drive_speed)
    elif (keys[pygame.K_s] and keys[pygame.K_a]) or (keys[pygame.K_DOWN] and keys[pygame.K_LEFT]):
        logging.debug('sa')
        move = True
        y += vel
        x -= vel
        # mc.sadiagonal(drivetime = drive_time, inputspeed = drive_speed)
    elif keys[pygame.K_w] or keys[pygame.K_UP]:
        logging.debug('up')
        move = True
        y -= vel
        rc.ForwardMixed(0x80, 64)
        rc.ForwardMixed(0x81, 64)
        # mc.forward(drivetime = drive_time, inputspeed = drive_speed)
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        logging.debug('down')
        move = True
        y += vel
        rc.BackwardMixed(0x80, 64)
        rc.BackwardMixed(0x81, 64)
        # mc.backward(drivetime = drive_time, inputspeed = drive_speed)
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        logging.debug('left')
        move = True
        x -= vel
        # mc.left(drivetime = drive_time, inputspeed = drive_speed)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        logging.debug('right')
        move = True
        x += vel
        # mc.right(drivetime = drive_time, inputspeed = drive_speed)
    elif keys[pygame.K_q]:
        logging.debug('counterclockwise')
        move = True
        # mc.rotate(direction = 'COUNTER_CLOCKWISE',drivetime = drive_time,
                #   inputspeed = drive_speed)
    elif keys[pygame.K_e]:
        logging.debug('clockwise')
        move = True
        # mc.rotate(direction = 'CLOCKWISE',drivetime = drive_time,
                #   inputspeed = drive_speed)

    if move == False and stopped == False: 
        #mc.stop()
        for address in addresses:
            rc.ForwardMixed(address, 0)
            rc.BackwardMixed(address,0)
            rc.TurnRightMixed(address,0)
            rc.TurnLeftMixed(address,0)
            rc.ForwardM1(address,0)
            rc.TorwardM2(address,0)
            rc.BackwardM1(address,0)
            rc.BackwardM2(address,0)
        stopped = True
        
    else:
        pass

    win.fill((0, 0, 0))  # Fills the screen with black
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()

logging.debug("Closing game...")
pygame.quit()
