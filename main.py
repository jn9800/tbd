import pygame
import random

pygame.mixer.init()

# globale Variable for game window
window_heigth = 800
window_width = 600

# generate window for frame
window = pygame.display.set_mode((window_width, window_heigth))
framespersecond = 60
elevation = window_heigth * 0.8


# dolphin variables for game
dolphin_position = (window_width // 4, window_heigth // 1.9)
dolphin_velocity = 0
started_flying = False

# pipe variables for game
spawn_pipe_every = 120
frame_count = 0
pipe_width = 80
pipe_gap = 220
pipe_speed = -4
pipes = []

# load images
background_image = pygame.image.load("images/background.png")
dolphin_image = pygame.image.load("images/dolphin.png")
pipe_image = pygame.image.load("images/pipe.png")
brick_texture = pygame.image.load("images/texture.png")

pygame.font.init()
font = pygame.font.SysFont("Arial", 30)  # None uses the default font, 55 is font size

# load sound
pygame.mixer.music.load("sound/Soliloquy.mp3")

# -1 means the music will loop indefinitely
pygame.mixer.music.play(-1)

# Set the volume (0.4 for half volume, for example)
pygame.mixer.music.set_volume(0.1)

# adding space bar sound
space_bar_sound = pygame.mixer.Sound("sound/bubbles.mp3")

# adjusting space bar sound volume
space_bar_sound.set_volume(0.1)


# scale images for game - size wasn't correct
background_image_upscaled = pygame.transform.scale(
    background_image,
    (background_image.get_width() * 6, background_image.get_height() * 6),
)
dolphin_image_downscaled = pygame.transform.scale(
    dolphin_image,
    (dolphin_image.get_width() * 0.6, dolphin_image.get_height() * 0.6),
)


# highscore function
def save_high_score(high_score):
    with open("highscore.txt", "w") as file:
        file.write(str(high_score))


def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


if __name__ == "__main__":  # aus geekforgeeks
    # For initializing modules of pygame library
    pygame.init()
    framespersecond_clock = pygame.time.Clock()
    high_score = load_high_score()


# Initialize scoring variables
score = 0
pipe_passed = False


# you have crashed display
def display_crash_screen(window, score, high_score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # exit function and restart game

        window.fill((0, 0, 0))
        crash_text = font.render("you crashed dawg", True, (255, 0, 0))
        score_text = font.render(f"Your Score: {score}", True, (255, 0, 0))
        restart_text = font.render("press space to restart", True, (255, 0, 0))
        high_score_text = font.render(
            f"Your high score: {high_score}", True, (255, 0, 0)
        )

        window.blit(crash_text, (window_width // 2 - 100, window_heigth // 2 - 50))
        window.blit(score_text, (window_width // 2 - 100, window_heigth // 2))
        window.blit(restart_text, (window_width // 2 - 100, window_heigth // 2 + 50))
        window.blit(
            high_score_text, (window_width // 2 - 100, window_heigth // 2 + 100)
        )

        pygame.display.flip()


# starting loop
running = True
while not started_flying:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (
                exit_button_x <= mouse_x <= exit_button_x + exit_button_width
                and exit_button_y <= mouse_y <= exit_button_y + exit_button_height
            ):
                running = False
                started_flying = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                started_flying = True

    # background
    window.fill((0, 0, 0))  # clears window

    window.blit(background_image_upscaled, (-20, -20))

    # textbox
    box_width, box_height = 400, 100  # You can adjust the size as needed
    box_x = (window_width - box_width) // 2
    box_y = (window_heigth - box_height) // 2
    pygame.draw.rect(window, (0, 0, 0), (box_x, box_y, box_width, box_height))

    text = font.render("Please press space to start", True, (120, 0, 0))
    text_rect = text.get_rect(center=(window_width // 2, window_heigth // 2))
    window.blit(text, text_rect)

    # exit button
    exit_button_width, exit_button_height = 200, 50
    exit_button_x = (window_width - exit_button_width) // 2
    exit_button_y = (window_heigth // 2) + 100

    pygame.draw.rect(
        window,
        (0, 0, 0),
        (exit_button_x, exit_button_y, exit_button_width, exit_button_height),
    )
    exit_text = font.render("Exit", True, (120, 0, 0))
    exit_text_rect = exit_text.get_rect(
        center=(
            exit_button_x + exit_button_width // 2,
            exit_button_y + exit_button_height // 2,
        )
    )
    window.blit(exit_text, exit_text_rect)

    pygame.display.flip()

# game loop - for gaming
running = True
show_crash_screen = False
while running:
    frame_count += 1
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dolphin_velocity = -6  # dolphins upward speed
                space_bar_sound.play()

    # Update game state
    dolphin_position = (
        dolphin_position[0],
        dolphin_position[1] + dolphin_velocity,
    )

    # transform into rect, to make collision detection simpler
    dolphin_rect = pygame.Rect(
        dolphin_position[0],
        dolphin_position[1],
        dolphin_image_downscaled.get_width(),
        dolphin_image_downscaled.get_height(),
    )
    # collision detection with pipes
    for pipe in pipes:
        if dolphin_rect.colliderect(pipe):
            running = False
            show_crash_screen = True

    # collison detection with top of screen
    if dolphin_rect.top <= 0:
        running = False
        show_crash_screen = True

    dolphin_velocity += 0.25  # dolphin drops each frame

    if dolphin_position[1] < 0:
        dolphin_position: (dolphin_position[0], 0)
    elif dolphin_position[1] > window_heigth:
        running = False

    # Check if dolphin passed the pipe to update score
    for pipe in pipes:
        if pipe[0] + pipe_width < dolphin_position[0] and not pipe_passed:
            score += 1
            pipe_passed = True

    # Reset pipe_passed when a new pipe is generated
    if frame_count % spawn_pipe_every == 0:
        pipe_passed = False

    # pipe spawning
    if frame_count % spawn_pipe_every == 0:
        top_pipe_height = random.randint(100, window_heigth - pipe_gap - 50)
        pipes.append([window_width, 0, pipe_width, top_pipe_height])
        bottom_pipe_height = window_heigth - top_pipe_height - pipe_gap
        pipes.append(
            [
                window_width,
                window_heigth - bottom_pipe_height,
                pipe_width,
                bottom_pipe_height,
            ]
        )

    for pipe in pipes:
        pipe[0] += pipe_speed

    pipes = [pipe for pipe in pipes if pipe[0] > -pipe_width]
    for i in range(len(pipes)):
        pipes[i] = pygame.Rect(pipes[i][0], pipes[i][1], pipe_width, pipes[i][3])

    # Render graphics
    window.fill((255, 255, 255))
    window.blit(background_image_upscaled, (-20, -20))
    window.blit(
        dolphin_image_downscaled, dolphin_position
    )  # dolphin position ist nicht in der mitte Sven fragen
    window.blit(pipe_image, (0, elevation))

    # draw pipes
    for pipe in pipes:
        pygame.draw.rect(window, (128, 128, 128), pipe)

    # Update the display
    pygame.display.flip()

    # Display Score
    score_text = font.render(f"Score: {score}", True, (255, 0, 0))
    window.blit(score_text, (10, 10))

    # Update the display only once per frame
    pygame.display.flip()

    framespersecond_clock.tick(framespersecond)

    if show_crash_screen:
        display_crash_screen(window, score, high_score)

        if score > high_score:
            high_score = score
            save_high_score(high_score)

        # now resetting game state
        running = True
        show_crash_screen = False
        score = 0
        pipes = []
        dolphin_position = (window_width // 4, window_heigth // 1.9)
        dolphin_velocity = 0


# Quit pygame when the loop ends
pygame.quit()
