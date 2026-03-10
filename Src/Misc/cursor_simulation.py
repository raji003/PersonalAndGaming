import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Cursor Simulation")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Player settings
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5

# Generate random targets
num_targets = 5
targets = [[random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)] for _ in range(num_targets)]

# Function to calculate vector to target
def calculate_aim(player, target):
    dx = target[0] - player[0]
    dy = target[1] - player[1]
    distance = math.hypot(dx, dy)
    if distance == 0:
        return (0, 0)
    return (dx, dy)

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press handling for player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_pos[1] += player_speed

    # Draw targets and aiming vectors
    for t in targets:
        pygame.draw.circle(screen, RED, t, 10)
        # Draw vector line from player to target
        aim_dx, aim_dy = calculate_aim(player_pos, t)
        pygame.draw.line(screen, GREEN, player_pos, (player_pos[0]+aim_dx, player_pos[1]+aim_dy), 2)

    # Draw player
    pygame.draw.circle(screen, BLUE, (int(player_pos[0]), int(player_pos[1])), 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
