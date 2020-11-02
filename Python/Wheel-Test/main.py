from motorcontroller import MotorController
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
drive_speed = 'LOW'

run = True
motor_controller = MotorController()
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    
    move = False

    if (keys[pygame.K_w] and keys[pygame.K_d])   or (keys[pygame.K_UP] and keys[pygame.K_RIGHT]):
        print('wd')
        move = True; y -= vel; x += vel
        motor_controller.diagonals(direction = 'wd', drivetime = drive_time)
    elif (keys[pygame.K_w] and keys[pygame.K_a]) or (keys[pygame.K_UP] and keys[pygame.K_LEFT]):
        print('wa')
        move = True; y -= vel; x -= vel
        motor_controller.diagonals(direction = 'wa', drivetime = drive_time)
    elif (keys[pygame.K_s] and keys[pygame.K_d]) or (keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]):
        print('sd')
        move = True; y += vel; x = vel
        motor_controller.diagonals(direction = 'sd', drivetime = drive_time)
    elif (keys[pygame.K_s] and keys[pygame.K_a]) or (keys[pygame.K_DOWN] and keys[pygame.K_LEFT]):
        print('sa')
        move = True; y += vel; x -= vel
        motor_controller.diagonals(direction = 'sa', drivetime = drive_time)
    
        
    if event.type == pygame.KEYDOWN and move != True:
        if event.key == pygame.K_UP or event.key == ord('w'):
            print('up')
            move = True
            y -= vel
            motor_controller.forward(drivetime = drive_time)
        elif event.key == pygame.K_DOWN or event.key == ord('s'):
            print('down')
            move = True
            y += vel
            motor_controller.backward(drivetime = drive_time)
        elif event.key == pygame.K_LEFT or event.key == ord('a'):
            print('left')
            move = True
            x -= vel
            motor_controller.left(drivetime = drive_time)
        elif event.key == pygame.K_RIGHT or event.key == ord('d'):
            print('right')
            move = True
            x += vel
            motor_controller.right(drivetime = drive_time)
        elif event.key == ord('q'):
            print('counterclockwise')
            move = True
            motor_controller.rotate(direction = 'q', drivetime = drive_time)
        elif event.key == ord('e'):
            print('clockwise')
            move = True
            motor_controller.rotate(direction = 'e', drivetime = drive_time)
    
    if move == False:
        motor_controller.stop()
    else:
        pass
        
    
    win.fill((0,0,0))  # Fills the screen with black
    pygame.draw.rect(win, (255,0,0), (x, y, width, height))   
    pygame.display.update() 
    
pygame.quit()