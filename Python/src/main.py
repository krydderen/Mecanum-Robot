# Importing packages
import logging, cv2, pygame
from threading import Thread

# Importing utils
from utils.server import Server

def rungame(x, y, width, height, vel):
    run = True
    pygame.init()
    while run:
        pygame.time.delay(100)
        
        currentevents = pygame.event.get()
        
        for event in currentevents:
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        
        move = False
        stopped = False
        # # Change motor speed to high or low.
        # if keys[pygame.K_t]:
        #     if drive_speed == 'LOW':
        #         drive_speed = 'HIGH'
        #         logging.debug('Drive speed is now HIGH')
        #     elif drive_speed == 'HIGH':
        #         drive_speed = 'LOW'
        #         logging.debug('Drive speed is now LOW')   
        
        if (keys[pygame.K_w] and keys[pygame.K_d])   or (keys[pygame.K_UP] and keys[pygame.K_RIGHT]):
            logging.debug('wd')
            move = True; y -= vel; x += vel
            server.send('wd')
            # mc.wddiagonal(drivetime = drive_time, inputspeed = drive_speed)
        elif (keys[pygame.K_w] and keys[pygame.K_a]) or (keys[pygame.K_UP] and keys[pygame.K_LEFT]):
            logging.debug('wa')
            move = True; y -= vel; x -= vel
            server.send('wa')
            # mc.wadiagonal(drivetime = drive_time, inputspeed = drive_speed)
        elif (keys[pygame.K_s] and keys[pygame.K_d]) or (keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]):
            logging.debug('sd')
            move = True; y += vel; x += vel
            server.send('sd')
            # mc.sddiagonal(drivetime = drive_time, inputspeed = drive_speed)
        elif (keys[pygame.K_s] and keys[pygame.K_a]) or (keys[pygame.K_DOWN] and keys[pygame.K_LEFT]):
            logging.debug('sa')
            move = True; y += vel; x -= vel
            server.send('sa')
            # mc.sadiagonal(drivetime = drive_time, inputspeed = drive_speed)
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            logging.debug('up')
            move = True
            y -= vel
            server.send('w')
            # mc.forward(drivetime = drive_time, inputspeed = drive_speed)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            logging.debug('down')
            move = True
            y += vel
            server.send('s')
            # mc.backward(drivetime = drive_time, inputspeed = drive_speed)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            logging.debug('left')
            move = True
            x -= vel
            server.send('a')
            # mc.left(drivetime = drive_time, inputspeed = drive_speed)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            logging.debug('right')
            move = True
            x += vel
            server.send('d')
            # mc.right(drivetime = drive_time, inputspeed = drive_speed)
        elif keys[pygame.K_q]:
            logging.debug('counterclockwise')
            move = True
            server.send('q')
            # mc.rotate(direction = 'COUNTER_CLOCKWISE',drivetime = drive_time, inputspeed = drive_speed)
        elif keys[pygame.K_e]:
            logging.debug('clockwise')
            move = True
            server.send('e')
            # mc.rotate(direction = 'CLOCKWISE',drivetime = drive_time, inputspeed = drive_speed)
        
        if move == False and stopped == False:
            # mc.stop()
            server.send('stop')
            stopped = True
            pass
        else:
            pass
        
        win.fill((0,0,0))  # Fills the screen with black
        pygame.draw.rect(win, (255,0,0), (x, y, width, height))
        pygame.display.update()
        
    pygame.quit()
    server.disconnect()

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

    win = pygame.display.set_mode((500,500))
    pygame.display.set_caption("brom brom")

    x = 50
    y = 50
    width = 40
    height = 60
    vel = 5*2

    drive_time = 0.2
    drive_speed = 'LOW'
    # server.start()
    server  = Server()
    serverthread = Thread(target=server.start(), args=(),daemon = True)
    gamethread = Thread(target=rungame(x, y, width, height, vel), args=(x, y, width, height, vel), daemon=True)
    
    gamethread.start()
    serverthread.start()