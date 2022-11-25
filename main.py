# Dino Game by Sana S

import pygame
import random 

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
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
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 10)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25,25))
        self.surf.fill((150,200,255))
        self.rect = self.surf.get_rect()
        print(self.rect.x, self.rect.y)

        self.isjumping = True
        self.isfalling = False

    def gravity(self):
        if self.rect.top != 550:
            self.rect.y += 1

    def jump(self):
        self.isjumping = True

        if self.isjumping is True:
            self.rect.move_ip(0,-2)
            pygame.time.wait(300)
            self.rect.move_ip(0,2)
            self.isjumping = False


    def update(self, pressed_keys):
        self.gravity()
        if pressed_keys[K_UP]:
            self.jump()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)

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

player = Player()

running = True

while running: 
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Fill the screen with black
    screen.fill((70,70,70)) 

    pygame.draw.rect(screen, [100, 100, 100], [0, 550, 800, 100],0)

    x = player.surf
    y = player.rect

    screen.blit(x,y)

    pygame.display.flip()

