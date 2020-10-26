from motorcontroller import *
import pygame
pygame.init()


win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Mecanum controller")

x = 50
y = 50
width = 40
height = 60
vel = 5*2

drive_time = 0.2
drive_speed = 'LOW'

run = True
motor_controller = MotorController()
while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    
    move = False
    
    
    if (keys[pygame.K_w] and keys[pygame.K_d])   or (keys[pygame.K_UP] and keys[pygame.K_RIGHT]):
        print('wd')
        move = True; y -= vel; x += vel
        motor_controller.wddiagonal(drivetime = drive_time, inputspeed = drive_speed)
    elif (keys[pygame.K_w] and keys[pygame.K_a]) or (keys[pygame.K_UP] and keys[pygame.K_LEFT]):
        print('wa')
        move = True; y -= vel; x -= vel
        motor_controller.wadiagonal(drivetime = drive_time, inputspeed = drive_speed)
    elif (keys[pygame.K_s] and keys[pygame.K_d]) or (keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]):
        print('sd')
        move = True; y += vel; x = vel
        motor_controller.sddiagonal(drivetime = drive_time, inputspeed = drive_speed)
    elif (keys[pygame.K_s] and keys[pygame.K_a]) or (keys[pygame.K_DOWN] and keys[pygame.K_LEFT]):
        print('sa')
        move = True; y += vel; x -= vel
        motor_controller.sadiagonal(drivetime = drive_time, inputspeed = drive_speed)
    
    # Change motorspeed of the robot.
    if keys[pygame.K_t]:
        speed_premap = int(input("set speed from 0 to 100: "))
        if not type(speed_premap) is int:
            raise TypeError("Please only use integers for speed setting ")
        elif (speed_premap < 0) or (speed_premap > 100):
            raise ValueError("Speedrange is from 0 to 100: ")
        motor_controller.speed_change(speed_premap)
        
        """ if drive_speed == 'LOW':
            drive_speed = 'HIGH'
            print('Drive speed is now HIGH')
        elif drive_speed == 'HIGH':
            drive_speed = 'LOW'
            print('Drive speed is now LOW')       
        """
        
    if event.type == pygame.KEYDOWN and move != True:
        if event.key == pygame.K_UP or event.key == ord('w'):
            print('up')
            move = True
            y -= vel
            motor_controller.forward(drivetime = drive_time, inputspeed = drive_speed)
        elif event.key == pygame.K_DOWN or event.key == ord('s'):
            print('down')
            move = True
            y += vel
            motor_controller.backward(drivetime = drive_time, inputspeed = drive_speed)
        elif event.key == pygame.K_LEFT or event.key == ord('a'):
            print('left')
            move = True
            x -= vel
            motor_controller.left(drivetime = drive_time, inputspeed = drive_speed)
        elif event.key == pygame.K_RIGHT or event.key == ord('d'):
            print('right')
            move = True
            x += vel
            motor_controller.right(drivetime = drive_time, inputspeed = drive_speed)
        elif event.key == ord('q'):
            print('counterclockwise')
            move = True
            motor_controller.rotate(direction = 'COUNTER_CLOCKWISE',drivetime = drive_time, inputspeed = drive_speed)
        elif event.key == ord('e'):
            print('clockwise')
            move = True
            motor_controller.rotate(direction = 'CLOCKWISE',drivetime = drive_time, inputspeed = drive_speed)
    
    if move == False:
        motor_controller.stop()
    else:
        pass
        
    
    win.fill((0,0,0))  # Fills the screen with black
    pygame.draw.rect(win, (255,0,0), (x, y, width, height))   
    pygame.display.update() 
    
pygame.quit()