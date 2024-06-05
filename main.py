import pygame
from settings import *
from snake import Snake
from apple import Apple


class Main:
    def __init__(self):
        pygame.init()
        self.display_surface=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        #game objects
        self.bg_rects=[pygame.Rect((col+int(row%2==0))*CELL_SIZE,row*CELL_SIZE,CELL_SIZE,CELL_SIZE) for col in range(0,COLS,2) for row in range(ROWS)]
        self.clock = pygame.time.Clock()  # Create a clock object to control the frame rate
        self.score_font = pygame.font.Font(None, 36) 
        self.snake=Snake()
        self.apple=Apple(self.snake)
        self.update_event=pygame.event.custom_type()
        pygame.time.set_timer(self.update_event,200)
        self.game_active=False
        self.crunch_sound=pygame.mixer.Sound(join('.','audio','crunch.wav'))
        self.bg_music=pygame.mixer.Sound(join('.','audio','Arcade.ogg'))
        self.bg_music.set_volume(0.5)
        self.bg_music.play(-1)
        self.score = 0
    
    def draw_bg(self):
        for rect in (self.bg_rects):
            pygame.draw.rect(self.display_surface,DARK_GREEN,rect)
            
    
    def input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.snake.direction=pygame.Vector2(0,-1) if self.snake.direction.y!=1 else self.snake.direction
        if keys[pygame.K_DOWN]:
            self.snake.direction=pygame.Vector2(0,1) if self.snake.direction.y!=-1 else self.snake.direction
        if keys[pygame.K_LEFT]:
            self.snake.direction=pygame.Vector2(-1,0) if self.snake.direction.x!=1 else self.snake.direction
        if keys[pygame.K_RIGHT]:
            self.snake.direction=pygame.Vector2(1,0) if self.snake.direction.x!=-1 else self.snake.direction
    def collision(self):
        if self.snake.body[0]==self.apple.pos:
            self.snake.has_eaten==True
            self.snake.body.append(self.snake.body[-1])
            self.apple.set_pos()
            self.crunch_sound.play()
            self.score+=1
        #collision with walls
        if self.snake.body[0].x<0 or self.snake.body[0].x>=COLS or self.snake.body[0].y<0 or self.snake.body[0].y>=ROWS:
            self.game_over()
    def game_over(self):
        # self.display_surface.fill('black')  # Fill screen with black color
    #     box_width = 300
    #     box_height = 150
    #     box_x = (WINDOW_WIDTH - box_width) / 2
    #     box_y = (WINDOW_HEIGHT - box_height) / 2
    #     pygame.draw.rect(self.display_surface, 'white', (box_x, box_y, box_width, box_height))
    # # Render game over text with score
    #     game_over_text = self.score_font.render(f"Game Over! Your score: {self.score}", True, 'black')  
    #     game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH / 2, box_y + box_height / 2)) # Position game over text in the center
    #     self.display_surface.blit(game_over_text, game_over_rect)  # Blit game over text onto screen
        self.snake.reset()
        self.apple.set_pos()
        self.game_active=False
        self.score=0
        # pygame.display.flip()  # Update display
        # pygame.time.wait(1000)  #
        
    def draw_shadow(self):
        shadow_surf=pygame.Surface(self.display_surface.get_size())
        shadow_surf.fill((0,255,0))
        shadow_surf.set_colorkey((0,255,0))
        shadow_surf.blit(self.apple.scaled_surf,self.apple.scaled_rect.topleft+SHADOW_SIZE)
        for surf,rect in self.snake.draw_data:
            shadow_surf.blit(surf,rect.topleft+SHADOW_SIZE)
        mask=pygame.mask.from_surface(shadow_surf)
        mask.invert()
        shadow_surf=mask.to_surface()
        shadow_surf.set_colorkey((255,255,255))
        shadow_surf.set_alpha(SHADOW_OPACITY)
        
        
        self.display_surface.blit(shadow_surf,(0,0))
    def render_score(self):
        score_text = self.score_font.render(f"Score: {self.score}", True, 'white')  # Render the score text
        self.display_surface.blit(score_text, (10, 10)) 
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type==self.update_event and self.game_active:
                    self.snake.update()
                if event.type==pygame.KEYDOWN and not self.game_active:
                    self.game_active=True
                   
            self.display_surface.fill(LIGHT_GREEN)
            self.input()
            self.collision()
            self.draw_bg()
            self.draw_shadow()
            self.snake.draw()
            self.apple.draw()
            self.render_score()
            pygame.display.update()
            self.clock.tick(60)




Main().run()