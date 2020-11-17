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
from typing import NoReturn
from pygame.constants import RESIZABLE
import os
import cv2

# Importing utils
from utils.server import Server
from utils.textinputbox import TextInputBox
from utils.obstacledetection import ObstacleDetection


def rungame(queue: Queue, event: Event) -> None:
    """[summary]
    This method is the soul and main controller of the project.
    Within this method, you create a GUI 'game' where you 
    interact with the robot once the robot is connected.
    You also gain vision through connection of said robot.

    Args:
        queue ([type]): [description]
        events ([type]): [description]
    """
    # while not event.is_set():

    x: int = 50
    y: int = 50
    vel: int = 5*2
    width: int = 40
    height: int = 60
    speed: int = 100
    diagsens: int = 0.3
    newspeed: int = 0
    drive_time: int = 0.2
    currentspeed: int = 0
    deadzone : float = 0.5
    stick_L: tuple = (0, 0)
    resolution: tuple = (640, 480)
    run: bool = True
    move: bool = False
    speed: int = 0
    stopped: bool = False
    connected: bool = False
    tosend: str = ''
    lastsent:str = ''
    
    if os.path.exists(r"python\src\utils\img"):
        # Change the current working Directory - Kev
        os.chdir(r"python\src\utils\img")
    elif os.path.exists(r'\mecanum\Mecanum-Robot'):
        # Change the current working Directory - Rub
        os.chdir(r'\mecanum\Mecanum-Robot')
    else:
        print("Can't change the Current Working Directory")

    screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
    pygame.display.set_caption("brom brom")
    pygame.init()
    pygame.joystick.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 50)
    text_input_box = TextInputBox(10, 10, 50, font)
    group = pygame.sprite.Group(text_input_box)
    direction_pos = (25, resolution[1]-25)
    arrow = pygame.transform.smoothscale(pygame.image.load('red_arrow.png'), (50,50))
    box = pygame.transform.smoothscale(pygame.image.load('red_square.png'), (50,50))
    rotating_arrows = pygame.transform.smoothscale(pygame.image.load('rotate_arrow.png'), (50,50))
    directionfigure = box
    
    text = font.render(f'SPEED: 100', True, (255, 255, 255), None)
    textRect = text.get_rect()

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not text_input_box.active:
                    text_input_box.active = 1
                if event.type == pygame.KEYDOWN and text_input_box.active:
                    if event.key == pygame.K_RETURN:
                        text_input_box.active = False
                        print(f"final text {text_input_box.text}")
                        try:
                            newspeed = int(text_input_box.text)
                            text = font.render(f'SPEED: {newspeed}', True, (255, 255, 255), None)
                            if connected and currentspeed != newspeed:
                                server.send(['speed', newspeed])
                                currentspeed = newspeed
                        except:
                            pass
                        text_input_box.text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text_input_box.text = text_input_box.text[:-1]
                    else:
                        text_input_box.text += event.unicode
                        # print(text_input_box.text)
                    text_input_box.render_text()
                
        # Check for any joystick inputs
        try:
            buttons = [None] * 4
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            stick_L = (joystick.get_axis(0), joystick.get_axis(1))
            buttons.insert(0,joystick.get_button(2))
            buttons.insert(1,joystick.get_button(3))
            buttons.insert(2,joystick.get_button(4))
            buttons.insert(3,joystick.get_button(5))
            buttons.insert(4,joystick.get_button(0))
            buttons.insert(5,joystick.get_button(1))
        except:
            pass

        # Fetch the current keys registered
        keys = pygame.key.get_pressed()

        # Check both arrow and wasd keys for flags.
        # If no flags on them, check joystick.
        # If connected, send cmd to client.
        
        # Flag for going northeast
        if ((keys[pygame.K_w] and keys[pygame.K_d]) or (
            keys[pygame.K_UP] and keys[pygame.K_RIGHT]) or
                stick_L[0] > diagsens and stick_L[1] < -diagsens):
            move = True
            stopped = False
            y -= vel
            x += vel
            tosend = 'wd'
        # Flag for going northwest
        elif ((keys[pygame.K_w] and keys[pygame.K_a]) or (
                keys[pygame.K_UP] and keys[pygame.K_LEFT]) or
                stick_L[0] < -diagsens and stick_L[1] < -diagsens):
            move = True
            stopped = False
            y -= vel
            x -= vel
            tosend = 'wa'
        # Flag for going southeast
        elif ((keys[pygame.K_s] and keys[pygame.K_d]) or (
                keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]) or
                stick_L[0] > diagsens and stick_L[1] > diagsens):
            move = True
            stopped = False
            y += vel
            x += vel
            tosend = 'sd'
        # Flag for going southwest
        elif ((keys[pygame.K_s] and keys[pygame.K_a]) or (
                keys[pygame.K_DOWN] and keys[pygame.K_LEFT]) or
                stick_L[0] < -diagsens and stick_L[1] > diagsens):
            move = True
            stopped = False
            y += vel
            x -= vel
            tosend = 'sa'
        # Flag for going forward/north
        elif (keys[pygame.K_w] or keys[pygame.K_UP] or
                stick_L[1] < -deadzone):
            move = True
            stopped = False
            y -= vel
            tosend = 'w'
        # Flag for going south/down
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN] or
                stick_L[1] > deadzone):
            move = True
            stopped = False
            y += vel
            tosend = 's'
        # Flag for going left/west
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT] or
                stick_L[0] < - deadzone):
            move = True
            stopped = False
            x -= vel
            tosend = 'a'
        # Flag for going right/east
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT] or
                stick_L[0] > deadzone):
            move = True
            stopped = False
            x += vel
            tosend = 'd'
        # Flag for rotating counterclockwise
        elif keys[pygame.K_q] or buttons[2]:
            move = True
            stopped = False
            tosend = 'q'
        # Flag for rotating clockwise
        elif keys[pygame.K_e] or buttons[3]:
            move = True
            stopped = False
            tosend = 'e'
        else:
            move = False
                
        # Speedselection using controller
        if buttons[0] and buttons[1]:
            logging.debug('+1 -1 speed')
        elif buttons[0]:
            if newspeed == 69:
                newspeed = 70
            newspeed -= 5
            if newspeed <= 0:
                newspeed = 0
            text = font.render(f'SPEED: {newspeed}', True, (255, 255, 255), None)
        elif buttons[1]:
            if newspeed == 69:
                newspeed = 70
            newspeed += 5
            if newspeed >= 100:
                newspeed = 100
            text = font.render(f'SPEED: {newspeed}', True, (255, 255, 255), None)
        elif buttons[4]:
            #A
            pass
        elif buttons[5]:
            #B
            newspeed = 69
            text = font.render(f'sped69:lmao', True, (255, 255, 255), None)
        
        
                        
        if connected and (pygame.joystick.get_count != 0) and currentspeed != newspeed:
            msg = ['speed', newspeed]
            server.send(msg)
            currentspeed = newspeed
            
        if tosend == 'w' and lastsent != tosend:
            directionfigure = (pygame.transform.rotate(arrow, 90))
        elif tosend == 'a' and lastsent != tosend:
            directionfigure = (pygame.transform.rotate(arrow, 180))
        elif tosend == 's' and lastsent != tosend:
            directionfigure = (pygame.transform.rotate(arrow, 270))
        elif tosend == 'd' and lastsent != tosend:
            directionfigure = (pygame.transform.rotate(arrow, 0))
        elif tosend == 'wd' and lastsent != tosend:
            directionfigure = (pygame.transform.rotate(arrow, 45)) 
        elif tosend == 'wa' and lastsent != tosend:
            directionfigure = (pygame.transform.rotate(arrow, 135))
        elif tosend == 'sa' and lastsent != tosend:
            directionfigure = (pygame.transform.rotate(arrow, 225))
        elif tosend == 'sd' and lastsent != tosend:
            directionfigure = (pygame.transform.rotate(arrow, 315))
        elif tosend == 'q' and lastsent != tosend:
            directionfigure = rotating_arrows
        elif tosend == 'e' and lastsent != tosend:
            directionfigure = (pygame.transform.flip(rotating_arrows, True, False))
        elif tosend == 'stop' and lastsent != tosend:
            directionfigure = box
        
        dir_rect = directionfigure.get_rect()
        dir_rect.center = direction_pos

        # Check move and stop for flags
        # If none are true, no new inputs are detected and
        # thus we stop the robot
        if move == False and stopped == False and connected:
            tosend = 'stop'
            if connected:
                server.send(tosend)
            stopped = True
            lastsent = 'stop'
            logging.debug(lastsent)
            directionfigure = box
            #arrow = screen.set_alpha(0) ## needs fix
        elif move == True and connected and lastsent != tosend:
            server.send(tosend)
            lastsent = tosend
            logging.debug(lastsent)
        elif move == False  and stopped == False:
            directionfigure = box
            tosend = 'stop'
            stopped = True
            lastsent = tosend
            logging.debug(lastsent)
            print('yo mom a hoho')
        elif move == True and lastsent != tosend:
            lastsent = tosend
            logging.debug(lastsent)
            

        # If connected, fill the background with the videostream
        # If not, just fill it with black
        frame = server.get_frame(resolution)
        canny = server.get_canny()
        if connected: 
            # try:
                # cv2.imshow("canny", canny)
            # except:
            #     pass
            obsdet.set_canny(canny)
        
        if connected and frame != None:
            screen.blit(frame, (0, 0))
        else:
            screen.fill('black')

        # Using a little red rectangle for movement visualisation
        #pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))
        if text_input_box.active:
            group.draw(screen)

        screen.blit(directionfigure, dir_rect)
        # Update the screen and set framerate
        
        textRect.bottomright = (resolution[0]-10, resolution[1]-10)
        screen.blit(text,textRect)
        pygame.display.update()

        
        clock.tick(15)
        

    # Send warningflags to stop the server and client.
    # After this has been done, close the game properly.
    logging.debug("Closing server...")
    # TODO: Perhaps add a wait here to ensure server sends disconnect?
    # server.close()
    logging.debug("Closing game...")
    pygame.quit()


# ---------- MAIN LOOP ----------
if __name__ == '__main__':
    # Set basic logging configuration.
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.DEBUG)

    # Initialize the server object.
    server = Server()
    obsdet = ObstacleDetection()
    # Set up the threading environment with threadPoolExecutor.
    pipeline = queue.Queue(maxsize=5)
    event = threading.Event()
    
    thread1 = threading.Thread(target=rungame, args=(queue, event))
    thread2 = threading.Thread(target=server.start, args=(queue, event))
    # thread3 = threading.Thread(target=obsdet.start, args=(queue, event))
    
    thread1.start()
    thread2.start()
    # thread3.start()
    
    thread1.join()
    thread2.join()
    # thread3.join()
    