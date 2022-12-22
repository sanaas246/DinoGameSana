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

    def update(self):
        self.x += self.speed
        if self.x <= -50:
            self.teleport()
        
    def draw(self): # draw multiple rects
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.w, self.h], 0)
        
    def teleport(self):
        self.x = 800
        self.y = random.randint(100, 450)
        self.speed -= random.uniform(0,1)
        if self.speed <= -0.8:
            self.speed = -0.05
            if score == 1:
                print("score hit 2")
                # enemies.add(Enemy()) 
        print(self.speed)

    def scoring(self):
        if self.x == 1:
            score += 1

    def collision(self, xval, yval):
        # Collision Detection
        if yval >= self.y and yval + 25 <= self.y and xval >= self.x and xval <= self.x + 50:
            enemy.speed = 0
            loss = True 

            

# Player Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25,25))
        self.surf.fill((150,200,255))
        self.rect = self.surf.get_rect()

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
                score = 0
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

    # enemies update
    for enemy in enemies:
        enemy.collision(player.rect.x, player.rect.y)
        enemy.scoring()
        enemy.update()


        # # Collision Detection
        # if player.rect.y >= enemy.y and player.rect.y + 25 <= enemy.y and player.rect.x >= enemy.x and player.rect.x <= enemy.x + 50:
        #     enemy.speed = 0
        #     loss = True 



    # Pressing keys to move player
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

     

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # DRAWING
    # Fill the screen with black
    screen.fill((70,70,70)) 

    # End Game Screen
    text1 = font.render("YOU LOST", True, (255,51,51))
    text1Rect = text1.get_rect()
    text1Rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 50)

    text2 = font.render(f"Score: {score}", True, (0,245,50)) 
    text2Rect = text2.get_rect()
    text2Rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2))

    pygame.display.set_caption(str(score))

    # the ground
    pygame.draw.rect(screen, [100, 100, 100], [0, 550, 800, 100],0)

    # Add the highscore to json
    def addhs():
        users_json = json.dumps(userscores)
        file = open("users.txt", "w")
        file.write(users_json)
        file.close()

    # USER LOSES
    # the ending screen
    if loss == True:
        player.kill()
        screen.fill((0,0,0))
        for enemy in enemies:
            enemy.kill()
    
        # add the new highscore to the userscores json list 
        if score > userscores[0]:
            del(userscores[0])
            userscores.append(score)
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
        screen.blit(text4,text4Rect) # ADD RESTART FUNCTION 

    # draw the enemy
    pygame.draw.rect(screen, [30, 30, 30], [x1, 350, 50, 50], 0)
    for enemy in enemies:
        enemy.draw()

        
    # draw the player if the game is still running
    if loss == False:
        screen.blit(player.surf,player.rect)

    # Load everything
    pygame.display.flip()

# second enemies don't always show up
# second enemy collision not working 
# collision detection not always working 