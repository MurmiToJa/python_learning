import pygame

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.inner_color = pygame.Color("#2f2f2f")
        self.border_color = pygame.Color("#ffb633")

    def draw(self, screen):
        pygame.draw.circle(screen, self.inner_color, self.center, self.radius)
        pygame.draw.circle(screen, self.border_color, self.center, self.radius, 3)