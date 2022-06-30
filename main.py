import pygame
import random
import sys

class Button:
    def __init__(self, display, text, width, height, pos, elevation, command):
        # Core
        self.display = display
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        
        # top rect
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = "#D26900"
        
		# bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'

        # text
        self.buttonText = pygame.font.Font('freesansbold.ttf', 18)
        self.text_surf = self.buttonText.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect()
        
        # listener
        self.command = command
        
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
                if self.pressed:
                    for fun in self.command:
                        fun()
                self.dynamic_elecation = self.elevation
                self.pressed = False

        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#D26900'
        
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
        
        # Const 
        self.green = (227, 229, 132)
        self.white = (255, 255, 255)
        
        self.display = display
        self.display_width = display_width
        self.game_height = display_height - info_height
        self.game_width_index = display_width/10
        self.game_height_index = self.game_height/10
        
        self.speedIndex = 0
        self.speedTexts = ["Slow", "Medium", "Fast"]
        self.speeds = [10, 20, 30]
        self.speedText = 'Slow'
        self.speed = 10
        
        self.mapIndex = 0
        self.mapTexts = ["Easy", "Medium", "Hard"]

        
        # Font
        self.infoText = pygame.font.Font('freesansbold.ttf', 20)
        self.finalText = pygame.font.Font('freesansbold.ttf', 64)
        
        # Image
        self.GrassUI = pygame.image.load("Icon//GrassUI.png")
        self.GrassUI.convert() # Increase drawing speed
        self.SnakeUI = pygame.image.load("Icon//SnakeUI.jpeg")
        self.SnakeUI.convert() # Increase drawing speed
        self.SnakeUI = pygame.transform.scale(self.SnakeUI, (display_width, info_height))
        
        self.RockUI = pygame.image.load("Icon//RockUI.png")
        self.RockUI.convert() 
        self.RockUI = pygame.transform.scale(self.RockUI, (20, 20))
        
        self.Tree1UI = pygame.image.load("Icon//Tree_ShortUI.png")
        self.Tree1UI.convert() 
        self.Tree1UI = pygame.transform.scale(self.Tree1UI, (20, 20))
        
        self.Tree2UI = pygame.image.load("Icon//Tree_UglyUI.png")
        self.Tree2UI.convert() 
        self.Tree2UI = pygame.transform.scale(self.Tree2UI, (20, 20))

        self.AppleUI = pygame.image.load("Icon//AppleUI.png")
        self.AppleUI.convert() 
        self.AppleUI = pygame.transform.scale(self.AppleUI, (20, 20))
        
        # Button
        self.buttonWidth = 80
        self.buttonHeight = 28
        self.pos = (info_height - 2 * self.buttonHeight) / 5
        self.start_position = (20, self.game_height + self.pos)
        self.level_position = (20, self.game_height + 2*self.pos + self.buttonHeight)
        self.map_position = (20, self.game_height + 3*self.pos + 2*self.buttonHeight)
        self.start_button = Button(self.display, 'START', self.buttonWidth, self.buttonHeight, self.start_position, 5, [self.countdown])
        self.level_button = Button(self.display, 'SPEED', self.buttonWidth, self.buttonHeight, self.level_position, 5, [self.choose_speed])
        self.map_button = Button(self.display, 'MAP', self.buttonWidth, self.buttonHeight, self.map_position, 5, [self.choose_map])

        # Text Position
        self.score_text_position = (40 + self.buttonWidth, self.start_position[1])
        self.speed_text_position = (40 + self.buttonWidth, self.level_position[1])
        self.map_text_position = (40 + self.buttonWidth, self.map_position[1])
        
        # Obstacle
        self.obstacle = []
        
        self.mainUI()
        
    def mainUI(self):
    
        # frame
        while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()               # close window
                    sys.exit()                  # close program
            
            self.display_background()
            self.start_button.draw() 
            self.level_button.draw()
            self.map_button.draw()
            self.display_info()
            
            pygame.display.update()
            
    def countdown(self):
        
        # frame
        time = 0
        num = 3
        countdown = str(num)
        
        while True:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit()               # close window
                    sys.exit()                  # close program
              
            self.display_background()
            self.display_info()
            
            if(time % 250 < 250):
                self.display_text(countdown)
                time += 1  
                
            if(time % 250 == 0):
                if(countdown == "Game Start"):
                    break
                num -= 1
                countdown = str(num)
                if(num == 0):
                    countdown = "Game Start"
                
            pygame.display.update()
            
        self.play()
        
    def play(self):
        
        # initialize snake and apple
        startX = self.display_width/2
        startY = self.game_height/2
        snake_position = [[startX, startY], [startX-10, startY],[startX-20, startY]]
        apple_position = self.generate_apple()
        frames = Frames(snake_position, apple_position)
        
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
            if frames.crashed==True: break;
            self.display_background()
            self.display_snake(frames.snake_position)
            self.display_apple(frames.apple_position)
            self.display_info()
            
            pygame.display.update()
            clock.tick(self.speed)
    
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
            frames.snake_position.insert(0, snake_head)
            frames.score += 1
    
        else:
            frames.snake_position.insert(0, snake_head)
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
            pygame.draw.rect(self.display, self.green, pygame.Rect(position[0],position[1], 10, 10))
    
    def display_apple(self, apple_position):
        self.display.blit(self.AppleUI, apple_position)
        
    def display_background(self):
        self.display.blit(self.GrassUI, (0, 0))
        self.display.blit(self.SnakeUI, (0, self.game_height))
        self.display.blit(self.RockUI, (20, 20))
        self.display.blit(self.RockUI, (240, 160))
        self.display.blit(self.RockUI, (160, 410))
        self.display.blit(self.RockUI, (180, 120))
        
        self.display.blit(self.Tree1UI, (280, 120))
        self.display.blit(self.Tree1UI, (380, 130))
        self.display.blit(self.Tree2UI, (120, 290))

    def display_info(self):
        
        # display score
        TextSurf = self.infoText.render("Score:  " + "0", True, self.white)
        self.display.blit(TextSurf, self.score_text_position)
        
        # display speed
        TextSurf = self.infoText.render("Speed:  " + self.speedText, True, self.white)
        self.display.blit(TextSurf, self.speed_text_position)
        
        # display map
        TextSurf = self.infoText.render("Map:  " + self.mapTexts[self.mapIndex], True, self.white)
        self.display.blit(TextSurf, self.map_text_position)
        
    def display_text(self, display_text):
        TextSurf = self.finalText.render(display_text, True, self.white)
        TextRect = TextSurf.get_rect()
        TextRect.center = ((self.display_width/2),(self.game_height/2))
        self.display.blit(TextSurf, TextRect)
        
    def choose_speed(self):
        self.speedIndex = (self.speedIndex + 1) % 3  
        self.speedText = self.speedTexts[self.speedIndex]
        self.speed = self.speeds[self.speedIndex]
          
    def choose_map(self):
        self.mapIndex = (self.mapIndex + 1) % 3

class Map():
    def __init__(self):
        pass
        
if __name__ == "__main__":
    
    #initialize pygame modules   
    pygame.init() 
    
    # initialize Clock
    clock= pygame.time.Clock() 
    
    # display game window
    display_width = 420
    display_height = 620
    info_height = 150
    
    # create the display surface object of specific dimension.
    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Snake Game v1.0')
    game = Snake_Game(display, display_width, display_height, info_height)
