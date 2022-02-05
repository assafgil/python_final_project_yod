import pygame
import random
import time

pygame.init()

width, height = 1500, 900
display = pygame.display.set_mode((width, height))
rock_pic = pygame.image.load('rock_2.png')
rock_pic = pygame.transform.scale(rock_pic, (100, 100))
rock_pic2 = pygame.image.load('rock_1.png')
rock_pic2 = pygame.transform.scale(rock_pic2, (100, 100))

# cannon_pic = pygame.image.load('cannon_by_me-removebg-preview.png')
# cannon_pic = pygame.transform.scale(cannon_pic, (115, 115))

cannon_pic_array = []
p1 = pygame.image.load('mycanon1.png')
p1 = pygame.transform.scale(p1, (115, 115))
p1.set_colorkey((255, 255, 255))
p1 = p1.convert_alpha()
cannon_pic_array.append(p1)

p1 = pygame.image.load('mycanon2.png')
p1 = pygame.transform.scale(p1, (115, 115))
p1.set_colorkey((255, 255, 255))
p1 = p1.convert_alpha()
cannon_pic_array.append(p1)

p1 = pygame.image.load('mycanon3.png')
p1 = pygame.transform.scale(p1, (115, 115))
p1.set_colorkey((255, 255, 255))
p1 = p1.convert_alpha()
cannon_pic_array.append(p1)

p1 = pygame.image.load('mycanon4.png')
p1 = pygame.transform.scale(p1, (115, 115))
p1.set_colorkey((255, 255, 255))
p1 = p1.convert_alpha()
cannon_pic_array.append(p1)

cannon_pic_loc = 3

cannon_pic_rect = p1.get_rect()
cannon_pic_rect = cannon_pic_rect.move(100, height - 155)

cannon_pic = cannon_pic_array[cannon_pic_loc]

dx, dy = 0, 0
bullet = pygame.image.load('bullet_cannon-removebg-preview.png')
bullet = pygame.transform.scale(bullet, (60, 60))

bullet_save = bullet

pygame.display.set_caption('A Rock Game')

shooting_sound = pygame.mixer.Sound('WhatsApp Video 2022-02-03 at 20.19.25.wav')
rock_explosion_sound = pygame.mixer.Sound('WhatsApp Video 2022-02-01 at 22.28.24.wav')
pygame.mixer.music.load('Without-Orchestra-2020-03-15_-_Western_Adverntures_-_David_Fesliyan.wav')
pygame.mixer.music.play(-1)

score = 0
level = 1
score_helper = 0
step2 = 0.1

font_1 = pygame.font.SysFont('ariel', 60, bold=True)
font_loss = pygame.font.SysFont('ariel', 75, bold=True)
font_3 = pygame.font.SysFont('david', 40, bold=True)
game_font = pygame.font.SysFont('ariel', 90, bold=True)

restart_text = font_1.render('restart', True, (255, 0, 0))
game_text = game_font.render('A Rock Game', True, (0, 0, 0))
game_text_rect = game_text.get_rect()
game_text_rect = game_text_rect.move(750, 200)
game_text_rect_bool = False

thanks_text = font_3.render('Special thanks for Gil Natanzon', True, (0, 0, 0))
go_back_text = font_1.render('menu', True, (255, 0, 0))
winner_text = game_font.render('winner ! ', True, (255, 0, 0))

bg = pygame.image.load('bg_rock.png')
bg = pygame.transform.scale(bg, (width, height))

bg2 = pygame.image.load('bg_rock_game2.png')
bg2 = pygame.transform.scale(bg2, (width, height))

rail = pygame.image.load('rail.png')
rail = pygame.transform.scale(rail, (41, 76))

arrow_1 = pygame.image.load('arrow-removebg-preview.png')
arrow_1 = pygame.transform.scale(arrow_1, (140, 140))

arrow_2 = arrow_1
arrow_2 = pygame.transform.rotate(arrow_2, 180)

pygame.display.set_icon(bg2)

game_time = time.monotonic_ns()
game_time_jump = time.monotonic_ns()

passed_screen = False
regular_mode = False
high_scores_screen = False

gravity = False
start_gravity = 0

loss_by_enemy = False


class Rock:
    x = 0
    y = 0
    img = 0
    step = 0.1
    isAlive = True

    def __init__(self, x, y, step, img):
        self.x = x
        self.y = y
        self.step = step
        self.img = img

    def display_on_screen(self):
        display.blit(self.img, (self.x, self.y))

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def goDown(self):
        self.y += self.step

    def transform(self):
        self.img = pygame.transform.scale(self.img, (random.randint(75, 150), random.randint(75, 150)))


