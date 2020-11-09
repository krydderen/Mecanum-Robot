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
import pygame_gui

# Importing utils
from utils.server import Server

class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y) 
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+20), t_surf.get_height()+10), pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        if self.active:
            self.image.blit(t_surf, (5, 5))
            pygame.draw.rect(self.image, self.color, self.image.get_rect(),2)
            self.rect = self.image.get_rect(topleft = self.pos)
        else:
            pass
        

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
    drive_time: int = 0.2
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
    


    screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
    pygame.display.set_caption("brom brom")
    pygame.init()
    pygame.joystick.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 50)
    text_input_box = TextInputBox(10, 10, 50, font)
    group = pygame.sprite.Group(text_input_box)
    
    text = font.render(f'SPEED: {speed}', True, (255, 255, 255), None)
    textRect = text.get_rect()
    
    arrow = pygame.image.load('red_arrow.png')


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
                            speed = int(text_input_box.text)
                            text = font.render(f'SPEED: {speed}', True, (255, 255, 255), None)
                            if connected:
                                server.send(['speed', speed])
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
            buttons = [] 
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            stick_L = (joystick.get_axis(0), joystick.get_axis(1))
            buttons.insert(0,joystick.get_button(2))
            buttons.insert(1,joystick.get_button(3))
            buttons.insert(2,joystick.get_button(4))
            buttons.insert(3,joystick.get_button(5))
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
                stick_L[0] > deadzone and stick_L[1] < -deadzone):
            move = True
            stopped = False
            y -= vel
            x += vel
            tosend = 'wd'
        # Flag for going northwest
        elif ((keys[pygame.K_w] and keys[pygame.K_a]) or (
                keys[pygame.K_UP] and keys[pygame.K_LEFT]) or
                stick_L[0] < -deadzone and stick_L[1] < -deadzone):
            move = True
            stopped = False
            y -= vel
            x -= vel
            tosend = 'wa'
        # Flag for going southeast
        elif ((keys[pygame.K_s] and keys[pygame.K_d]) or (
                keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]) or
                stick_L[0] > deadzone and stick_L[1] > deadzone):
            move = True
            stopped = False
            y += vel
            x += vel
            tosend = 'sd'
        # Flag for going southwest
        elif ((keys[pygame.K_s] and keys[pygame.K_a]) or (
                keys[pygame.K_DOWN] and keys[pygame.K_LEFT]) or
                stick_L[0] < -deadzone and stick_L[1] > deadzone):
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
        elif keys[pygame.K_q] or button1:
            move = True
            stopped = False
            tosend = 'q'
        # Flag for rotating clockwise
        elif keys[pygame.K_e] or button2:
            move = True
            stopped = False
            tosend = 'e'
        else:
            move = False
                
        # Speedselection using controller
        if buttons[0] and buttons[1]:
            logging.debug('+1 -1 speed')
        elif buttons[1]:
            speed -= 1
            if speed <= 0:
                speed = 100
        elif buttons[0]:
            speed += 1
            if speed >= 100:
                speed = 100
                        
        if connected and (pygame.joystick.get_count > 0):
            msg = ['speed', speed]
            server.send(msg)

        # Check move and stop for flags
        # If none are true, no new inputs are detected and
        # thus we stop the robot
        if move == False and stopped == False and connected:
            if connected:
                server.send('stop')
            stopped = True
            lastsent = 'stop'
            logging.debug(lastsent)
        elif move == True and connected and lastsent != tosend:
            server.send(tosend)
            lastsent = tosend
            logging.debug(lastsent)

        # If connected, fill the background with the videostream
        # If not, just fill it with black
        frame = server.get_frame(resolution)
        if connected and frame != None:
            screen.blit(frame, (0, 0))
        else:
            screen.fill('black')

        # Using a little red rectangle for movement visualisation
        pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))
        if text_input_box.active:
            group.draw(screen)
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

    # Set up the threading environment with threadPoolExecutor.
    pipeline = queue.Queue(maxsize=5)
    event = threading.Event()
    
    thread1 = threading.Thread(target=rungame, args=(queue, event))
    thread2 = threading.Thread(target=server.start, args=(queue, event))
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
