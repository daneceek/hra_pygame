import pygame
import random
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SILVER = (192, 192, 192)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("IMG/pngegg.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 8
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("IMG/koin.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(3, 7)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("IMG/duch.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(self.rect.width, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)

class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(['life', 'speed', 'double points'])
        self.image = pygame.image.load("IMG/luckyblock.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-1000, -600)
        self.speedy = random.randint(3, 7)
        self.double_points = False
        self.start_time = pygame.time.get_ticks()
        self.show_text = False
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()  

    def apply_bonus(self, player):
        if self.type == 'speed':
            player.speed += 4
            self.start_time = pygame.time.get_ticks()  
        elif self.type == "life":
            self.start_time = pygame.time.get_ticks()  
            player.lives += 1
        elif self.type == "double points":
            self.double_points = True
            self.start_time = pygame.time.get_ticks()
            
     
        
         
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the coins")
font = pygame.font.Font(None, 36)

background = pygame.image.load("IMG/bg-dementors.png").convert()
background_rect = background.get_rect()

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

bonuses = pygame.sprite.Group()
coins = pygame.sprite.Group()
for _ in range(3):
    coin = Coin()
    all_sprites.add(coin)
    coins.add(coin)

enemies = pygame.sprite.Group()
for _ in range(6):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

running = True
clock = pygame.time.Clock()
score = 0
last_bonus_time = pygame.time.get_ticks()
bonus_frequency = 30000

def reset_game():
    global score
    global now
    now = 0
    score = 0
    enemies.empty()
    player.rect.centerx = SCREEN_WIDTH // 2
    player.rect.bottom = SCREEN_HEIGHT - 10
    player.lives = 3
    player.speed = 8
    all_sprites.empty()
    all_sprites.add(player)
    for _ in range(3):
        coin = Coin()
        all_sprites.add(coin)
        coins.add(coin)
    for _ in range(6):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if player.lives <= 0:
                reset_game()

    all_sprites.update()

    
    now = pygame.time.get_ticks()
    if now - last_bonus_time > bonus_frequency:
        last_bonus_time = now
        bonus = Bonus()
        all_sprites.add(bonus)
        bonuses.add(bonus)
        
    hits = pygame.sprite.spritecollide(player, bonuses, True)
    for hit in hits:
        hit.apply_bonus(player)  
        bonus.show_text = True
        
    if player.speed != 8 and pygame.time.get_ticks() - bonus.start_time >= 15000:
        player.speed = 8
     
    hits = pygame.sprite.spritecollide(player, coins, True)
    for hit in hits:
        
        if "bonus" in locals():
            if bonus.double_points:
                if pygame.time.get_ticks() - bonus.start_time >= 20000:
                    score += 10
                    bonus.double_points = False
                else:
                    score += 20
            else:
                score += 10
        else:
            score += 10
        coin = Coin()
        all_sprites.add(coin)
        coins.add(coin)

    if ("bonus" in locals()):
        if bonus.show_text:
            if bonus.type == "speed":
                text = "Rychlost hrace zvysena na 15 sekund!"
            elif bonus.type == "life":
                text = "Zivot navic!"
            elif bonus.type == "double points":
                text = "Dvojnásobné skóre na 15 sekund!"
            font_bonus = pygame.font.Font('freesansbold.ttf', 32)
            text_message = font.render(text, True, WHITE)
            text_message_rect = text_message.get_rect()
            text_message_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text_message, text_message_rect)
            
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.lives -= 1
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        if player.lives <= 0:
            player.lives = 0

    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    
    if ("bonus" in locals()):
        if bonus.show_text:
            if bonus.type == "speed":
                text = "Rychlost hrace zvysena na 15 sekund!"
            elif bonus.type == "life":
                text = "Zivot navic!"
            elif bonus.type == "double points":
                text = "Dvojnasobne skore na 15 sekund!"
            font_bonus = pygame.font.Font('freesansbold.ttf', 32)
            text_message = font.render(text, True, WHITE)
            text_message_rect = text_message.get_rect()
            text_message_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text_message, text_message_rect)
            now_text = pygame.time.get_ticks()
            if pygame.time.get_ticks() - bonus.start_time >= 2000:
                bonus.show_text = False
            
            
    score_text = font.render("Skore: {}".format(score), True, WHITE)
    screen.blit(score_text, (10, 10))
    lives_text = font.render("Zivoty: {}".format(player.lives), True, WHITE)
    screen.blit(lives_text, (10, 50))

    if player.lives <= 0:
        game_over_text = font.render("KONEC HRY", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        final_score_text = font.render("Konečné skóre: {}".format(score), True, WHITE)
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        play_again_text = font.render("Stisknete jakoukoliv klavesu pro hrani znovu", True, RED)
        screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    waiting = False
                    reset_game()

    pygame.display.update()

pygame.quit()
sys.exit()