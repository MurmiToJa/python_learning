import pygame
import random
import math
import time

class Ball:
    def __init__(self, center, radius_circle, initial_radius, speed, growth, max_radius, color, max_speed, circle_border_thickness):
        self.center = center
        self.radius_circle = radius_circle
        self.radius = initial_radius
        self.speed = speed
        self.growth = growth
        self.max_radius = max_radius
        self.color = color
        self.max_speed = max_speed
        self.angle = random.uniform(0, 2 * math.pi)
        self.start_distance_from_edge = 30
        self.circle_border_thickness = circle_border_thickness
        self.x, self.y = self._random_start_position()
        self.growth_delay = 0
        self.bounced_this_frame = False 

    def _random_start_position(self):
        angle = random.uniform(0, 2 * math.pi)
        safe_distance = self.start_distance_from_edge + self.radius
        x = self.center[0] + math.cos(angle) * (self.radius_circle - safe_distance - self.circle_border_thickness)
        y = self.center[1] + math.sin(angle) * (self.radius_circle - safe_distance - self.circle_border_thickness)
        return x, y

    def random_color(self, exclude_color):
        while True:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if color != exclude_color:
                return color

    def calculate_new_position(self):
        velocity_x = math.cos(self.angle) * self.speed
        velocity_y = math.sin(self.angle) * self.speed

        current_speed = math.sqrt(velocity_x**2 + velocity_y**2)
        if current_speed > self.max_speed:
            scale = self.max_speed / current_speed
            velocity_x *= scale
            velocity_y *= scale
        
        self.x += velocity_x
        self.y += velocity_y
        self.bounced_this_frame = False 

    def distance_to_center(self):
        return math.sqrt((self.x - self.center[0]) ** 2 + (self.y - self.center[1]) ** 2)

    def bounce(self):
        if self.bounced_this_frame: 
            return
        
        dist_to_center = self.distance_to_center()
        if dist_to_center + self.radius >= self.radius_circle:
            self.bounced_this_frame = True

            normal_x = (self.x - self.center[0]) / dist_to_center
            normal_y = (self.y - self.center[1]) / dist_to_center

            # Oblicz wektor prędkości
            velocity_x = math.cos(self.angle) * self.speed
            velocity_y = math.sin(self.angle) * self.speed

            dot_product = velocity_x * normal_x + velocity_y * normal_y
            velocity_x -= 2 * dot_product * normal_x
            velocity_y -= 2 * dot_product * normal_y

            self.angle = math.atan2(velocity_y, velocity_x)
            
            self.angle += random.uniform(-0.1, 0.1)

            self.growth_delay = 10

            self.x += math.cos(self.angle) * self.radius * 0.1
            self.y += math.sin(self.angle) * self.radius * 0.1
    
    def update(self):
        if self.growth_delay > 0:
            self.growth_delay -= 1
        else: 
            if self.radius + self.growth <= self.max_radius:
               self.radius += self.growth
               self.color = self.random_color((255, 255, 255))


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 800
        self.RADIUS_CIRCLE = 300
        self.BALL_INITIAL_RADIUS = 10
        self.BALL_GROWTH = 2
        self.MAX_BALL_RADIUS = self.RADIUS_CIRCLE * 0.3
        self.BALL_SPEED = 5
        self.MAX_BALL_SPEED = 10
        self.FPS = 60
        self.CIRCLE_BORDER_THICKNESS = 5

        # Kolory
        self.OUTSIDE_COLOR = (39, 39, 39)  # #272727
        self.INSIDE_COLOR = (47, 47, 47)  # #2f2f2f
        self.CIRCLE_BORDER_COLOR = (255, 182, 51)  # #ffb633

        # Tworzenie okna
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Bouncing Ball in Circle")

        # Pozycja środka okręgu
        self.CENTER = (self.WIDTH // 2, self.HEIGHT // 2)

        # Utwórz kulkę
        self.ball = Ball(self.CENTER, self.RADIUS_CIRCLE, self.BALL_INITIAL_RADIUS, self.BALL_SPEED, self.BALL_GROWTH, self.MAX_BALL_RADIUS, (255,255,255), self.MAX_BALL_SPEED, self.CIRCLE_BORDER_THICKNESS)

        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.OUTSIDE_COLOR)

            pygame.draw.circle(self.screen, self.INSIDE_COLOR, self.CENTER, self.RADIUS_CIRCLE)
            pygame.draw.circle(self.screen, self.CIRCLE_BORDER_COLOR, self.CENTER, self.RADIUS_CIRCLE, self.CIRCLE_BORDER_THICKNESS)

            self.ball.calculate_new_position()
            self.ball.bounce()
            self.ball.update()

            self.ball.draw(self.screen)

            pygame.display.flip()

            self.clock.tick(self.FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()