import pygame

# globale Variable for game window
window_heigth = 600
window_width = 400

# generate window for frame
window = pygame.display.set_mode((window_width, window_heigth))
framespersecond = 60
pipe_image = "images/pipe.png"
background_image = "images/background.png"
bird_image = "images/bird.png"


if __name__ == "__main__":  # aus geekforgeeks
    # For initializing modules of pygame library
    pygame.init()
    framepersecond_clock = pygame.time.Clock()