import pygame
import random
import os
import sys


pygame.init()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SILVER = (192, 192, 192)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Adresář pro obrázky
img_folder = os.path.join(os.path.dirname(__file__), 'img')

# Třída reprezentující hráče
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("IMG/potter-icon.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 8
        self.lives = 3

    def update(self):
        # Pohyb hráče
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        # Omezí pohyb hráče do hranic okna
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

# Třída reprezentující minci
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("IMG/koin.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(3, 7)

    def update(self):
        # Pohyb mince dolů po obrazovce
        self.rect.y += self.speedy
        # Pokud mince opustí dolní hranici obrazovky, resetuje se na náhodné pozici
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(3, 7)

# Třída reprezentující nepřátelský objekt
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("IMG/mozkomor-zluty.ico").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(3, 7)

    def update(self):
        # Pohyb nepřátelského objektu dolů po obrazovce
        self.rect.y += self.speedy
        # Pokud nepřátelský objekt opustí dolní hranici obrazovky, resetuje se na náhodné pozici
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(3, 7)

# Inicializace okna
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Pygame Game")

# Načtení obrázků
background = pygame.image.load("IMG/bg-dementors.png").convert()
background_rect = background.get_rect()

# Načtení fontu
font = pygame.font.Font(None, 36)

# Vytvoření hráče, mincí a nepřátelských objektů
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

coins = pygame.sprite.Group()
for _ in range(8):
    coin = Coin()
    all_sprites.add(coin)
    coins.add(coin)

enemies = pygame.sprite.Group()
for _ in range(15):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Hlavní smyčka hry
running = True
clock = pygame.time.Clock()
score = 0

def reset_game():
    player.lives = 3
    global score
    score = 0
    all_sprites.empty()
    all_sprites.add(player)
    for _ in range(10):
        coin = Coin()
        all_sprites.add(coin)
        coins.add(coin)
    for _ in range(5):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

# Hlavní smyčka hry
while running:
    clock.tick(60)

    # Události v hlavní smyčce
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if player.lives <= 0:
                reset_game()
                # Po stisknutí klávesy při zobrazení GAME OVER hra začne znovu

    # Aktualizace všech sprite objektů
    all_sprites.update()

    # Detekce kolize hráče s mincemi
    hits = pygame.sprite.spritecollide(player, coins, True)
    for hit in hits:
        score += 10
        # Generování nové mince po odstranění staré mince
        coin = Coin()
        all_sprites.add(coin)
        coins.add(coin)

    # Detekce kolize hráče s nepřátelskými objekty
    hits = pygame.sprite.spritecollide(player, enemies, True)
    if hits:
        player.lives -= 1
        if player.lives <= 0:
            player.lives = 0

    # Vykreslení pozadí
    screen.blit(background, background_rect)

    # Vykreslení všech sprite objektů
    all_sprites.draw(screen)

    # Vykreslení skóre a počtu životů
    score_text = font.render("Score: {}".format(score), True, WHITE)
    screen.blit(score_text, (10, 10))
    lives_text = font.render("Lives: {}".format(player.lives), True, WHITE)
    screen.blit(lives_text, (10, 50))

    # Pokud hráč ztratí všechny životy, zobrazíme obrazovku konečného skóre
    if player.lives <= 0:
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
        final_score_text = font.render("Final Score: {}".format(score), True, WHITE)
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        # Obnovení obrazovky po stisknutí libovolné klávesy
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False
                    reset_game()

    # Obnovení obrazovky
    pygame.display.flip()

pygame.quit()
sys.exit()