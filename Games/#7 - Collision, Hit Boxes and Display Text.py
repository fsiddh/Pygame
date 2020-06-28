import pygame
pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption("Collision and Hit Boxes")

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
        self.standing = True
        # The elements in the hitbox are (top left x, top left y, width, height)
        self.hitbox = (self.x + 20, self.y + 12, 24, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            else:
                win.blit(walkRight[0], (self.x, self.y))

        # Since our player moves we will have to constantly redefine the hit box from within,
        # the draw method of our player class.
        # To do this we will simply copy the line from above into the draw method."
        self.hitbox = (self.x + 20, self.y + 12, 24, 52)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # To draw the hit box around the player


# We will repeat adding rect process in the enemy class.
# And after adding in the hit box we will also define a new method called hit.
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
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.hitcount = 0

    def draw(self, win):
        self.move()

        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # Draws a rectangle around the score
        pygame.draw.rect(win, (0, 0, 0), (330, 13, 140, 30), 2)  # Draws the hit box around the enemy

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    # NEW METHOD
    def hit(self, win):  # This will display when the enemy is hit
        # create a font object.
        # 1st parameter is the font file which is present in pygame.
        # 2nd parameter is size of the font
        font = pygame.font.Font('freesansbold.ttf', 20)

        # create a text surface object, on which text is drawn on it.
        score = font.render("Score = -{}xp".format(self.hitcount), True, (0, 0, 0))
        win.blit(score, (340, 20))
        pass


class Projectiles:
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def redraw_game_window():
    win.blit(bg, (0, 0))
    enemy.hit(win)
    man.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    enemy.draw(win)
    pygame.display.update()


man = Player(200, 404.5, 64, 64)
enemy = Enemy(70, 410, 64, 64, 400)

bullets = []

# Bullet Glitch (BG)
# There is a small glitch you may have noticed which causes our bullets to stick together,
# or shoot multiple at the same time. To fix this we must do the following.
# First we are going to create a variable called bullets_fix outside of our main loop."
bullets_fix = 0

run = True
# mainloop
while run:
    clock.tick(27)

    # (BG) After that we will place the following code at the top of our while loop.
    if bullets_fix > 0:
        bullets_fix += 1
    if bullets_fix > 3:
        bullets_fix = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # Collision
    # The fist collision we will check for is between the bullets and the enemy.
    # Every time we move a bullet we will check if it has collided with the enemy.
    # Since we already have a for loop setup to check if the bullets leave the screen,
    # we will do our collision check in there.
    # We are going to say these objects have collided if the x and y coordinate of the bullet sit inside the hit box,
    # of the enemy. We check this with the following code.
    for bullet in bullets:  # This for loop is for moving the bullets ! ("Do not delete this Comment")
        # Check if the bullets is in between the height of the hitbox
        if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
            # Check if the bullets is in between the length of the hitbox
            if bullet.x + bullet.radius*2 > enemy.hitbox[0] and bullet.x - bullet.radius*2 < enemy.hitbox[0] + \
                    enemy.hitbox[2]:
                enemy.hit(win)  # calls enemy hit method
                bullets.pop(bullets.index(bullet))  # removes bullet from bullet list
                enemy.hitcount += 1

        if 500 > bullet.x > man.vel:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # (BG) Then we will modify our space bar event check the following way. (by adding the "and shootLoop == 0")
    if keys[pygame.K_SPACE] and bullets_fix == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(Projectiles(round(man.x + man.width//2), round(man.y + man.height // 2), 6, (0, 0, 0),
                                       facing))

        bullets_fix = 1

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
