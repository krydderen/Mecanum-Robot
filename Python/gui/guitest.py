import pygame
# * 1 - Adding pygame_gui
import pygame_gui
import cv2

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800,600))

background = pygame.Surface((800,600))
background.fill('black')

# * 1 - Create the UIManager
manager = pygame_gui.UIManager((800,600))
manager.set_visual_debug_mode((True))
# * 3 - Craete the Hello Button
hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350,275), (100,50)),
                                            text= 'Say Hello',
                                            manager=manager)

# * 2 - Create the clock timer
clock = pygame.time.Clock()

is_running = True


while is_running:
    # * 2 - Set timer ( FPS )
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # * 4 - Checking for button click event
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    print('Hello World!')
        
        # * 2 - Process manager events
        manager.process_events(event)
    
    # * 2 - Update manager
    manager.update(time_delta)
    
    window_surface.blit(background, (0,0))
    # * 2 - Make the manager draw the window_surface
    manager.draw_ui(window_surface)
    
    
    pygame.display.update()