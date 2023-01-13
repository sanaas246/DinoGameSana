# Dodging Game by Sana S

# All imports
import pygame
import random
import json 

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

# Screen Measures
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Variables
isjump = False
x1 = 800
loss = False
running = True
score = 0

# HighScore File (Score)
file = open("users.txt", "r")
user_from_file = file.read()
file.close() 
userscores = json.loads(user_from_file)

# SPRITES   
# Player Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25,25))
        self.surf.fill((150,200,255))
        self.rect = self.surf.get_rect()

    # the player will fall to the ground
    def gravity(self):
        if self.rect.top != 550:
            self.rect.y += 1

    # the player will jump and then gravity will the player down
    def jump(self):
        dy = -3
        accel = 1
        dy += accel
        self.isjumping = True
        if self.isjumping == True:
            self.rect.y += dy
            self.isjumping = False

    # the arrow use
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

# Enemy Group
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.x = 800
        self.y = 450
        self.w = 50
        self.h = 100
        self.color = (100, 100, 100)
        self.speed = -0.06
        self.score = 0
        self.loss = False

    # Update the location
    def update(self):
        self.x += self.speed
        if self.x <= -50:
            self.teleport()
    
    # Draw the enemy
    def draw(self): # draw multiple rects
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h], 0)
        
    # Speed of enemy and how it moves
    def teleport(self):
        self.x = 800
        self.y = random.randint(100, 450)
        self.speed -= random.uniform(0,1)
        if self.speed <= -0.8:
            self.speed = -0.05
        print(self.speed)
        if self.x != 1:
            print("scoring works")
            self.score += 1
            print(self.score)

    # Collision Detection
    def collision(self, xval, yval): 
        # Collision Detection
        if yval >= self.y and yval <= self.y + 100 and xval >= self.x and xval <= self.x + 50:
            enemy.speed = 0
            print("loss")
            self.kill() 
            self.loss = True    

# Initializing screen and pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ADDENEMY = pygame.USEREVENT + 1

# PyGame Variables
font = pygame.font.Font('freesansbold.ttf', 32)

# Adding Sprites to a Group
player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
enemies.add(Enemy())


# Loop to run screen
while running: 
    for event in pygame.event.get():
        # quit 
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            # restart
            if event.key == pygame.K_r:
                # reset to game mode
                isjump = False
                x1 = 800
                loss = False
                for enemy in enemies:
                    enemy.score = 0
                player.rect.x = 50
                player.rect.y = 500
                new_enemy = Enemy()
                enemies.add(new_enemy)
        # quit 
        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            if loss == False:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
    
    # Add the highscore to json
    def addhs(): 
        users_json = json.dumps(userscores)
        file = open("users.txt", "w")
        file.write(users_json)
        file.close()

    # enemies update and lost 
    for enemy in enemies:
        enemy.update()
        enemy.collision(player.rect.x, player.rect.y)
        if enemy.loss == True:
            drawendscreen()

    # Pressing keys to move player
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # DRAWING
    # Fill the screen with black
    for enemy in enemies:
        if enemy.loss == False:
            screen.fill((70,70,70)) 
            # the ground
            pygame.draw.rect(screen, [100, 100, 100], [0, 550, 800, 100],0)
    

    # End Game Screen
    text1 = font.render("YOU LOST", True, (255,51,51))
    text1Rect = text1.get_rect()
    text1Rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 50)

    # Draw Score
    for enemy in enemies:
        text2 = font.render(f"Score: {enemy.score}", True, (0,245,50)) 
        text2Rect = text2.get_rect()
        text2Rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2))

        pygame.display.set_caption(str(enemy.score))

    # the ending screen 
    def drawendscreen():
        player.kill()
        screen.fill((0,0,0))
        # add the new highscore to the userscores json list 
        for enemy in enemies:    
            if enemy.score > userscores[0]:
                del(userscores[0])
                userscores.append(enemy.score)
            # save the userscores file
        addhs()
        screen.blit(text1,text1Rect)
        screen.blit(text2,text2Rect)

        # print the highscore to the screen    
        text3 = font.render(f"High Score: {userscores[0]}", True, (255,204,229)) 
        text3Rect = text3.get_rect()
        text3Rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2)+ 50)
        screen.blit(text3,text3Rect)
        # Instructions to restart or reset game
        text4 = font.render(f"To restart, press R. To quit, press ESC", True, (198,1,1)) 
        text4Rect = text4.get_rect()
        text4Rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2)+150)
        screen.blit(text4,text4Rect) 

    # draw the enemy
    pygame.draw.rect(screen, [30, 30, 30], [x1, 350, 50, 50], 0)
    for enemy in enemies:
        enemy.draw()

        
    # draw the player if the game is still running
    for enemy in enemies:
        if enemy.loss == False:
            screen.blit(player.surf,player.rect)

    # Load everything
    pygame.display.flip()
