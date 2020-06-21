import pygame

pygame.init()

win = pygame.display.set_mode((500, 480))
pygame.display.set_caption('#3 - Character Animation & Sprites')

x = 50
y = 405
# We change the width and height as the character img we are using is of size 64x64
width = 64
height = 64
velocity = 5

surface_width = 500
surface_height = 500

isJump = False
jump_count = 10

# This will allow us to change the fps(frame/pictures per second) in our game.
clock = pygame.time.Clock()

# Loading images of background and our character when he/ she moves left, right and faces in front
bg = pygame.image.load('pics/bg.jpg')
front_facing = pygame.image.load('pics/standing.png')
walk_right = [pygame.image.load('pics/R1.png'), pygame.image.load('pics/R2.png'), pygame.image.load('pics/R3.png'),
              pygame.image.load('pics/R4.png'), pygame.image.load('pics/R5.png'), pygame.image.load('pics/R6.png'),
              pygame.image.load('pics/R7.png'), pygame.image.load('pics/R8.png'), pygame.image.load('pics/R9.png')]
walk_left = [pygame.image.load('pics/L1.png'), pygame.image.load('pics/L2.png'), pygame.image.load('pics/L3.png'),
             pygame.image.load('pics/L4.png'), pygame.image.load('pics/L5.png'), pygame.image.load('pics/L6.png'),
             pygame.image.load('pics/L7.png'), pygame.image.load('pics/L8.png'), pygame.image.load('pics/L9.png')]


# When we are moving are character, we need to keep track of the direction of character is moving in,
# are they moving and how many step they have already moved, this is important so that we could,
# accurately display our character on the screen.
left = False
right = False
walk_count = 0


# Here we are going to 19 images of size 64x64,
# 9 for left side character, 9 for right side character and 1 for front facing character.
# Now, if want to change anything wrt to drawing we'll do it in this loop
def config_game_window():
    # making a var global means: If we made changes to walk_count in this function,
    # the changes woudn't be made outside of this method if we haven't made it global
    global walk_count

    # Now we don't want to fill our background with color, but with a pic instead,
    # i.e. instead of 'win.fill((0, 0, 0))' we write,
    win.blit(bg, (0, 0))  # second para is the position from where the picture will load
    
    # We did this bc if walk_count goes beyond 27, we'll run into index error, 
    # as we have only 9 img and I mean to run each one for 3 frames
    if walk_count + 1 > 27:
        walk_count = 0
    # Here we use walk_count//3 to round of the no. when divide by 3,
    # as we have 9 photos of each direction we can only have 3 frames and no.s from 1-9  when // 3 will give only 1,2&3.
    # We use '(x, y)' to move and keep track of our character.
    if left:
        win.blit(walk_left[walk_count//3], (x, y))
    elif right:
        win.blit(walk_right[walk_count//3], (x, y))
    else:
        win.blit(front_facing, (x, y))
    pygame.display.update()


# Main Loop
run = True
while run:
    # Instead 'pygame.time.delay(10)' we write the following to set our own fps value.
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and x > velocity:
        x -= velocity
        # This is so that we don't confuse are program that we have both right and left = True
        right = False
        left = True
    elif key[pygame.K_RIGHT] and x < (surface_width - width - velocity):
        x += velocity
        right = True
        left = False
    else:
        right = False
        left = False
        walk_count = 0
        
    if not isJump:
        # We deleted Up and Down movement,
        # because in real games, such movements are only possible through jumping
        if key[pygame.K_SPACE]:
            isJump = True
            right = False
            left = False
            
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

    # This is our main game loop,
    # we cannot create/ draw our character on every iteration,
    # it's not good habit, i.e. why create another method with sole purpose
    # of drawing and configuring our display screen of pygame
    config_game_window()

pygame.quit()
