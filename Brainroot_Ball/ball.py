# ball.py
import pygame
import random
import math

class Ball:
    def __init__(self, circle):
        self.circle = circle
        self.x = circle.center[0]
        self.y = circle.center[1]
        self.size = 10
        self.color = pygame.Color(random.randint(50, 255), 
                                  random.randint(50, 255), 
                                  random.randint(50, 255))
        self.speed = 10
        self.angle = random.uniform(0, 2 * math.pi)

    def update(self):
        new_x = self.x + self.speed * math.cos(self.angle)
        new_y = self.y + self.speed * math.sin(self.angle)

        max_allowed_distance = self.circle.radius - self.size

        distance_from_center = math.sqrt((new_x - self.circle.center[0])**2 + 
                                         (new_y - self.circle.center[1])**2)

        if distance_from_center >= max_allowed_distance:

            normal_x = new_x - self.circle.center[0]
            normal_y = new_y - self.circle.center[1]
            normal_length = math.sqrt(normal_x**2 + normal_y**2)
            
            normal_x /= normal_length
            normal_y /= normal_length

            angle_variation = random.uniform(-math.pi/4, math.pi/4)
            
            velocity_x = self.speed * math.cos(self.angle)
            velocity_y = self.speed * math.sin(self.angle)

            reflected_angle = math.atan2(
                velocity_y - 2 * (velocity_x * normal_x + velocity_y * normal_y) * normal_y,
                velocity_x - 2 * (velocity_x * normal_x + velocity_y * normal_y) * normal_x
            ) + angle_variation

            self.angle = reflected_angle
            self.color = pygame.Color(random.randint(50, 255), 
                                      random.randint(50, 255), 
                                      random.randint(50, 255))
        
            if self.size < self.circle.radius * 0.3:
                self.size += 2

            self.x = self.circle.center[0] + max_allowed_distance * math.cos(math.atan2(normal_y, normal_x))
            self.y = self.circle.center[1] + max_allowed_distance * math.sin(math.atan2(normal_y, normal_x))
        else:
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))