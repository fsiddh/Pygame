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

# Score (S)
# (S1)For simplicity we are simply going to be increasing the score each time a bullet hits our goblin/enemy.
# (S2)We are going to start by creating a variable at the top of our program called score.
score = 0


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

        self.hitbox = (self.x + 20, self.y + 12, 24, 52)
        # We displayed hitbox on the screen to better understand the boundaries on our characters,
        # Now, as we understand it better we'll comment our hitbox rect.(Do not delete hitbox from init as,
        # it plays important role in removing bullets when bullet hits our enemy)
        # Although hitbox isn't displayed on our screen it doesn't mean that its not there!
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


# Health Bar (HB)
# What we are going to do now is give our enemy health and a health bar. This way we can see
# when we should remove it from the screen. To create the health bar we are going to draw two
# rectangles. One green and one red. We will change the width of the green rectangle (which will
# overlay the red one) each time the enemy is hit.
class Enemy:
    walkRight = [pygame.image.load('pics/R1E.png'), pygame.image.load('pics/R2E.png'),
                 pygame.image.load('pics/R3E.png'),
                 pygame.image.load('pics/R4E.png'), pygame.image.load('pics/R5E.png'),
                 pygame.image.load('pics/R6E.png'),
                 pygame.image.load('pics/R7E.png'), pygame.image.load('pics/R8E.png'),
                 pygame.image.load('pics/R9E.png'),
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

        self.health = 10  # This var. will keep track enemy's health
        self.visible = True  # If the health of enemy finishes the enemy will die. (It keeps check on this)

    def draw(self, win):
        self.move()

        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            # (HB1)Red Health bar
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0] - 15, self.hitbox[1] - 10, 50, 8))
            # (HB2) Green health bar overlaid on red one. It's width decreases as we hit the enemy as a result,
            # red bar starts to appear bullet by bullet.
            pygame.draw.rect(win, (0, 130, 0),
                             (self.hitbox[0] - 15, self.hitbox[1] - 10, 50 - (5 * (10 - self.health)), 8))

            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        # We displayed hitbox on the screen to better understand the boundaries on our characters,
        # Now, as we understand it better we'll comment our hitbox rect.
        # Although hitbox isn't displayed on uur screen it doesn't mean that its not there!
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # Draws the hit box around the enemy

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

    def hit(self, win):
        # (HB3)Health decrease on impact of bullet if health is not 0 yet(i.e. greater than 0)
        if self.health > 0:
            self.health -= 1
        # (HB4) If health on the enemy finishes off then he disappears.( visible will become False and enemy draw
        # function won't run as it has condition to work only if visible is True)
        else:
            self.visible = False
        print('Hit')
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
    # Renders our background
    win.blit(bg, (0, 0))

    # Draw our player
    man.draw(win)

    # Draws our bullets
    for bullet in bullets:
        bullet.draw(win)

    # Draws our Enemy
    enemy.draw(win)

    # (S5) After we create our font we need to render some text and blit it to the screen.
    text = font.render('Score: {}'.format(score), 1, (0, 0, 0))  # Arguments are: text, anti-aliasing, color
    win.blit(text, (370, 20))

    pygame.display.update()


# (S4)We would like to display this score to the screen. To do this we must first create a font object.
# The first argument is the font, next is size
# and then True to make our font bold (One can add another True to make their font italic)
font = pygame.font.SysFont('Type1', 30, True)

man = Player(200, 404.5, 64, 64)
enemy = Enemy(70, 410, 64, 64, 400)

bullets = []
bullets_fix = 0

run = True
# mainloop
while run:
    clock.tick(27)

    if bullets_fix > 0:
        bullets_fix += 1
    if bullets_fix > 3:
        bullets_fix = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # (S3)Next we are going to increment the score from our main loop where we check if the goblin is hit.
    for bullet in bullets:  # This for loop is for moving the bullets ! ("Do not delete this Comment")
        if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
            if bullet.x + bullet.radius * 2 > enemy.hitbox[0] and bullet.x - bullet.radius * 2 < enemy.hitbox[0] + \
                    enemy.hitbox[2]:
                enemy.hit(win)
                bullets.pop(bullets.index(bullet))
                score += 1

        if 500 > bullet.x > man.vel:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    if keys[pygame.K_SPACE] and bullets_fix == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(Projectiles(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0),
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
