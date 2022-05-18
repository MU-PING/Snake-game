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
        self.text_surf = buttonText.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        
    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 
        
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
        
        pygame.draw.rect(self.display, self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(self.display, self.top_color, self.top_rect,border_radius = 12)
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
   
def collision_with_apple(apple_position, score):#如果與蘋果碰撞，產生新的蘋果，並分數加1
    apple_position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
    score += 1
    return apple_position, score

def collision_with_boundaries(snake_head): #判斷是否與邊界
    if snake_head[0]>=500 or snake_head[0]<0 or snake_head[1]>=500 or snake_head[1]<0 :
        return 1
    else:
        return 0

def collision_with_self(snake_position): #判斷是否與自己碰撞
    snake_head = snake_position[0]
    if snake_head in snake_position[1:]:
        return 1
    else:
        return 0
    

def is_direction_blocked(snake_position):#判斷是否死亡
    snake_head = snake_position[0]
    if collision_with_boundaries(snake_head) == 1 or collision_with_self(snake_position) == 1:
        return 1
    else:
        return 0

def generate_snake(snake_head, snake_position, apple_position, button_direction, score):
    crashed = False
    
    if button_direction == 1:
        snake_head[0] += 10
    elif button_direction == 0:
        snake_head[0] -= 10
    elif button_direction == 2:
        snake_head[1] += 10
    elif button_direction == 3:
        snake_head[1] -= 10
    else:
        pass
        
    if snake_head == apple_position:
        apple_position, score = collision_with_apple(apple_position, score)
        snake_position.insert(0,list(snake_head))

    else:
        snake_position.insert(0,list(snake_head))
        snake_position.pop()
    
    if is_direction_blocked(snake_position) == 1:
            crashed = True
            
    return snake_position, apple_position, score, crashed

def display_snake(snake_position):
    for position in snake_position:
        pygame.draw.rect(display, green, pygame.Rect(position[0],position[1],10,10))

def display_apple(apple_position):
        pygame.draw.rect(display, red, pygame.Rect(apple_position[0],apple_position[1],10,10))


def play_game(snake_head, snake_position, apple_position, button_direction, score):
    crashed = False
    prev_button_direction = 1 # snake can't go back
    button_direction = 1
    
    button1 = Button(display, 'Click me', 200, 40, (0, 510) ,5)
    
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()               # close window
                sys.exit()                  # close program
             
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and prev_button_direction != 1:
                    button_direction = 0
                elif event.key == pygame.K_RIGHT and prev_button_direction != 0:
                    button_direction = 1
                elif event.key == pygame.K_UP and prev_button_direction != 2:
                    button_direction = 3
                elif event.key == pygame.K_DOWN and prev_button_direction != 3:
                    button_direction = 2
                else:
                    button_direction = button_direction
    
        snake_position, apple_position, score, crashed = generate_snake(snake_head, snake_position, apple_position, button_direction, score)
        pygame.display.set_caption("Snake Game"+"  "+"SCORE: " + str(score))
        
        if crashed==True: break;
        
        display.fill(ground_color, pygame.Rect(0, 0, 500, 500))
        display.fill(info_color, pygame.Rect(0, 500, 500, 100))
        button1.draw()
        display_apple(apple_position)
        display_snake(snake_position)
        display_info(score)
        pygame.display.update()
        prev_button_direction = button_direction
        
        clock.tick(20)
        
    return score

def display_info(score):
    score = 'Score:' + str(score)
    display.blit(infoText.render(score, True, black), (0, 500))

def display_final_score(display_text, final_score):
    TextSurf = finalText.render(display_text, True, black)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((display_width/2),(display_height/2))
    display.blit(TextSurf, TextRect)
    pygame.display.update()
    
if __name__ == "__main__":
    
    #initialize pygame modules   
    pygame.init() 
    
    # initialize const 
    green = (61,145,64)
    red = (255,0,0)
    black = (0,0,0)
    
    # initialize required parameters
    display_width = 500
    display_height = 600
    ground_color = (200,200,200)
    info_color = (250,235,215)
    infoText = pygame.font.Font('freesansbold.ttf',20)
    finalText = pygame.font.Font('freesansbold.ttf',35)
    buttonText = pygame.font.Font('freesansbold.ttf',30)
    clock=pygame.time.Clock() 
    
    snake_head = [250,250]
    snake_position = [[250,250],[240,250],[230,250]]
    apple_position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
    snake_score = 0

    # display game window
    display = pygame.display.set_mode((display_width,display_height))
    
    display.fill(ground_color, pygame.Rect(0, 0, 500, 500))
    display.fill(info_color, pygame.Rect(0, 500, 500, 100))
    final_score = play_game(snake_head, snake_position, apple_position, 1, snake_score)

    display_text = 'Your Score is: ' + str(final_score)
    display_final_score(display_text, final_score)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()               # close window
                sys.exit()                  # close program