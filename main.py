import pygame
import random

# globale Variable for game window
window_heigth = 800
window_width = 600

# generate window for frame
window = pygame.display.set_mode((window_width, window_heigth))
framespersecond = 60
elevation = window_heigth * 0.8


# bird variables for game
bird_position = (window_width // 4, window_heigth // 1.9)
bird_velocity = 0
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
bird_image = pygame.image.load("images/bird.png")
pipe_image = pygame.image.load("images/pipe.png")
brick_texture = pygame.image.load("images/texture.png")
pygame.font.init()
font = pygame.font.SysFont("Arial", 30)  # None uses the default font, 55 is font size

# scale images for game - size wasn't correct
background_image_upscaled = pygame.transform.scale(
    background_image,
    (background_image.get_width() * 6, background_image.get_height() * 6),
)
bird_image_downscaled = pygame.transform.scale(
    bird_image,
    (bird_image.get_width() * 0.6, bird_image.get_height() * 0.6),
)


if __name__ == "__main__":  # aus geekforgeeks
    # For initializing modules of pygame library
    pygame.init()
    framespersecond_clock = pygame.time.Clock()

# Initialize scoring variables
score = 0
pipe_passed = False

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
while running:
    frame_count += 1
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -6  # birds upward speed

    # Update game state
    bird_position = (
        bird_position[0],
        bird_position[1] + bird_velocity,
    )

    # transform into rect, to make collision detection simpler
    bird_rect = pygame.Rect(
        bird_position[0],
        bird_position[1],
        bird_image_downscaled.get_width(),
        bird_image_downscaled.get_height(),
    )
    # collision detection
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            running = False
            show_crash_screen = True

    bird_velocity += 0.25  # bird drops each frame

    if bird_position[1] < 0:
        bird_position: (bird_position[0], 0)
    elif bird_position[1] > window_heigth:
        running = False

    # Check if bird passed the pipe to update score
    for pipe in pipes:
        if pipe[0] + pipe_width < bird_position[0] and not pipe_passed:
            score += 1
            pipe_passed = True

    # Reset pipe_passed when a new pipe is generated
    if frame_count % spawn_pipe_every == 0:
        pipe_passed = False

    # pipe spawning
    if frame_count % spawn_pipe_every == 0:
        top_pipe_height = random.randint(150, window_heigth - pipe_gap - 50)
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
        bird_image_downscaled, bird_position
    )  # bird position ist nicht in der mitte Sven fragen
    window.blit(pipe_image, (0, elevation))

    # draw pipes
    for pipe in pipes:
        pygame.draw.rect(window, (128, 128, 128), pipe)

    # Update the display
    pygame.display.flip()

    # Display Score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    # Update the display only once per frame
    pygame.display.flip()

    framespersecond_clock.tick(framespersecond)


# Quit pygame when the loop ends
pygame.quit()
