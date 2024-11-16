import pygame
import sys
import random

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TANK_WIDTH = 40
TANK_HEIGHT = 40

TANK_COLOR = (0, 255, 0) # Green
BLACK = (0, 0, 0)
ENEMY_COLOR = (255, 0, 0) # Red

ENEMY_COUNT = 5

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

class EnemyTank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TANK_WIDTH
        self.height = TANK_HEIGHT
        self.color = ENEMY_COLOR
        self.speed = 3 # slower than the player

    def move_randomly(self):
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up' and self.y > 0:
            self.y -= self.speed
        elif direction == 'down' and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
        elif direction == 'left' and self.x > 0:
            self.x -= self.speed
        elif direction == 'right' and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed

    def move_towards_player(self, player_x, player_y, enemy_tanks):
        # Avoid collision with other enemy tanks
        for enemy in enemy_tanks:
            if enemy != self: # Don't check collision with itself
                if abs(self.x - enemy.x) < 100 and abs(self.y - enemy.y) < 100:
                    if self.x < enemy.x:
                        self.x -= self.speed # move left
                    elif self.x > enemy.x:
                        self.x += self.speed # move right
                
                    if self.y < enemy.y:
                        self.y -= self.speed # move up
                    elif self.y > enemy.y:
                        self.y += self.speed # move down
                    return # exit if avoiding another empty tank

        if self.x < player_x:
            self.x += self.speed
        elif self.x > player_x:
            self.x -= self.speed

        if self.y < player_y:
            self.y += self.speed
        elif self.y > player_y:
            self.y -= self.speed

    def move_locally(self, player_x, player_y, enemy_tanks):
        if abs(self.x - player_x) < 150 and abs(self.y - player_y) < 150:
            self.move_towards_player(player_x, player_y, enemy_tanks)
        else:
            self.move_randomly()
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        

# Main game loop
def main():
    clock = pygame.time.Clock()
    player_tank = PlayerTank(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    enemy_tanks = [EnemyTank(random.randint(0, SCREEN_WIDTH - TANK_WIDTH), 
                            random.randint(0, SCREEN_HEIGHT - TANK_HEIGHT)) 
                            for _ in range(ENEMY_COUNT)]


    while True:
        screen.fill(BLACK)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check for player input
        keys = pygame.key.get_pressed()
        player_tank.move(keys)

        # Move and draw each enemy tank
        for enemy in enemy_tanks:
            # enemy.move_randomly()
            # enemy.move_towards_player(player_tank.x, player_tank.y, enemy_tanks)
            enemy.move_locally(player_tank.x, player_tank.y, enemy_tanks)       
            enemy.draw()

        # Draw player tank
        player_tank.draw()

        pygame.display.update()
        clock.tick(60) # 60 frames per second

if __name__ == "__main__":
    main()
