#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main interface for controlling the Mecanum-Robot model.
This script runs a method 'rungame' which takes in a Queue
and Event. These args are necessary when driving threadPool-
executors, due to the necessity of knowing which thread goes where.

Reference:
    https://realpython.com/documenting-python-code/
"""

# Importing packages
import logging
import queue
import threading
import pygame
from threading import Event
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from typing import NoReturn
from pygame.constants import RESIZABLE

# Importing utils
from utils.server import Server


def rungame(queue: Queue, events: Event) -> NoReturn:
    """[summary]
    This method is the soul and main controller of the project.
    Within this method, you create a GUI 'game' where you 
    interact with the robot once the robot is connected.
    You also gain vision through connection of said robot.

    Args:
        queue ([type]): [description]
        events ([type]): [description]
    """
    while not events.is_set():

        x: int = 50
        y: int = 50
        vel: int = 5*2
        width: int = 40
        height: int = 60
        drive_time: int = 0.2
        stick_L: tuple = (0, 0)
        resolution: tuple = (640, 480)
        run: bool = True
        move: bool = False
        stopped: bool = False
        connected: bool = False
        drive_speed: str = 'LOW'

        screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
        pygame.display.set_caption("brom brom")
        pygame.init()
        pygame.joystick.init()
        clock = pygame.time.Clock()

        while run:
            # -----------------------------------------------
            # ---------Check if connection is active---------
            connected = server.isconnected()

            # pygame.time.delay(50)

            # Get the current events happening on screen
            # and treat each individual input as designed
            currentevents = pygame.event.get()
            for event in currentevents:
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.VIDEORESIZE:
                    resolution = (event.w, event.h)
                    screen = pygame.display.set_mode(
                        resolution, pygame.RESIZABLE)

            # Check for any joystick inputs
            joystick_count = pygame.joystick.get_count()
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                # buttons = joystick.get_button()
                stick_L = (joystick.get_axis(0), joystick.get_axis(1))

            # Fetch the current keys registered
            keys = pygame.key.get_pressed()

            # Set move to false because we have not moved yet.
            move = False

            # # Change motor speed to high or low.
            # if keys[pygame.K_t]:
            #     if drive_speed == 'LOW':
            #         drive_speed = 'HIGH'
            #         logging.debug('Drive speed is now HIGH')
            #     elif drive_speed == 'HIGH':
            #         drive_speed = 'LOW'
            #         logging.debug('Drive speed is now LOW')

            # Check both arrow and wasd keys for flags.
            # If no flags on them, check joystick.
            # If connected, send cmd to client.
            # Flag for going northeast
            if ((keys[pygame.K_w] and keys[pygame.K_d]) or (
                keys[pygame.K_UP] and keys[pygame.K_RIGHT]) or
                    stick_L[0] > 0.3 and stick_L[1] < -0.3):
                logging.debug('wd')
                move = True
                stopped = False
                y -= vel
                x += vel
                if connected:
                    server.send('wd')
            # Flag for going northwest
            elif ((keys[pygame.K_w] and keys[pygame.K_a]) or (
                    keys[pygame.K_UP] and keys[pygame.K_LEFT]) or
                    stick_L[0] < -0.3 and stick_L[1] < -0.3):
                logging.debug('wa')
                move = True
                stopped = False
                y -= vel
                x -= vel
                if connected:
                    server.send('wa')
            # Flag for going southeast
            elif ((keys[pygame.K_s] and keys[pygame.K_d]) or (
                    keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]) or
                    stick_L[0] > 0.3 and stick_L[1] > 0.3):
                logging.debug('sd')
                move = True
                stopped = False
                x += vel
                if connected:
                    server.send('sd')
            # Flag for going southwest
            elif ((keys[pygame.K_s] and keys[pygame.K_a]) or (
                    keys[pygame.K_DOWN] and keys[pygame.K_LEFT]) or
                    stick_L[0] < -0.3 and stick_L[1] > 0.3):
                logging.debug('sa')
                move = True
                stopped = False
                y += vel
                x -= vel
                if connected:
                    server.send('sa')
            # Flag for going forward/north
            elif (keys[pygame.K_w] or keys[pygame.K_UP] or
                  stick_L[1] < -0.3):
                logging.debug('up')
                move = True
                stopped = False
                y -= vel
                if connected:
                    server.send('w')
            # Flag for going south/down
            elif (keys[pygame.K_s] or keys[pygame.K_DOWN] or
                  stick_L[1] > 0.3):
                logging.debug('down')
                move = True
                stopped = False
                y += vel
                if connected:
                    server.send('s')
            # Flag for going left/west
            elif (keys[pygame.K_a] or keys[pygame.K_LEFT] or
                  stick_L[0] < - 0.3):
                logging.debug('left')
                move = True
                stopped = False
                x -= vel
                if connected:
                    server.send('a')
            # Flag for going right/east
            elif (keys[pygame.K_d] or keys[pygame.K_RIGHT] or
                  stick_L[0] > 0.3):
                logging.debug('right')
                move = True
                stopped = False
                x += vel
                if connected:
                    server.send('d')
            # Flag for rotating counterclockwise
            elif keys[pygame.K_q]:
                logging.debug('counterclockwise')
                move = True
                stopped = False
                if connected:
                    server.send('q')
            # Flag for rotating clockwise
            elif keys[pygame.K_e]:
                logging.debug('clockwise')
                move = True
                stopped = False
                if connected:
                    server.send('e')

            # Check move and stop for flags
            # If none are true, no new inputs are detected and
            # thus we stop the robot
            if move == False and stopped == False:
                logging.debug('stop')
                if connected:
                    server.send('stop')
                stopped = True
            else:
                pass

            # If connected, fill the background with the videostream
            # If not, just fill it with black
            if connected:
                frame = server.get_frame(resolution)
                screen.blit(frame, (0, 0))
            else:
                screen.fill('black')

            # Using a little red rectangle for movement visualisation
            pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))
            # Update the screen and set framerate
            pygame.display.update()
            clock.tick(15)

        # Send warningflags to stop the server and client.
        # After this has been done, close the game properly.
        logging.debug("Closing server...")
        server.send("!DISCONNECT")
        # TODO: Perhaps add a wait here to ensure server sends disconnect?
        # server.close()
        logging.debug("Closing game...")
        pygame.quit()
        break


# ---------- MAIN LOOP ----------
if __name__ == '__main__':
    # Set basic logging configuration.
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)

    # Initialize the server object.
    server = Server()

    # Set up the threading environment with threadPoolExecutor.
    pipeline = queue.Queue(maxsize=5)
    event = threading.Event()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(rungame, pipeline, event)
        executor.submit(server.start, pipeline, event)
