import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coleta de Estrelas")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configurações do personagem
PLAYER_SIZE = 50
PLAYER_COLOR = (0, 0, 255)
player_pos = [WIDTH // 2, HEIGHT - 2 * PLAYER_SIZE]
player_speed = 5

# Configurações das estrelas
STAR_SIZE = 30
STAR_COLOR = (255, 223, 0)
stars = []
star_spawn_time = 30
star_counter = 0

# Configurações dos inimigos
ENEMY_SIZE = 50
ENEMY_COLOR = (255, 0, 0)
enemies = []
enemy_spawn_time = 50
enemy_counter = 0

# Pontuação
score = 0
font = pygame.font.SysFont("monospace", 35)

# Função para desenhar o jogador
def draw_player(position):
    pygame.draw.rect(WIN, PLAYER_COLOR, (position[0], position[1], PLAYER_SIZE, PLAYER_SIZE))

# Função para desenhar estrelas
def draw_stars(stars):
    for star in stars:
        pygame.draw.rect(WIN, STAR_COLOR, (star[0], star[1], STAR_SIZE, STAR_SIZE))

# Função para desenhar inimigos
def draw_enemies(enemies):
    for enemy in enemies:
        pygame.draw.rect(WIN, ENEMY_COLOR, (enemy[0], enemy[1], ENEMY_SIZE, ENEMY_SIZE))

# Função para atualizar a posição dos objetos
def update_positions(objects, speed):
    for obj in objects:
        obj[1] += speed

# Função para detectar colisões
def detect_collision(player, obj):
    p_x, p_y = player[0], player[1]
    o_x, o_y = obj[0], obj[1]
    if (o_x >= p_x and o_x < (p_x + PLAYER_SIZE)) or (p_x >= o_x and p_x < (o_x + STAR_SIZE)):
        if (o_y >= p_y and o_y < (p_y + PLAYER_SIZE)) or (p_y >= o_y and p_y < (o_y + STAR_SIZE)):
            return True
    return False

# Loop principal do jogo
run = True
clock = pygame.time.Clock()

while run:
    clock.tick(30)
    WIN.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Movimento do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - PLAYER_SIZE:
        player_pos[0] += player_speed

    # Spawn de estrelas
    if star_counter == star_spawn_time:
        star_x = random.randint(0, WIDTH - STAR_SIZE)
        stars.append([star_x, 0])
        star_counter = 0
    star_counter += 1

    # Spawn de inimigos
    if enemy_counter == enemy_spawn_time:
        enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
        enemies.append([enemy_x, 0])
        enemy_counter = 0
    enemy_counter += 1

    # Atualizar posições
    update_positions(stars, 5)
    update_positions(enemies, 7)

    # Checar colisões com estrelas
    for star in stars[:]:
        if detect_collision(player_pos, star):
            stars.remove(star)
            score += 1

    # Checar colisões com inimigos
    for enemy in enemies[:]:
        if detect_collision(player_pos, enemy):
            run = False

    # Desenhar elementos na tela
    draw_player(player_pos)
    draw_stars(stars)
    draw_enemies(enemies)

    # Desenhar pontuação
    score_text = font.render("Score: {}".format(score), 1, BLACK)
    WIN.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
