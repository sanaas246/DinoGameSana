# Dino Game by Sana S

import pygame
import random 

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Variables
isjump = False
x1 = 800
loss = False
running = True
white = (255,255,255)
red = (255,51,51)
pink = (255,204,229)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.x = 800
        self.y = 450
        self.w = 50
        self.h = 100
        self.color = (100, 100, 100)
        self.speed = -0.05

    def update(self):
        self.x += self.speed
        if self.x <= 0:
            self.kill()
    
    def draw(self): # draw multiple rects
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h], 0)
        if self.x <= 50:
            self.x = 800
            self.y = random.randint(100, 450)
            self.w = 50
            self.h = 300
            self.color = (100, 100, 100)
            self.speed -= random.uniform(0,1)
            if self.speed <= -0.8:
                self.speed = -0.05
            print(self.speed)
            pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h], 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25,25))
        if loss == True:
            self.surf.fill((0,0,0))
            print("loss")
        else:
            self.surf.fill((150,200,255))
        self.rect = self.surf.get_rect()
        print(self.rect.x, self.rect.y)

    def gravity(self):
        if self.rect.top != 550:
            self.rect.y += 1

    def jump(self):
        dy = -3
        accel = 1
        dy += accel
        self.isjumping = True
        if self.isjumping == True:
            self.rect.y += dy
            self.isjumping = False

    def update(self, pressed_keys):
        self.gravity()
        if pressed_keys[K_UP] or pressed_keys[K_SPACE]:
            self.jump()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1, 0)

            # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= 550:
            self.rect.bottom = 550  
            dy = 0      

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDENEMY, 250)

player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

new_enemy = Enemy()
enemies.add(new_enemy)




# YOU LOST sign
pygame.display.set_caption('Show Text')
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('YOU LOST', True, red, pink)
textRect = text.get_rect()
textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

while running: 
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # enemies update
    for enemy in enemies:
        enemy.update()
    

    # Fill the screen with black
    screen.fill((70,70,70)) 

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    pygame.draw.rect(screen, [100, 100, 100], [0, 550, 800, 100],0)

    pygame.draw.rect(screen, [30, 30, 30], [x1, 350, 50, 50], 0)


    # print the enemy 
    for enemy in enemies:
        enemy.draw()


    if player.rect.y >= enemy.y and player.rect.y <= enemy.y + 300 and player.rect.x >= enemy.x and player.rect.x <= enemy.x + 50:
        enemy.speed = 0
        loss = True
        
    if loss == True:
        screen.fill((0,0,0))
        for enemy in enemies:
            enemy.kill()
        screen.blit(text,textRect)
        player.kill()
        

    x = player.surf
    y = player.rect

    screen.blit(x,y)



    pygame.display.flip()

#  add a score num  : everytime an enemy kills itself to change the speed, increase the score num
