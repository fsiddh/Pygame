import pygame
pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption("Shooting Bullets")

walkRight = [pygame.image.load('pics/R1.png'), pygame.image.load('pics/R2.png'), pygame.image.load('pics/R3.png'),
             pygame.image.load('pics/R4.png'), pygame.image.load('pics/R5.png'), pygame.image.load('pics/R6.png'),
             pygame.image.load('pics/R7.png'), pygame.image.load('pics/R8.png'), pygame.image.load('pics/R9.png')]
walkLeft = [pygame.image.load('pics/L1.png'), pygame.image.load('pics/L2.png'), pygame.image.load('pics/L3.png'),
            pygame.image.load('pics/L4.png'), pygame.image.load('pics/L5.png'), pygame.image.load('pics/L6.png'),
            pygame.image.load('pics/L7.png'), pygame.image.load('pics/L8.png'), pygame.image.load('pics/L9.png')]
bg = pygame.image.load('pics/bg.jpg')
char = pygame.image.load('pics/standing.png')

clock = pygame.time.Clock()


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        # So that we could know the direction in which our character is looking
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        # Obviously if our character is not standing, only then he'll move left or right
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        # If our character was moving left and then stopped we'll show first image from walkLeft list,
        # and if our character was walking right then stopped we'll show first image from walkRight list.
        else:
            if self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            else:
                win.blit(walkRight[0], (self.x, self.y))


class Enemy:
    walkRight = [pygame.image.load('pics/R1E.png'), pygame.image.load('pics/R2E.png'), pygame.image.load('pics/R3E.png'),
                 pygame.image.load('pics/R4E.png'), pygame.image.load('pics/R5E.png'), pygame.image.load('pics/R6E.png'),
                 pygame.image.load('pics/R7E.png'), pygame.image.load('pics/R8E.png'), pygame.image.load('pics/R9E.png'),
                 pygame.image.load('pics/R10E.png'), pygame.image.load('pics/R11E.png')]
    walkLeft = [pygame.image.load('pics/L1E.png'), pygame.image.load('pics/L2E.png'), pygame.image.load('pics/L3E.png'),
                pygame.image.load('pics/L4E.png'), pygame.image.load('pics/L5E.png'), pygame.image.load('pics/L6E.png'),
                pygame.image.load('pics/L7E.png'), pygame.image.load('pics/L8E.png'), pygame.image.load('pics/L9E.png'),
                pygame.image.load('pics/L10E.png'), pygame.image.load('pics/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]  # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = 3

    def draw(self, win):
        self.move()

        # Since we have 11 images for each animation our upper bound is 33.
        # We will show each image for 3 frames. 3 x 11 = 33.
        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:  # If we are moving to the right we will display our walkRight images
            win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:  # Otherwise we will display the walkLeft images
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

    def move(self):
        if self.vel > 0:  # If we are moving right
            if self.x < self.path[1] + self.vel:  # If we have not reached the furthest right point on our path('end').
                self.x += self.vel
            else:  # Change direction and move back the other way
                self.vel = self.vel * -1
                self.walkCount = 0
        else:  # If we are moving left
            if self.x > self.path[0] - self.vel:  # If we have not reached the furthest left point on our path('self.x')
                self.x += self.vel
            else:  # Change direction
                self.vel = self.vel * -1
                self.walkCount = 0


class Projectiles:
    # facing will define the direction of our bullets, left(-1) or right(1)
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        # This is how we draw the bullets
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def redraw_game_window():
    win.blit(bg, (0, 0))
    man.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    enemy.draw(win)
    pygame.display.update()


man = Player(200, 410, 64, 64)
enemy = Enemy(100, 410, 64, 64, 400)
bullets = []
run = True
# mainloop
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    for bullet in bullets:
        if 500 > bullet.x > man.vel:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(Projectiles(round(man.x + man.width//2), round(man.y + man.height // 2), 6, (0, 30, 0),
                                       facing))

        pygame.time.delay(10)
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 0.5
            if man.jumpCount < 0:
                neg = -0.5
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redraw_game_window()

pygame.quit()
