# Importing packages
import logging
import pygame
from roboclaw_3 import Roboclaw
from time import sleep

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("brom brom")

rc = Roboclaw("/dev/ttyS0", 38400)
addresses = [0x80, 0x81]
sleep(0.2)
speed = 64
rc.Open()

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
x = 50
y = 50
width = 40
height = 60
vel = 5*2
drive_time = 0.2
drive_speed = 'LOW'
stopped = True
run = True
pygame.init()
while run:
    # if server.isconnected():
    #     connected = True

    pygame.time.delay(50)

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
        stopped = False
        y -= vel
        x += vel
        rc.ForwardM2(0x80, 64)
        rc.ForwardM2(0x81, 64)
        # mc.wddiagonal(drivetime = drive_time, inputspeed = drive_speed)
    elif (keys[pygame.K_w] and keys[pygame.K_a]) or (keys[pygame.K_UP] and keys[pygame.K_LEFT]):
        logging.debug('wa')
        move = True
        stopped = False
        y -= vel
        x -= vel
        rc.ForwardM1(0x80, 64)
        rc.ForwardM1(0x81, 64)
        # mc.wadiagonal(drivetime = drive_time, inputspeed = drive_speed)
    elif (keys[pygame.K_s] and keys[pygame.K_d]) or (keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]):
        logging.debug('sd')
        move = True
        stopped = False
        y += vel
        x += vel
        rc.BackwardM1(0x80, 64)
        rc.BackwardM1(0x81, 64)
        # mc.sddiagonal(drivetime = drive_time, inputspeed = drive_speed)
    elif (keys[pygame.K_s] and keys[pygame.K_a]) or (keys[pygame.K_DOWN] and keys[pygame.K_LEFT]):
        logging.debug('sa')
        move = True
        stopped = False
        y += vel
        x -= vel
        rc.BackwardM2(0x80, 64)
        rc.BackwardM2(0x81, 64)
        # mc.sadiagonal(drivetime = drive_time, inputspeed = drive_speed)
    elif keys[pygame.K_w] or keys[pygame.K_UP]:
        logging.debug('up')
        move = True
        stopped = False
        y -= vel
        rc.ForwardM1(0x80, 64)
        rc.ForwardM1(0x81, 64)
        rc.ForwardM2(0x80, 64)
        rc.ForwardM2(0x81, 64)
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        logging.debug('down')
        move = True
        stopped = False
        y += vel
        rc.BackwardM1(0x80, 64)
        rc.BackwardM1(0x81, 64)
        rc.BackwardM2(0x80, 64)
        rc.BackwardM2(0x81, 64)
        # mc.backward(drivetime = drive_time, inputspeed = drive_speed)
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        logging.debug('left')
        move = True
        stopped = False
        x -= vel
        rc.BackwardM2(0x80, 64)
        rc.ForwardM1(0x80, 64)
        rc.ForwardM1(0x81, 64)
        rc.BackwardM2(0x81, 64)
        # mc.left(drivetime = drive_time, inputspeed = drive_speed)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        logging.debug('right')
        move = True
        stopped = False
        x += vel
        rc.BackwardM1(0x80, 64)
        rc.ForwardM2(0x80, 64)
        rc.ForwardM2(0x81, 64)
        rc.BackwardM1(0x81, 64)
        # mc.right(drivetime = drive_time, inputspeed = drive_speed)
    elif keys[pygame.K_q]:
        logging.debug('counterclockwise')
        move = True
        stopped = False
        rc.BackwardM2(0x80, 64)
        rc.ForwardM1(0x80, 64)
        rc.ForwardM2(0x81, 64)
        rc.BackwardM1(0x81, 64)
        # mc.rotate(direction = 'COUNTER_CLOCKWISE',drivetime = drive_time,
        #   inputspeed = drive_speed)
    elif keys[pygame.K_e]:
        logging.debug('clockwise')
        move = True
        stopped = False
        rc.BackwardM1(0x80, 64)
        rc.ForwardM2(0x80, 64)
        rc.ForwardM1(0x81, 64)
        rc.BackwardM2(0x81, 64)
        # mc.rotate(direction = 'CLOCKWISE',drivetime = drive_time,
        #   inputspeed = drive_speed)

    if move == False and stopped == False:
        # mc.stop()
        logging.debug('stop')
        rc.ForwardM1(0x80, 0)
        rc.ForwardM2(0x80, 0)
        rc.BackwardM1(0x80, 0)
        rc.BackwardM2(0x80, 0)
        rc.ForwardM1(0x81, 0)
        rc.ForwardM2(0x81, 0)
        rc.BackwardM1(0x81, 0)
        rc.BackwardM2(0x81, 0)
        stopped = True

    else:
        pass

    win.fill((0, 0, 0))  # Fills the screen with black
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()

logging.debug("Closing game...")
pygame.quit()
