import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Jumping and Boundaries')

screen_width = 500
screen_height = 500

# Jump Variables
isJump = False
jump_count = 10

x = 0
y = 440
width = 40
height = 60
velocity = 5

run = True
while run:
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()

    # Setting Boundaries so that your character doesn't go off the Screen
    # 'and x > 0' restricts our rect to go out of the left boundary
    if key[pygame.K_LEFT] and x > 0:
        x -= velocity
    # 'and x < (screen_width - width)' restricts our rect to go out of the Right boundary
    if key[pygame.K_RIGHT] and x < (screen_width - width):
        x += velocity

    if not(isJump):
        # 'and y > 0' restricts our rect to go out of the Upper boundary
        if key[pygame.K_UP] and y > 0:
            y -= velocity
        # 'and y < (screen_height - height)' restricts our rect to go out of the lower boundary
        if key[pygame.K_DOWN] and y < (screen_height - height):
            y += velocity
        # If Space bar is pressed loop will go into else
        if key[pygame.K_SPACE]:
            isJump = True
    else:
        if jump_count >= -10:
            gravity = 0.5
            if jump_count < 0:
                gravity = -0.5
            y -= pow(jump_count, 2) * 0.5 * gravity
            jump_count -= 1
        else:
            isJump = False
            jump_count = 10

    # Fill the trailing red color
    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()

pygame.quit()