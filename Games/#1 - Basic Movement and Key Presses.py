import pygame

pygame.init()

# Window side
win = pygame.display.set_mode((500, 500))

# Will  display the title on upper left corner of our pygame window
pygame.display.set_caption('First Pygame')

x = 50
y = 50
width = 40
height = 60
velocity = 5

run = True
while run:

    # Now we'll add time delay, so that everyhing doesn't happen supper quick
    pygame.time.delay(100)

    # On every run It'll check If the user have press exit button, if so it'll exit
    # If you will skip this code your pygame window won't close, and you've to stop the program in order to exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 1
    if keys[pygame.K_RIGHT]:
        x += 1

    if keys[pygame.K_UP]:
        y -= 1

    if keys[pygame.K_DOWN]:
        y += 1
            
    # Now we've to create a shape which'll appear on our window(We'll use rectangle)
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    # To show updated data we've to write this code
    pygame.display.update()

# Ends the program and end the window for us
pygame.quit()
