import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import time
import random

pygame.init()

# COLORS
black = (0, 0, 0)
white = (255, 255, 255)
dark_blue = (0, 0, 200)
dark_red = (200, 0, 0)
dark_green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)

# DISPLAY
display_width = 500
display_height = 800
window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Fruit Catcher")

# IMAGES
basket_img = pygame.image.load('basket.png')
basket_img = pygame.transform.scale(basket_img, (150, 100))
bg = pygame.image.load('background.jpg')
bomb_img = pygame.image.load('bomb.png')
bomb_img = pygame.transform.scale(bomb_img, (100, 100))

clock = pygame.time.Clock()

class Basket(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10
        self.hitbox = (self.x, self.y + 20, 150, 80)
    
    def draw(self, window):
        window.blit(basket_img, (self.x, self.y))
        self.hitbox = (self.x, self.y + 20, 150, 80)
    
class Fruits(object):
    def __init__(self, x, y, f_type):
        self.x = x
        self.y = y
        self.f_type = f_type
        self.vel = 10
        self.hitbox = (self.x, self.y, 100, 100)
    
    def draw(self, window):
        if self.f_type == 0:
            fruit = pygame.image.load('strawberry.png')
        elif self.f_type == 1:
            fruit = pygame.image.load('apple.png')  # Add a new fruit image
        fruit = pygame.transform.scale(fruit, (100, 100))
        window.blit(fruit, (self.x, self.y))
        self.hitbox = (self.x, self.y, 100, 100)


class Bombs(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 10
        self.hitbox = (self.x, self.y, 100, 100)
    
    def draw(self, window):
        window.blit(bomb_img, (self.x, self.y))
        self.hitbox = (self.x, self.y, 100, 100)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, x, y, size):
    regText = pygame.font.Font("freesansbold.ttf", size)
    textSurf, textRect = text_objects(msg, regText)
    textRect.center = (x, y)
    window.blit(textSurf, textRect)

def button(msg, x, y, width, height, inactive_color, active_color, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if (x+width > mouse[0] > x and y+height > mouse[1] > y):
        pygame.draw.rect(window, active_color, (x, y, width, height))
        if (click[0] == 1 and action != None):
            if (action == "play"):
                main()
            elif (action == "quit"):
                pygame.quit()
                quit()
            elif (action == "back"):
                game_intro()
    else:
        pygame.draw.rect(window, inactive_color, (x, y, width, height))
    message_to_screen(msg, (x + (width/2)), (y + (height/2)), 20)
        
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        window.blit(bg, (0,0))
        message_to_screen("Ayo Tangkap Aku ", display_width/2, display_height/2, 50)
        button("Start", 100, 450, 75, 50, dark_green, bright_green, "play")
        button("Quit", 200, 450, 75, 50, dark_red, bright_red, "quit")
        pygame.display.update()
        clock.tick(15)
    
def main():
    score = 0
    fruits = []
    bombs = []
    fruit_add_counter = 0
    bomb_add_counter = 0
    add_fruit_rate = 30
    add_bomb_rate = 100
    basket = Basket(display_width * 0.35, display_height - 160)
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False      
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket.x > basket.vel - 5:
            basket.x -= basket.vel
        elif keys[pygame.K_RIGHT] and basket.x < 500 - 150 - basket.vel:
            basket.x += basket.vel  
        window.blit(bg, (0,0))
        fruit_add_counter += 1
        bomb_add_counter += 1
        if fruit_add_counter == add_fruit_rate:
            fruit_add_counter = 0
            f_startx = random.randrange(100, display_width - 100)
            f_starty = 0
            f_type = random.randint(0, 1)
            fruits.append(Fruits(f_startx, f_starty, f_type))
        if bomb_add_counter == add_bomb_rate:
            bomb_add_counter = 0
            b_startx = random.randrange(100, display_width - 100)
            b_starty = 0
            bombs.append(Bombs(b_startx, b_starty))
        for f in fruits:
            if f.y < display_height:
                f.y += f.vel
                f.draw(window)
                if (f.hitbox[1] + f.hitbox[3]) > basket.hitbox[1] and f.hitbox[1] < (basket.hitbox[1] + basket.hitbox[3]):
                    if (f.hitbox[0] + f.hitbox[2]) > basket.hitbox[0] and f.hitbox[0] < (basket.hitbox[0] + basket.hitbox[2]):
                        fruits.remove(f)
                        score += 1
            else:
                fruits.remove(f)
        for b in bombs:
            if b.y < display_height:
                b.y += b.vel
                b.draw(window)
                if (b.hitbox[1] + b.hitbox[3]) > basket.hitbox[1] and b.hitbox[1] < (basket.hitbox[1] + basket.hitbox[3]):
                    if (b.hitbox[0] + b.hitbox[2]) > basket.hitbox[0] and b.hitbox[0] < (basket.hitbox[0] + basket.hitbox[2]):
                        game_over(score)
            else:
                bombs.remove(b)
        basket.draw(window)
        text = pygame.font.Font("freesansbold.ttf", 30)
        score_text = text.render("Score: " + str(score), 1, black)
        window.blit(score_text, (20, 20))
        pygame.display.update()
        clock.tick(60)
    
def game_over(score):
    window.fill(white)
    message_to_screen("skill issue", display_width/2, display_height/2 - 50, 70)
    message_to_screen("Score: " + str(score), display_width/2, display_height/2 + 50, 40)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

game_intro()
pygame.quit()
quit()
