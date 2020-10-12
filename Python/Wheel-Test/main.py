from motorcontroller import *
import pygame
pygame.init()


win = pygame.display.set_mode((500,500))
pygame.display.set_caption("First Game")

x = 50
y = 50
width = 40
height = 60
vel = 5*2

drive_time = 0.2

run = True
motor_controller = MotorController()
while run:
    pygame.time.delay(25)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        x -= vel
        print('left')
        motor_controller.left(drivetime = drive_time, inputspeed = 'LOW')
    elif keys[pygame.K_RIGHT]:
        x += vel
        print('right')
        motor_controller.right(drivetime = drive_time, inputspeed = 'LOW')
    elif keys[pygame.K_UP]:
        y -= vel
        print('up')
        motor_controller.forward(drivetime = drive_time, inputspeed = 'LOW')
    elif keys[pygame.K_DOWN]:
        y += vel
        print('down')
        motor_controller.backward(drivetime = drive_time, inputspeed = 'LOW')
    else:
        motor_controller.stop()
        
    win.fill((0,0,0))  # Fills the screen with black
    pygame.draw.rect(win, (255,0,0), (x, y, width, height))   
    pygame.display.update() 
    
pygame.quit()