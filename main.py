import pygame
import random
pygame.init()
width, height = 900, 900
display = pygame.display.set_mode((width, height))
rock1 = pygame.image.load('rock1-removebg-preview.png')
rock1 = pygame.transform.scale(rock1, (60, 60))
apple = pygame.image.load('apple-removebg-preview.png')
apple = pygame.transform.scale(apple, (70, 70))

snake = pygame.image.load('rock1-removebg-preview.png')
snake = pygame.transform.scale(snake, (70, 70))
snake_rect = snake.get_rect()
snake_rect = snake_rect.move(100, 100)
dx, dy = 0, 0

bg_img = pygame.image.load('snake_bg.png')
bg_img = pygame.transform.scale(bg_img, (width, height))

score = 0
font_1 = pygame.font.SysFont('ariel', 60, bold=True)
snake_game = True


# snake game class :
class Apple:
    x = 0
    y = 0
    img = 0

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

    def display_on_screen(self):
        display.blit(self.img, (self.x, self.y))

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())


# snake game class :
class SnakeAdd:
    snake_rect = 0
    img = 0

    def __init__(self, snake_rect, img):
        self.snake_rect = snake_rect
        self.img = img


apples = []
apples.append(Apple(random.randint(0, width - 70), random.randint(0, height - 70), apple))

snakeAdd = []

game_loop = True
while game_loop:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        game_loop = False
    if snake_game:
        score_text = font_1.render('score :  ' + str(score), True, (255, 0, 0))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = -1
            elif event.key == pygame.K_DOWN:
                dy = 1
            elif event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                dy = 0
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                dx = 0
            elif snake_rect.right >= width or snake_rect.left <= 0:
                dx = 0
            elif snake_rect.bottom >= height or snake_rect.top <= 0:
                dy = 0

        if snake_rect.left < 0:
            snake_rect.left = 0

        if snake_rect.right > width:
            snake_rect.right = width

        if snake_rect.top < 0:
            snake_rect.top = 0

        if snake_rect.bottom > height:
            snake_rect.bottom = height

        pos = (0, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

        # display.blit(bg_img, [0, 0])
        display.fill((30, 30, 30))
        for a in apples:
            a.display_on_screen()
            if a.getRect().colliderect(snake_rect):
                apples.remove(a)
                apples.append(Apple(random.randint(0, width - 70), random.randint(0, height - 70), apple))
                score += 1

        snake_rect = snake_rect.move(dx, dy)
        display.blit(snake, snake_rect)
        display.blit(score_text, [300, 0])
    pygame.display.flip()
