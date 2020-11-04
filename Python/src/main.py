#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""[summary]
Main interface for controlling the Mecanum-Robot model.
- - S C R I P T  D O C S T R I N G  W I P - -
Reference:
    https://realpython.com/documenting-python-code/
"""

# Importing packages
import logging
import queue
import threading
import pygame
import numpy
import cv2
from threading import Event
from queue import Queue
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from typing import NoReturn

from pygame.constants import RESIZABLE

# Importing utils
from utils.server import Server


def rungame(queue: Queue, events: Event) -> NoReturn:
    """[summary]
    Start and run the PYGAME screendow.
    
    Args:
        queue ([type]): [description]
        events ([type]): [description]
    """
    while not events.is_set():
        

        x = 50
        y = 50
        width = 40
        height = 60
        vel = 5*2
        drive_time = 0.2
        resolution = (640,480)
        stick = None
        stick_L = (0,0)
        buttons = None
        drive_speed = 'LOW'
        connected = False
        stopped = False
        run = True
        screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
        pygame.display.set_caption("brom brom")
        pygame.init()
        pygame.joystick.init()
        clock = pygame.time.Clock()
        
        
        while run:
            connected = server.isconnected()

            # pygame.time.delay(50)

            currentevents = pygame.event.get()

            for event in currentevents:
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.VIDEORESIZE:
                    resolution = (event.w, event.h)
                    screen = pygame.display.set_mode(resolution,pygame.RESIZABLE)
            
            joystick_count = pygame.joystick.get_count()

            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                buttons = stick.get_buttons()
                stick_L = (stick.get_axis(0), stick.get_axis(1))

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

            if ((keys[pygame.K_w] and keys[pygame.K_d]) or (
                keys[pygame.K_UP] and keys[pygame.K_RIGHT]) or 
                stick_L[0] > 0.3 and stick_L[1] < -0.3):
                logging.debug('wd')
                move = True;stopped = False
                y -= vel;x += vel
                if connected:
                    server.send('wd')
            elif ((keys[pygame.K_w] and keys[pygame.K_a]) or (
                keys[pygame.K_UP] and keys[pygame.K_LEFT]) or
                stick_L[0] < -0.3 and stick_L[1] < -0.3):
                logging.debug('wa')
                move = True;stopped = False
                y -= vel;x -= vel
                if connected:
                    server.send('wa')
            elif ((keys[pygame.K_s] and keys[pygame.K_d]) or (
                keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]) or 
                stick_L[0] > 0.3 and stick_L[1] > 0.3):
                logging.debug('sd')
                move = True;stopped = False
                x += vel
                if connected:
                    server.send('sd')
            elif ((keys[pygame.K_s] and keys[pygame.K_a]) or (
                keys[pygame.K_DOWN] and keys[pygame.K_LEFT]) or 
                stick_L[0] < -0.3 and stick_L[1] > 0.3):
                logging.debug('sa')
                move = True;stopped = False
                y += vel;x -= vel
                if connected:
                    server.send('sa')
            elif keys[pygame.K_w] or keys[pygame.K_UP] or stick_L[1] < -0.3:
                logging.debug('up')
                move = True;stopped = False
                y -= vel
                if connected:
                    server.send('w')
            elif keys[pygame.K_s] or keys[pygame.K_DOWN] or stick_L[1] > 0.3:
                logging.debug('down')
                move = True;stopped = False
                y += vel
                if connected:
                    server.send('s')
            elif keys[pygame.K_a] or keys[pygame.K_LEFT] or stick_L[0] <- 0.3:
                logging.debug('left')
                move = True;stopped = False
                x -= vel
                if connected:
                    server.send('a')
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT] or stick_L[0] > 0.3:
                logging.debug('right')
                move = True;stopped = False
                x += vel
                if connected:
                    server.send('d')
            elif keys[pygame.K_q] or (buttons == 4):
                logging.debug('counterclockwise')
                move = True;stopped = False
                if connected:
                    server.send('q')
            elif keys[pygame.K_e] or (buttons == 5):
                logging.debug('clockwise')
                move = True;stopped = False
                if connected:
                    server.send('e')

            if move == False and stopped == False: 
                # mc.stop()
                logging.debug('stop')
                if connected:
                    # logging.debug('stop')
                    server.send('stop')
                    server.send('stop') 
                stopped = True
            else:
                pass
            
            if connected:
                frame = server.get_frame(resolution)
                screen.blit(frame, (0, 0))
            else:
                screen.fill('black')            
            # screen.fill('black')  # Fills the screen with black
            pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))
            pygame.display.update()
            clock.tick(15)

        logging.debug("Closing server...")
        server.send("!DISCONNECT")
        # TODO: Perhaps add a wait here to ensure server sends disconnect?
        # server.close()
        logging.debug("Closing game...")
        pygame.quit()
        break


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)

    server = Server()

    pipeline = queue.Queue(maxsize=5)
    event = threading.Event()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(rungame, pipeline, event)
        executor.submit(server.start, pipeline, event)