import pygame
import random

pygame.init()

width, height = 1500, 900
display = pygame.display.set_mode((width, height))

bg_img = pygame.image.load('road1.png')
bg_img = pygame.transform.scale(bg_img, (width, height))

bg_img2 = pygame.image.load('road2.png')
bg_img2 = pygame.transform.scale(bg_img2, (width, height))

bg_img_rect = bg_img.get_rect()

chicken_pic = pygame.image.load('chickmen.png')
chicken_pic = pygame.transform.scale(chicken_pic, (80, 80))
chicken_pic = pygame.transform.rotate(chicken_pic, 180)
chicken_rect = chicken_pic.get_rect()
chicken_rect = chicken_rect.move(750, height)

vehicle_pic1 = pygame.image.load('rock_1.png')
vehicle_pic1 = pygame.transform.scale(vehicle_pic1, (100, 100))
coin_pic = pygame.image.load('coin.png')
coin_pic = pygame.transform.scale(coin_pic, (30, 30))

x = y = 0
score = 0
font_1 = pygame.font.SysFont('arial', 60, bold=True)


class Object:
    def __init__(self, __x, __y, w, h, img):
        self.rect = pygame.Rect(__x, __y, w, h)
        self.render_rect = self.rect.copy()
        self.img = img

    def update(self, abc=0):
        self.rect.x += abc
        self.render_rect.update(self.rect.x + x, self.rect.y + y, self.rect.w, self.rect.h)

    def display_on_screen(self):
        display.blit(self.img, self.render_rect)


class Vehicle(Object):

    def __init__(self, __x, __y, img):
        self.x = __x
        self.y = __y
        super().__init__(__x, __y, img.get_width(), img.get_height(), img)
        self.right = True

    def moving(self, abc):
        self.x += abc
        if self.right:
            if self.x >= width - 100:
                self.right = False
        else:
            if self.x <= 0:
                self.right = True

    def getRect(self):
        return self.render_rect


class Coin(Object):

    def __init__(self, __x, __y, img):
        super().__init__(__x, __y, img.get_width(), img.get_height(), img)

    def getRect(self):
        return self.render_rect


class Bg(Object):
    def __init__(self, img: pygame.Surface, rect_under=pygame.Rect(0, height, 0, 0)):
        __x = rect_under.x
        __y = rect_under.y - img.get_height()
        super().__init__(__x, __y, img.get_width(), img.get_height(), img)
        self.rect_under = rect_under
        self.spawned_coins = False


vehicles = []
bgs = []
bgs.append(Bg(bg_img))
bgs.append(Bg(bg_img2, bgs[0].render_rect))

key = lambda k: pygame.key.get_pressed()[k]

for i in range(2):
    vehicles.append(Vehicle(600 + i * 200, 270 + i * 200, vehicle_pic1))

coins = []
for x in range(3):
    coins.append(Coin(random.randint(0, width - 70), random.randint(0, height - 70), coin_pic))


def spawnCoins(bg):
    for x in range(3):
        rand_y = random.randint(bg.render_rect.top, bg.render_rect.bottom)
        coins.append(Coin(random.randint(0, width - 70), rand_y, coin_pic))


game_loop = True
while game_loop:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        game_loop = False

    display.fill((0, 0, 0))

    score_text = font_1.render('score : ' + str(score), True, (255, 0, 0))

    y += key(pygame.K_w)
    y -= key(pygame.K_s)
    x += key(pygame.K_a)
    x -= key(pygame.K_d)

    if chicken_rect.left < 0:
        chicken_rect.left = 0

    if chicken_rect.right > width:
        chicken_rect.right = width

    if chicken_rect.top < 0:
        chicken_rect.top = 0

    if chicken_rect.bottom > height:
        chicken_rect.bottom = height

    for bg in bgs:
        bg.update()
        bg.display_on_screen()
        if bg.rect_under.colliderect(chicken_rect) and not bg.spawned_coins:
            bg.spawned_coins = True
            spawnCoins(bg)

    for vehicle in vehicles:
        amount = random.randint(1, 3)
        if not vehicle.right:
            amount *= -1
        vehicle.update(amount)
        vehicle.moving(amount)
        vehicle.display_on_screen()

        # if vehicle.getRect().colliderect(chicken_rect):
        #   quit(0)

    pos = (0, 0)
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        print(pos)

    for coin in coins:
        coin.update()
        coin.display_on_screen()
        if coin.getRect().colliderect(chicken_rect):
            coins.remove(coin)
            score += 1

    display.blit(chicken_pic, chicken_rect)
    display.blit(score_text, [700, 50])

    pygame.display.flip()