class Shot:
    x = 100
    y = 1000
    img = 0
    step = 1

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

    def moveup(self):
        self.y -= self.step

    def display_on_screen(self):
        display.blit(self.img, (self.x, self.y))

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())


class Enemy:
    def __init__(self, x, y, img, step):
        self.x = x
        self.y = y
        self.img = img
        self.step = step

    def moving(self):
        self.x += self.step

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def display_on_screen(self):
        display.blit(self.img, (self.x, self.y))


class Rail:
    def __init__(self, x, y, img, step):
        self.x = x
        self.y = y
        self.img = img
        self.step = step

    def display_on_screen(self):
        display.blit(self.img, (self.x, self.y))

    def moving(self):
        self.x += self.step


rails = []
i = -41
while i <= 1500:
    rails.append(Rail(i, 790, rail, 1))
    i += 41

enemies = []

shotArray = []

rocks = []

img1 = rock_pic2


def restart():
    for x in rocks:
        x.step = 0.1
    shotArray.clear()
    rocks.clear()
    for i in range(level + 2):
        rocks.append(Rock(250 + 400 * i, 0, 0.1, img1))
    enemies.clear()


upgrade_tool = 1


def levelUpgrade():
    shotArray.clear()
    rocks.clear()
    for i in range(level + 2):
        rocks.append(Rock(250 + 200 * i, 50, 0.3 * upgrade_tool, img1))


def winPause():
    for j in rocks:
        j.step = 0
    if len(shotArray) > 0:
        shotArray.clear()
    for e in enemies:
        e.step = 0


def load_score():
    file = open('high_score.txt', 'r')
    out = file.read()
    file.close()
    # print("load=",out)

    return int(out)


def save_score(score):
    file = open('high_score.txt', 'w')
    # print("score",str(score))
    file.write(str(score))
    file.close()


high_score = load_score()

