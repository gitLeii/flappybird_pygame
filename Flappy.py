import sys
import pygame
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 650))
    screen.blit(floor_surface, (floor_x_pos + 476, 650))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(680, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(680, random_pipe_pos - 210))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 630:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 700:
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, - bird_movement * 3, 1)
    return new_bird


def bird_anime():
    new_surface = bird_frames[bird_index]
    new_bird_rect = new_surface.get_rect(center=(100, bird_rect.centery))
    return new_surface, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(268, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render("Score: " + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(248, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render("High Score: " + str(int(score)), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(248, 150))
        screen.blit(high_score_surface, high_score_rect)


def update_score(_score, _high_score):
    if _score > high_score:
        _high_score = score
    return _high_score


pygame.mixer.pre_init(frequency=44100, size=8, channels=1, buffer=512)

pygame.init()
screen = pygame.display.set_mode((476, 730))
clock = pygame.time.Clock()
game_font = pygame.font.Font('FlappyBird_Python/04B_19.TTF', 40)

# ====== Game Variables ============
gravity = 0.20
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load("FlappyBird_Python/assets/background-day.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (476, 730))

floor_surface = pygame.image.load("FlappyBird_Python/assets/base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.image.load("FlappyBird_Python/assets/bluebird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("FlappyBird_Python/assets/bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("FlappyBird_Python/assets/bluebird-upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 350))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load("FlappyBird_Python/assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [300, 400, 550]

game_over_surface = pygame.transform.scale(pygame.image.load("FlappyBird_Python/assets/message.png"), (200, 400)).convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(238, 395))

flap_sound = pygame.mixer.Sound("FlappyBird_Python/sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("FlappyBird_Python/sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("FlappyBird_Python/sound/sfx_point.wav")
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                flap_sound.play()
                bird_movement = 0
                bird_movement -= 7
            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 350)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_anime()
# Background-----------------
    screen.blit(bg_surface, (0, 0))
    if game_active:
        # Bird------------------------
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes----------------------
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

# Floor-----------------------
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -476:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
