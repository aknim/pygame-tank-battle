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
WHITE = (255, 255, 255)
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
        self.direction = 'up'
        self.bullets = []
        self.last_shot_time = 0
        self.shoot_delay = 500

    def move(self, keys):
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
            self.direction = 'up'
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
            self.direction = 'down'
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
            self.direction = 'left'
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            self.direction = 'right'

    def shoot(self):
        current_time = pygame.time.get_ticks() 
        if current_time - self.last_shot_time > self.shoot_delay:
            bullet = Bullet(self.x + self.width // 2 - 2, self.y + self.height // 2 - 5, self.direction)
            self.bullets.append(bullet) # Add bullet to the list
            self.last_shot_time = current_time
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        for bullet in self.bullets:
            bullet.move()
            bullet.draw()

    def check_bullet_out_of_bounds(self):
        self.bullets = [bullet for bullet in self.bullets if 
                        0 <= bullet.x <= SCREEN_WIDTH and 
                        0 <= bullet.y <= SCREEN_HEIGHT]

class EnemyTank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TANK_WIDTH
        self.height = TANK_HEIGHT
        self.color = ENEMY_COLOR
        self.speed = 3 # slower than the player
        self.direction = 'down'
        self.bullets = []

    def shoot(self):
        if random.randint(1, 60) == 1:
            bullet = Bullet(self.x + self.width // 2 - 2, self.y + self.height // 2 - 5, 'up')
            self.bullets.append(bullet)

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
        for bullet in self.bullets:
            bullet.move()
            bullet.draw()

    def check_bullet_out_of_bounds(self):
        self.bullets = [bullet for bullet in self.bullets if
                        0 <= bullet.x <= SCREEN_WIDTH 
                        and 0 <= bullet.y <= SCREEN_HEIGHT]

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.color = WHITE
        self.speed = 7
        self.direction = direction 

    def move(self):
        if self.direction == 'up':
            self.y -= self.speed
        elif self.direction == 'down':
            self.y += self.speed
        elif self.direction == 'left':
            self.x -= self.speed
        elif self.direction == 'right':
            self.x += self.speed

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

        if keys[pygame.K_SPACE]:
            player_tank.shoot()

        # Move and draw each enemy tank
        for enemy in enemy_tanks:
            # enemy.move_randomly()
            # enemy.move_towards_player(player_tank.x, player_tank.y, enemy_tanks)
            enemy.move_locally(player_tank.x, player_tank.y, enemy_tanks)  
            enemy.shoot()     
            enemy.draw()

        # Draw player tank
        player_tank.draw()

        # Remove bullets that are out of bounds
        player_tank.check_bullet_out_of_bounds()
        for enemy in enemy_tanks:
            enemy.check_bullet_out_of_bounds()

        pygame.display.update()
        clock.tick(60) # 60 frames per second

if __name__ == "__main__":
    main()
