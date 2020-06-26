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


# We created a class for objects that'll be coming out of our character
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

    # As mentioned in the previous files, this method is used for drawing
    # Therefore this loop create/draws the bullets
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


man = Player(200, 410, 64, 64)
# This 'bullets' list will contain all of our bullets
bullets = []
run = True
# mainloop
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # This will have our multiple bullets
    # (We didn't wanted to have only one bullet coming out of our man i.e. why we create this for loop)
    for bullet in bullets:
        if 500 > bullet.x > man.vel:
            # This piece of code will move our bullets
            bullet.x += bullet.vel
        else:
            # This code will take bullet val and find it's index from bullets list and then pop that index from bullets
            bullets.pop(bullets.index(bullet))

    # In order to shoot them from our character the following code is written,
    # Adding bullet(solid spheres) in bullets list:
    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        # How many bullets to have on screen on a single go,
        # acc. to this condition 5 bullet will be added in 'bullets' list.
        if len(bullets) < 5:
            # As we created our man object, here we create our bullet object(used below in the bullets for loop),
            # over here we called Projectile class and initialized the bullet's shape n all
            bullets.append(Projectiles(round(man.x + man.width//2), round(man.y + man.height // 2), 6, (0, 0, 0),
                                       facing))

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        # If man is walking in the left direction he's not standing
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        # If man is walking in the right direction he's not standing
        man.standing = False
    else:
        # If man is not walking then he's standing
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
