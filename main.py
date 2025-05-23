import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 600))
    screen.blit(floor_surface, (floor_x_pos + 576, 600))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 200))
    return (bottom_pipe, top_pipe)


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 750:
            screen.blit(pipe_surface, pipe)
        else:
            flipped_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flipped_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            #death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom > 590:
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotate(bird, bird_movement * -2.5)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return (new_bird, new_bird_rect)


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(243, 550))
        screen.blit(high_score_surface, high_score_rect)


def update_high_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


# pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 750))
clock = pygame.time.Clock()
game_font = pygame.font.Font('assets/04b19.ttf', 40)

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Background
bg_surface = pygame.image.load('assets/background-night.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (576, 750))

# Floor
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (576, 200))
floor_x_pos = 0

# Bird
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 325))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Pipes
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [300, 400, 500]

game_over_surface = pygame.transform.scale(pygame.image.load('assets/message.png').convert_alpha(), (230, 300))
game_over_rect = game_over_surface.get_rect(center=(288, 325))

flap_sound = pygame.mixer.Sound('Sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('Sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('Sound/sfx_point.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 7
                #flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                # Reset everything
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 325)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            if len(pipe_list) > 10:
                pipe_list.pop(0)
                pipe_list.pop(0)
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index == 2:
                bird_index = 0
            else:
                bird_index += 1

            (bird_surface, bird_rect) = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird logic
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipe logic
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score logic

        score += 0.01
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_high_score(score, high_score)
        score_display('game_over')

    # Floor logic
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
