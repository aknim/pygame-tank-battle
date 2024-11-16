import pygame
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TANK_WIDTH = 40
TANK_HEIGHT = 40
TANK_COLOR = (0, 255, 0) # Green
BLACK = (0, 0, 0)

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Battle")

# Define the Player Tank class
class PlayerTank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TANK_WIDTH
        self.height = TANK_HEIGHT
        self.color = TANK_COLOR
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


# Main game loop
def main():
    clock = pygame.time.Clock()
    player_tank = PlayerTank(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    while True:
        screen.fill(BLACK)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check for player input
        keys = pygame.key.get_pressed()
        player_tank.move(keys)

        # Draw player tank
        player_tank.draw()

        pygame.display.update()
        clock.tick(60) # 60 frames per second

if __name__ == "__main__":
    main()
