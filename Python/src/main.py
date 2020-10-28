# Importing packages
import logging
import cv2
import pygame
import queue
import threading
from concurrent.futures import ThreadPoolExecutor

# Importing utils
from utils.server import Server


def rungame(queue, events):
    while not events.is_set():
        win = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("brom brom")

        x = 50
        y = 50
        width = 40
        height = 60
        vel = 5*2
        drive_time = 0.2
        drive_speed = 'LOW'
        connected = False
        stopped = False
        run = True
        pygame.init()
        while run:
            connected = server.isconnected()
            # connected = False
            logging.debug(f"Server connection: {server.isconnected()}")
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
                if connected:
                    server.send('wd')
                # mc.wddiagonal(drivetime = drive_time, inputspeed = drive_speed)
            elif (keys[pygame.K_w] and keys[pygame.K_a]) or (keys[pygame.K_UP] and keys[pygame.K_LEFT]):
                logging.debug('wa')
                move = True
                y -= vel
                x -= vel
                if connected:
                    server.send('wa')
                # mc.wadiagonal(drivetime = drive_time, inputspeed = drive_speed)
            elif (keys[pygame.K_s] and keys[pygame.K_d]) or (keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]):
                logging.debug('sd')
                move = True
                y += vel
                x += vel
                if connected:
                    server.send('sd')
                # mc.sddiagonal(drivetime = drive_time, inputspeed = drive_speed)
            elif (keys[pygame.K_s] and keys[pygame.K_a]) or (keys[pygame.K_DOWN] and keys[pygame.K_LEFT]):
                logging.debug('sa')
                move = True
                y += vel
                x -= vel
                if connected:
                    server.send('sa')
                # mc.sadiagonal(drivetime = drive_time, inputspeed = drive_speed)
            elif keys[pygame.K_w] or keys[pygame.K_UP]:
                logging.debug('up')
                move = True
                y -= vel
                if connected:
                    server.send('w')
                # mc.forward(drivetime = drive_time, inputspeed = drive_speed)
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                logging.debug('down')
                move = True
                y += vel
                if connected:
                    server.send('s')
                # mc.backward(drivetime = drive_time, inputspeed = drive_speed)
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                logging.debug('left')
                move = True
                x -= vel
                if connected:
                    server.send('a')
                # mc.left(drivetime = drive_time, inputspeed = drive_speed)
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                logging.debug('right')
                move = True
                x += vel
                if connected:
                    server.send('d')
                # mc.right(drivetime = drive_time, inputspeed = drive_speed)
            elif keys[pygame.K_q]:
                logging.debug('counterclockwise')
                move = True
                if connected:
                    server.send('q')
                # mc.rotate(direction = 'COUNTER_CLOCKWISE',drivetime = drive_time, inputspeed = drive_speed)
            elif keys[pygame.K_e]:
                logging.debug('clockwise')
                move = True
                if connected:
                    server.send('e')
                # mc.rotate(direction = 'CLOCKWISE',drivetime = drive_time, inputspeed = drive_speed)

            if move == False and stopped == False:
                # mc.stop()
                if connected:
                    server.send('stop')
                stopped = True
                pass
            else:
                pass

            win.fill((0, 0, 0))  # Fills the screen with black
            pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
            pygame.display.update()

        logging.debug("Closing server...")
        server.close()
        logging.debug("Closing game...")
        pygame.quit()
        break


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.INFO)

    server = Server()

    pipeline = queue.Queue(maxsize=5)
    event = threading.Event()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(rungame, pipeline, event)
        executor.submit(server.start, pipeline, event)

    # server.start()
    # server  = server()
    # serverthread = Theread(target=server.start(), args=(), daemon = True)
    # gamethread = Thread(target=rungame(), args=(), daemon=True)

    # gamethread.start()
    # serverthread.start()
