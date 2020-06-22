import pygame
pygame.init()

no_key_press_left = False
no_key_press_right = False

screen_width = 500
screen_height = 480

win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Optimization and OOP')

bg = pygame.image.load('pics/bg.jpg')
front_facing = pygame.image.load('pics/standing.png')
walk_right = [pygame.image.load('pics/R1.png'), pygame.image.load('pics/R2.png'), pygame.image.load('pics/R3.png'),
              pygame.image.load('pics/R4.png'), pygame.image.load('pics/R5.png'), pygame.image.load('pics/R6.png'),
              pygame.image.load('pics/R7.png'), pygame.image.load('pics/R8.png'), pygame.image.load('pics/R9.png')]
walk_left = [pygame.image.load('pics/L1.png'), pygame.image.load('pics/L2.png'), pygame.image.load('pics/L3.png'),
             pygame.image.load('pics/L4.png'), pygame.image.load('pics/L5.png'), pygame.image.load('pics/L6.png'),
             pygame.image.load('pics/L7.png'), pygame.image.load('pics/L8.png'), pygame.image.load('pics/L9.png')]


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.char_width = width
        self.char_height = height
        self.vel = 7.5
        self.isJump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.clock = pygame.time.Clock()

    def draw(self, win):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        if self.left:
            win.blit(walk_left[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
        elif self.right:
            win.blit(walk_right[self.walk_count // 3], (self.x, self.y))
        else:
            win.blit(front_facing, (self.x, self.y))


def config_game_screen():
    win.blit(bg, (0, 0))
    man.draw(win)
    pygame.display.update()


man = Player(200, 410, 64, 64)
run = True
while run:
    man.clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        no_key_press_left = True
    elif key[pygame.K_RIGHT] and man.x < screen_width - man.char_width - man.vel:
        man.x += man.vel
        man.left = False
        man.right = True
        no_key_press_left = True
    else:
        if no_key_press_left:
            win.blit(walk_left[0], (man.x, man.y))
        elif no_key_press_right:
            win.blit(walk_right[0], (man.x, man.y))
        man.walk_count = 0
    if not man.isJump:
        if key[pygame.K_UP]:
            man.isJump = True
            man.left = True
            man.right = True
            man.walk_count = 0
    else:
        if man.jump_count >= -10:
            gravity = 1.2
            if man.jump_count < 0:
                gravity = -1.2
            man.y -= pow(man.jump_count, 2) * 0.3 * gravity
            man.jump_count -= 1
        else:
            man.isJump = False
            man.jump_count = 10

    config_game_screen()


pygame.quit()

