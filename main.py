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

isjump = False
v = 5
m = 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((50, random.randint(100, 400)))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                550,
            )
        )
        self.speed = 0.1

    def update(self):
        self.rect.move_ip(-1, 0) # work on enemy speed and then collision detection
        if self.rect.right < 0:
            self.kill()
        if self.rect.left == 0:
            self.kill()    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25,25))
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
pygame.time.set_timer(ADDENEMY, 250)

player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


running = True

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

    enemies.update()

    # Fill the screen with black
    screen.fill((70,70,70)) 

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    pygame.draw.rect(screen, [100, 100, 100], [0, 550, 800, 100],0)

    x = player.surf
    y = player.rect

    screen.blit(x,y)

    pygame.display.flip()

