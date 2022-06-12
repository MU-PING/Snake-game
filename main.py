import pygame
import time
import random
import sys

class Button:
    def __init__(self, display, text, width, height, pos, elevation):
        # Core
        self.display = display
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        
        # top rect
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = "#475F77"
        
		# bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'

        # text
        self.buttonText = pygame.font.Font('freesansbold.ttf',30)
        self.text_surf = self.buttonText.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        
    def draw(self):
        
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 
        
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
        
        pygame.draw.rect(self.display, self.bottom_color, self.bottom_rect, border_radius = 12)
        pygame.draw.rect(self.display, self.top_color, self.top_rect, border_radius = 12)
        self.display.blit(self.text_surf, self.text_rect)
        self.check_click()
        
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'
            
class Frames():
    
    def __init__(self, snake_position, apple_position):
        
        self.snake_position = snake_position
        self.apple_position = apple_position
        self.crashed = False
        self.score = 0
        
        # direction
        self.prev_button_direction = 1 
        self.button_direction = 1
        
class Snake_Game():
    
    def __init__(self, display, display_width, display_height, info_height):
        
        # initialize const 
        self.green = (61,145,64)
        self.red = (255,0,0)
        self.black = (0,0,0)
        self.ground_color = (200,200,200)
        self.info_color = (250,235,215)
        
        self.display = display
        self.display_width = display_width
        self.display_height = display_height
        self.info_height = info_height
        self.game_height = display_height - info_height
        self.game_width_index = display_width/10
        self.game_height_index = self.game_height/10
        self.ground_Rect = pygame.Rect(0, 0, display_width, self.game_height)
        self.info_Rect = pygame.Rect(0, self.game_height, display_width, info_height)

        # initialize Font
        self.infoText = pygame.font.Font('freesansbold.ttf',20)
        self.finalText = pygame.font.Font('freesansbold.ttf',35)
        
        self.display.fill(self.ground_color, self.ground_Rect)
        self.display.fill(self.info_color, self.info_Rect)

        
    def play(self):
        
        # initialize snake and apple
        snake_head = [self.display_width/2, (self.display_height-self.info_height)/2]
        snake_position = [snake_head, [snake_head[0]-10,250],[snake_head[0]-20,250]]
        apple_position = self.generate_apple()
        frames = Frames(snake_position, apple_position)
        
        button1 = Button(display, 'Click me', 200, 40, (0, 550) ,5)
        button1.draw()
        
        # frame
        while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()               # close window
                    sys.exit()                  # close program
                 
                # snake can't go back
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and frames.prev_button_direction != 1:
                        frames.button_direction = 0
                        
                    elif event.key == pygame.K_RIGHT and frames.prev_button_direction != 0:
                        frames.button_direction = 1
                        
                    elif event.key == pygame.K_UP and frames.prev_button_direction != 2:
                        frames.button_direction = 3
                        
                    elif event.key == pygame.K_DOWN and frames.prev_button_direction != 3:
                        frames.button_direction = 2
        
                    frames.prev_button_direction = frames.button_direction
                    
            self.generate_snake(frames)
            pygame.display.set_caption("Snake Game"+"  "+"Score: " + str(frames.score))
            
            if frames.crashed==True: break;
              
            self.display.fill(self.ground_color, self.ground_Rect)
            self.display.fill(self.info_color, self.info_Rect)
            self.display_apple(frames.apple_position)
            self.display_snake(frames.snake_position)
            self.display_info(frames.score)
            
            pygame.display.update()
            
            clock.tick(15)

    def generate_snake(self, frames):
        
        snake_head = frames.snake_position[0].copy()
        
        if frames.button_direction == 1:
            snake_head[0] += 10
        elif frames.button_direction == 0:
            snake_head[0] -= 10
        elif frames.button_direction == 2:
            snake_head[1] += 10
        elif frames.button_direction == 3:
            snake_head[1] -= 10
           
        # collision with apple -----------------------
        if snake_head == frames.apple_position:
            frames.apple_position = self.generate_apple()
            frames.snake_position.insert(0, list(snake_head))
            frames.score += 1
    
        else:
            frames.snake_position.insert(0, list(snake_head))
            frames.snake_position.pop()
        
        # collision with boundaries ----------------------------
        if snake_head[0] >= self.display_width or snake_head[0] < 0 or snake_head[1] >= self.game_height or snake_head[1] < 0:
            frames.crashed = True
            
        # collision with self ----------------------------
        if snake_head in frames.snake_position[1:]:
            frames.crashed = True

    def generate_apple(self):
        return [random.randrange(1, self.game_width_index)*10, random.randrange(1, self.game_height_index)*10]
        
    def display_snake(self, snake_position):
        for position in snake_position:
            pygame.draw.rect(display, self.green, pygame.Rect(position[0],position[1], 10, 10))
    
    def display_apple(self, apple_position):
            pygame.draw.rect(display, self.red, pygame.Rect(apple_position[0],apple_position[1], 10, 10))
    
    def display_info(self, score):
        score = 'Score:' + str(score)
        display.blit(self.infoText.render(score, True, self.black), (50, 550))
    
    def display_final_score(self, display_text, final_score):
        TextSurf = self.finalText.render(display_text, True, self.black)
        TextRect = TextSurf.get_rect()
        TextRect.center = ((self.display_width/2),(self.display_height/2))
        display.blit(TextSurf, TextRect)
        pygame.display.update()
    
if __name__ == "__main__":
    
    #initialize pygame modules   
    pygame.init() 
    
    # initialize Clock
    clock= pygame.time.Clock() 
    
    # display game window
    display_width = 500
    display_height = 600
    info_height = 100
    display = pygame.display.set_mode((display_width, display_height))

    game = Snake_Game(display, display_width, display_height, info_height)
    game.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()               # close window
                sys.exit()                  # close program