restart()
game_loop = True
while game_loop:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        game_loop = False
    if passed_screen:
        rand_1 = random.randint(1, 2)
        if rand_1 == 1:
            img1 = rock_pic
        else:
            img1 = rock_pic2

        cannon_pic_loc = cannon_pic_loc + 0.01
        if cannon_pic_loc > len(cannon_pic_array):
            cannon_pic_loc = 0
        cannon_pic = cannon_pic_array[int(cannon_pic_loc)]

        # creating enemies:
        current_time = time.monotonic_ns()
        if current_time - game_time > 10000000000:
            game_time = current_time
            enemies.append(Enemy(1500, 770, arrow_2, -1))
            enemies.append(Enemy(-50, 770, arrow_1, 1))

        # jumping:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and cannon_pic_rect.y == height - 155:
            gravity = True
            start_gravity = time.time()
        if cannon_pic_rect.y > height - 155:
            cannon_pic_rect.y = height - 155
            gravity = False
        if gravity:
            cannon_pic_rect.y = height - (
                    50 * (time.time() - start_gravity) - 50 * (time.time() - start_gravity) ** 4) - 230

        score_text = font_1.render('score :  ' + str(score_helper), True, (255, 0, 0))
        loss_text = font_loss.render('you lost ! ', True, (255, 0, 0))
        level_text = font_1.render('level is  : ' + str(level), True, (255, 0, 0))

        cannon_pic_rect.centerx = pygame.mouse.get_pos()[0]
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            # if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mixer.Sound.play(shooting_sound)
            shotArray.append(Shot(cannon_pic_rect.x + 30, cannon_pic_rect.y, bullet))

        if cannon_pic_rect.left < 0:
            cannon_pic_rect.left = 0

        if cannon_pic_rect.right > width:
            cannon_pic_rect.right = width

        if cannon_pic_rect.top < 0:
            cannon_pic_rect.top = 0

        if cannon_pic_rect.bottom > height:
            cannon_pic_rect.bottom = height

        pos = (0, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # print(pos)

            if 0 <= pos[0] <= 122 and 0 <= pos[1] <= 27:
                if score_helper > high_score:
                    high_score = score_helper
                    save_score(high_score)

                passed_screen = False
                loss_by_enemy = False
                level = 1
                score = 0
                score_helper = 0
                for rock in rocks:
                    rock.step = 0.1
                restart()

        display.fill((50, 50, 50))
        display.blit(bg, [0, 0])

        # rails:
        for a_rail in rails:
            a_rail.display_on_screen()
            a_rail.moving()
            if a_rail.x > width:
                rails.remove(a_rail)
                rails.append(Rail(-18, 790, rail, 1))

        for enemy in enemies:
            enemy.display_on_screen()
            enemy.moving()

        for rock in rocks:
            rock.display_on_screen()
            rock.goDown()

            for rock_x in rocks:
                if rock.y >= height - 50:
                    rock_x.transform()

                    display.blit(loss_text, [600, 400])
                    display.blit(restart_text, [640, 550])

                    if len(shotArray) > 0:
                        shotArray.clear()

                    if 640 <= pos[0] <= 840 and 550 <= pos[1] <= 575:
                        if score_helper > high_score:
                            high_score = score_helper
                            save_score(high_score)

                        level = 1
                        score = 0
                        score_helper = 0
                        rock.step = 0.1
                        upgrade_tool = 1
                        restart()

            cannon_pic_rect = cannon_pic_rect.move(dx, dy)
            display.blit(cannon_pic, cannon_pic_rect)

            for shot in shotArray:
                shot.display_on_screen()
                shot.moveup()

                if len(shotArray) == 6 and shot in shotArray:
                    shotArray.remove(shot)

                if shot.y <= 0 and shot in shotArray:
                    shotArray.remove(shot)
                if shot.getRect().colliderect(rock.getRect()):
                    # pygame.mixer.Sound.play(rock_explosion_sound)
                    score += 1

                    score_helper += 1
                    newRock = Rock(random.randint(100, width - 150), 50, rock.step + 0.05, img1)
                    rocks.append(newRock)
                    newRock.transform()
                    if shot in shotArray:
                        shotArray.remove(shot)
                    rocks.remove(rock)

        display.blit(score_text, [600, 50])
        display.blit(go_back_text, [0, 0])

        # loosing by enemy

        for e in enemies:
            if e.getRect().colliderect(cannon_pic_rect):
                loss_by_enemy = True

        if loss_by_enemy:
            display.blit(loss_text, [600, 400])
            display.blit(restart_text, [640, 550])
            winPause()
            if len(shotArray) > 0:
                shotArray.clear()

            if 640 <= pos[0] <= 840 and 550 <= pos[
                1] <= 575:
                loss_by_enemy = False
                if score_helper > high_score:
                    high_score = score_helper
                    save_score(high_score)

                level = 1
                score = 0
                score_helper = 0
                for rock in rocks:
                    rock.step = 0.1
                upgrade_tool = 1
                restart()

        if regular_mode:
            display.blit(level_text, [100, 730])
            if score == 25:
                score = 0
                level += 1
                levelUpgrade()
                upgrade_tool += 1

        # win:
        if level == 3:
            display.blit(winner_text, [600, 400])
            display.blit(restart_text, [640, 550])
            winPause()

            if 640 <= pos[0] <= 840 and 550 <= pos[1] <= 575:
                level = 1
                score = 0
                score_helper = 0
                for rock in rocks:
                    rock.step = 0.1
                upgrade_tool = 1
                restart()

        pygame.display.flip()

    # menu screen :

    pos = (0, 0)
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        # print(pos)
        if high_scores_screen and 0 <= pos[0] <= 122 and 0 <= pos[1] <= 27:
            high_scores_screen = False

    if not passed_screen and not high_scores_screen:
        display.blit(bg2, [0, 0])
        font_2 = pygame.font.SysFont('j', 70, bold=True)
        start_text = font_2.render('regular mode  ', True, (0, 0, 0))
        start_text2 = font_2.render('infinite mode ', True, (0, 0, 0))
        quit_text = font_3.render('QUIT', True, (0, 0, 0))
        highScores_text_enter = font_2.render('High scores', True, (0, 0, 0))
        highScores_text = font_2.render('highest score is :' + str(high_score), True, (0, 0, 0))
        menu_text_passed_screen = font_1.render('menu', True, (255, 0, 0))

        display.blit(start_text, [625, 450])
        display.blit(start_text2, [625, 600])
        display.blit(highScores_text_enter, [625, 750])
        display.blit(game_text, game_text_rect)
        display.blit(thanks_text, [100, 800])
        display.blit(quit_text, [1300, 800])

        if game_text_rect_bool:
            game_text_rect.y += 1
            if game_text_rect.y > 250:
                game_text_rect_bool = False
        if not game_text_rect_bool:
            game_text_rect.y -= 1
            if game_text_rect.y < 150:
                game_text_rect_bool = True

        if 625 <= pos[0] <= 990 and 450 <= pos[1] <= 484:
            passed_screen = True
            regular_mode = True

        if 625 <= pos[0] <= 985 and 600 <= pos[1] <= 635:
            passed_screen = True
            regular_mode = False

        if 625 <= pos[0] <= 940 and 750 <= pos[1] <= 788:
            high_scores_screen = True
            display.blit(bg2, [0, 0])
            display.blit(menu_text_passed_screen, [0, 0])
            display.blit(highScores_text, [450, 500])

        # print(pos)

        if 1300 <= pos[0] <= 1400 and 800 <= pos[1] <= 824:
            quit(0)

        pygame.display.flip()
