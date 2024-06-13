import pygame
import neat
import os
import pickle
from settings import *
from snake import Snake
from apple import Apple

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_rects = [pygame.Rect((col + int(row % 2 == 0)) * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE) 
                         for col in range(0, COLS, 2) for row in range(ROWS)]
        self.clock = pygame.time.Clock()
        self.score_font = pygame.font.Font(None, 36)
        self.snake = Snake()
        self.apple = Apple(self.snake)
        self.update_event = pygame.event.custom_type()
        pygame.time.set_timer(self.update_event, 300)  # Adjust timer for smooth movement
        self.game_active = False
        self.crunch_sound = pygame.mixer.Sound(os.path.join('.', 'audio', 'crunch.wav'))
        self.bg_music = pygame.mixer.Sound(os.path.join('.', 'audio', 'Arcade.ogg'))
        self.bg_music.set_volume(0)
        self.bg_music.play(-1)
        self.score = 0

    def draw_bg(self):
        for rect in self.bg_rects:
            pygame.draw.rect(self.display_surface, DARK_GREEN, rect)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.snake.direction = pygame.Vector2(0, -1) if self.snake.direction.y != 1 else self.snake.direction
        if keys[pygame.K_DOWN]:
            self.snake.direction = pygame.Vector2(0, 1) if self.snake.direction.y != -1 else self.snake.direction
        if keys[pygame.K_LEFT]:
            self.snake.direction = pygame.Vector2(-1, 0) if self.snake.direction.x != 1 else self.snake.direction
        if keys[pygame.K_RIGHT]:
            self.snake.direction = pygame.Vector2(1, 0) if self.snake.direction.x != -1 else self.snake.direction

    def collision(self):
        if self.snake.body[0] == self.apple.pos:
            self.snake.has_eaten = True
            self.snake.body.append(self.snake.body[-1])
            self.apple.set_pos()
            self.crunch_sound.play()
            self.score += 1
        if self.snake.body[0].x < 0 or self.snake.body[0].x >= COLS or self.snake.body[0].y < 0 or self.snake.body[0].y >= ROWS:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.apple.set_pos()
        self.game_active = False
        self.score = 0

    def draw_shadow(self):
        shadow_surf = pygame.Surface(self.display_surface.get_size())
        shadow_surf.fill((0, 255, 0))
        shadow_surf.set_colorkey((0, 255, 0))
        shadow_surf.blit(self.apple.scaled_surf, self.apple.scaled_rect.topleft + SHADOW_SIZE)
        for surf, rect in self.snake.draw_data:
            shadow_surf.blit(surf, rect.topleft + SHADOW_SIZE)
        mask = pygame.mask.from_surface(shadow_surf)
        mask.invert()
        shadow_surf = mask.to_surface()
        shadow_surf.set_colorkey((255, 255, 255))
        shadow_surf.set_alpha(SHADOW_OPACITY)
        self.display_surface.blit(shadow_surf, (0, 0))

    def render_score(self):
        score_text = self.score_font.render(f"Score: {self.score}", True, 'white')
        self.display_surface.blit(score_text, (10, 10))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == self.update_event and self.game_active:
                    self.snake.update()
                if event.type == pygame.KEYDOWN and not self.game_active:
                    self.game_active = True

            self.display_surface.fill(LIGHT_GREEN)
            self.input()
            self.collision()
            self.draw_bg()
            self.draw_shadow()
            self.snake.draw()
            self.apple.draw()
            self.render_score()
            pygame.display.update()
            self.clock.tick(30)  # Lower the FPS to 30 for smoother gameplay

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        game = Main()
        game.game_active = True

        run = True
        while run and game.game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Calculate normalized inputs
            horizontal_distance = (game.apple.pos.x - game.snake.body[0].x) / COLS
            vertical_distance = (game.apple.pos.y - game.snake.body[0].y) / ROWS

            # Feed inputs to the neural network
            inputs = [horizontal_distance, vertical_distance]
            output = net.activate(inputs)

            # Interpret output to determine snake movement
            max_value = max(output)
            index = output.index(max_value)

            if index == 0 and game.snake.direction != pygame.Vector2(1, 0):
                game.snake.direction = pygame.Vector2(-1, 0)  # Move left
            elif index == 1 and game.snake.direction != pygame.Vector2(-1, 0):
                game.snake.direction = pygame.Vector2(1, 0)  # Move right
            elif index == 2 and game.snake.direction != pygame.Vector2(0, 1):
                game.snake.direction = pygame.Vector2(0, -1)  # Move up
            elif index == 3 and game.snake.direction != pygame.Vector2(0, -1):
                game.snake.direction = pygame.Vector2(0, 1)  # Move down

            # Update game state
            game.collision()
            game.snake.update()

            if game.snake.body[0] in game.snake.body[1:] or game.snake.body[0].x < 0 or game.snake.body[0].x >= COLS or game.snake.body[0].y < 0 or game.snake.body[0].y >= ROWS:
                run = False

            genome.fitness += 1

            # Render game
            game.display_surface.fill(LIGHT_GREEN)
            game.draw_bg()
            game.draw_shadow()
            game.snake.draw()
            game.apple.draw()
            game.render_score()
            pygame.display.update()
            game.clock.tick(30)  # Adjust the tick rate to match the game's FPS

def run_neat(config_file):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)

    with open('winner.pkl', 'wb') as output:
        pickle.dump(winner, output, 1)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run_neat(config_path)
