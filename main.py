import pygame

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

# load images
background_image = pygame.image.load("images/background.png")
bird_image = pygame.image.load("images/bird.png")
pipe_image = pygame.image.load("images/pipe.png")


# scale images for game - size wasn't correct
background_image_upscaled = pygame.transform.scale(
    background_image,
    (background_image.get_width() * 6, background_image.get_height() * 6),
)
bird_image_downscaled = pygame.transform.scale(
    bird_image,
    (bird_image.get_width() * 0.2, bird_image.get_height() * 0.2),
)


if __name__ == "__main__":  # aus geekforgeeks
    # For initializing modules of pygame library
    pygame.init()
    framepersecond_clock = pygame.time.Clock()

# Setting up font for display
    font = pygame.font.SysFont(None, 55)  # None uses the default font, 55 is font size
    text = font.render('Please press space to start', True, (255, 255, 255))  # 

# starting loop
running = True
while not started_flying:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                started_flying = True

        # Display the text
        window.fill((0, 255, 0))  # Fill screen with black
        window.blit(text, (50, window_heigth // 2))  # Adjust the position as needed
        pygame.display.flip()

# game loop - for gaming
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -2  # birds upward speed

    # Update game state
    bird_position = (
        bird_position[0],
        bird_position[1] + bird_velocity,
    )

    bird_velocity += 0.01  # bird drops each frame

    if bird_position[1] < 0:
        bird_position: (bird_position[0], 0)
    elif bird_position[1] > window_heigth:
        running = False

    # Render graphics
    window.fill((255, 255, 255))
    window.blit(background_image_upscaled, (-20, -20))
    window.blit(
        bird_image_downscaled, bird_position
    )  # bird position ist nicht in der mitte Sven fragen
    window.blit(pipe_image, (0, elevation))

    # Update the display
    pygame.display.flip()


# Quit pygame when the loop ends
pygame.quit()
