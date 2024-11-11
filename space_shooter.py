from turtle import clone
import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player
class Player:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = 5
        self.bullets = []
    
    def draw(self):
        pygame.draw.rect(window, WHITE, (self.x, self.y, self.width, self.height))
        for bullet in self.bullets:
            bullet.draw()
    
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed
    
    def shoot(self):
        bullet = Bullet(self.x + self.width//2, self.y)
        self.bullets.append(bullet)
    
    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)

# Bullet
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7
        self.radius = 3
    
    def draw(self):
        pygame.draw.circle(window, WHITE, (int(self.x), int(self.y)), self.radius)
    
    def move(self):
        self.y -= self.speed

# Enemy
class Enemy:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = random.randint(0, WIDTH - self.width)
        self.y = -self.height
        self.speed = random.uniform(1, 3)
    
    def draw(self):
        pygame.draw.rect(window, WHITE, (self.x, self.y, self.width, self.height))
    
    def move(self):
        self.y += self.speed
    
    def is_off_screen(self):
        return self.y > HEIGHT

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.score = 0
        self.game_over = False
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 60  # Frames between enemy spawns
        self.font = pygame.font.Font(None, 36)

    def spawn_enemy(self):
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            self.enemies.append(Enemy())
            self.enemy_spawn_timer = 0

    def check_collisions(self):
        # Check bullet-enemy collisions
        for enemy in self.enemies[:]:
            for bullet in self.player.bullets[:]:
                if (bullet.x > enemy.x and bullet.x < enemy.x + enemy.width and
                    bullet.y > enemy.y and bullet.y < enemy.y + enemy.height):
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
                    self.score += 10

        # Check player-enemy collisions
        for enemy in self.enemies:
            if (self.player.x < enemy.x + enemy.width and
                self.player.x + self.player.width > enemy.x and
                self.player.y < enemy.y + enemy.height and
                self.player.y + self.player.height > enemy.y):
                self.game_over = True

    def update(self):
        if not self.game_over:
            # Handle player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move("left")
            if keys[pygame.K_RIGHT]:
                self.player.move("right")

            # Update game elements
            self.player.update_bullets()
            self.spawn_enemy()
            
            # Update enemies
            for enemy in self.enemies[:]:
                enemy.move()
                if enemy.is_off_screen():
                    self.enemies.remove(enemy)
            
            self.check_collisions()

    def draw(self):
        window.fill(BLACK)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        window.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = self.font.render("Game Over! Press R to restart", True, WHITE)
            window.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))
        
        pygame.display.update()

    def reset(self):
        self.__init__()

def main():
    clock = pygame.time.Clock()
    game = Game()
    running = True

    while running:
        clock.tick(60)  # 60 FPS
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game.game_over:
                    game.player.shoot()
                elif event.key == pygame.K_r and game.game_over:
                    game.reset()

        game.update()
        game.draw()

    pygame.quit()

if __name__ == "__main__":
    main()