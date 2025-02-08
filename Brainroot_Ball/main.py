import pygame
import sys
from circle import Circle
from ball import Ball

def main():
    pygame.init()
    screen_width, screen_height = 800, 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Kulka w kole")
    clock = pygame.time.Clock()

    circle_radius = 300
    circle_center = (screen_width // 2, screen_height // 2)
    
    circle = Circle(circle_center, circle_radius)
    ball = Ball(circle)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((39, 39, 39)) 
        
        circle.draw(screen)
        ball.update()
        ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

        if ball.size >= circle_radius * 0.3:
            running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()