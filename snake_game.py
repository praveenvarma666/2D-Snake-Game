import pygame
from pygame.math import Vector2
import sys
import random
import time

pygame.init()

# Dimensions of Game Screen
cell_size = 20
cell_no = 40
screen_width = cell_size * cell_no
screen_height = cell_size * cell_no

# Creating a Game Screen
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('SNAKE GAME')

# Ensures the game works at specified framerate
clock = pygame.time.Clock()
fps = 60

#Defining Font
score_font = pygame.font.Font(None,25)

# Defining colours
white = 255,255,255
black = 0,0,0
red = 255,0,0
green = 0,255,0
blue = 0,0,255

# Loading Fruit Images
apple_img = pygame.image.load('Snake Game/images/apple.png').convert_alpha()
apple_img = pygame.transform.scale(apple_img,(cell_size,cell_size))

# Creating Background Pattern
def bg_pattern():
    dark_color = (167,209,61)
    for row in range(cell_no):
        for col in range(cell_no):
            bg_rect = pygame.Rect(row*cell_size,col*cell_size,cell_size,cell_size)
            if row % 2 == 0:
                if col % 2 == 0:
                    pygame.draw.rect(screen,dark_color,bg_rect)
            else:
                if col % 2 != 0:
                    pygame.draw.rect(screen,dark_color,bg_rect)

# Fruit Class
class Fruit:
    def __init__(self):
        self.place_fruit()
        
    def draw(self):
        # Creating a rectangle for fruit
        fruit_rect = pygame.Rect(self.pos[0]*cell_size,self.pos[1]*cell_size,cell_size,cell_size)
        screen.blit(apple_img,fruit_rect)

    def place_fruit(self):
        pos_x = random.randint(0,cell_no -1)
        pos_y = random.randint(0,cell_no -1)
        self.pos = Vector2(pos_x,pos_y)
        # Random colour picker
        self.colour = random.choice([white,black,red,green,blue])
  
# Snake Class
class Snake:
    def __init__(self):
        self.body_parts = [Vector2(4,10),Vector2(3,10),Vector2(2,10)]
        self.direction = Vector2(1,0)
        self.new_part = False

        # Loading Snake Head Images
        self.head_right = pygame.image.load('Snake Game/images/right_head.png')
        self.head_right = pygame.transform.scale(self.head_right,(cell_size,cell_size))

        self.head_left = pygame.image.load('Snake Game/images/left_head.png')
        self.head_left = pygame.transform.scale(self.head_left,(cell_size,cell_size))

        self.head_up = pygame.image.load('Snake Game/images/up_head.png')
        self.head_up = pygame.transform.scale(self.head_up,(cell_size,cell_size))

        self.head_down = pygame.image.load('Snake Game/images/down_head.png')
        self.head_down = pygame.transform.scale(self.head_down,(cell_size,cell_size))

        # Loading Snake Tail Images
        self.tail_right = pygame.image.load('Snake Game/images/right_tail.png')
        self.tail_right = pygame.transform.scale(self.tail_right,(cell_size,cell_size))

        self.tail_left = pygame.image.load('Snake Game/images/left_tail.png')
        self.tail_left = pygame.transform.scale(self.tail_left,(cell_size,cell_size))

        self.tail_up = pygame.image.load('Snake Game/images/up_tail.png')
        self.tail_up = pygame.transform.scale(self.tail_up,(cell_size,cell_size))

        self.tail_down = pygame.image.load('Snake Game/images/down_tail.png')
        self.tail_down = pygame.transform.scale(self.tail_down,(cell_size,cell_size))

        # Loading Vertical Body Image
        self.body_vertical = pygame.image.load('Snake Game/images/vertical_body.png')
        self.body_vertical = pygame.transform.scale(self.body_vertical,(cell_size,cell_size))

        # Loading Horizontal Body Image
        self.body_horizontal = pygame.image.load('Snake Game/images/horizontal_body.png')
        self.body_horizontal = pygame.transform.scale(self.body_horizontal,(cell_size,cell_size))

        # Loading Turned Body Images
        self.turn_1 = pygame.image.load('Snake Game/images/turn_1.png')
        self.turn_1 = pygame.transform.scale(self.turn_1,(cell_size,cell_size))

        self.turn_2 = pygame.image.load('Snake Game/images/turn_2.png')
        self.turn_2 = pygame.transform.scale(self.turn_2,(cell_size,cell_size))

        self.turn_3 = pygame.image.load('Snake Game/images/turn_3.png')
        self.turn_3 = pygame.transform.scale(self.turn_3,(cell_size,cell_size))

        self.turn_4 = pygame.image.load('Snake Game/images/turn_4.png')
        self.turn_4 = pygame.transform.scale(self.turn_4,(cell_size,cell_size))

        # Loading Sounds
        self.crunch_sound = pygame.mixer.Sound('Snake Game/Sound/crunch_sound.wav')
        self.crunch_sound.set_volume(0.5)
        self.collision_sound = pygame.mixer.Sound('Snake Game/Sound/collision.wav')
        self.game_over_sound = pygame.mixer.Sound('Snake Game/Sound/game_over.wav')

    def draw(self):
        self.update_head_direction()
        self.update_tail_direction()
        time.sleep(0.10)
        for index,part in enumerate(self.body_parts):
            
            pos_x = part[0]*cell_size
            pos_y = part[1]*cell_size
            part_rect = pygame.Rect(pos_x,pos_y,cell_size,cell_size)
            if index == 0:
                screen.blit(self.head,part_rect)
            elif index == len(self.body_parts) - 1:
                screen.blit(self.tail,part_rect)
            else:
                prev_part = self.body_parts[index+1] - part
                next_part = self.body_parts[index-1] - part
                if prev_part.x == next_part.x:
                    screen.blit(self.body_vertical,part_rect)
                elif prev_part.y == next_part.y:
                    screen.blit(self.body_horizontal,part_rect)
                else:
                    if prev_part.y == 1 and next_part.x == -1 or next_part.y == 1 and prev_part.x == -1:
                        screen.blit(self.turn_1,part_rect)
                    if prev_part.y == 1 and next_part.x == 1 or next_part.y == 1 and prev_part.x == 1:
                        screen.blit(self.turn_2,part_rect)
                    if prev_part.y == -1 and next_part.x == 1 or next_part.y == -1 and prev_part.x == 1:
                        screen.blit(self.turn_3,part_rect)
                    if prev_part.y == -1 and next_part.x == -1 or next_part.y == -1 and prev_part.x == -1:
                        screen.blit(self.turn_4,part_rect)
                        
    def move(self):
        if self.new_part == True:
            body_copy = self.body_parts[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body_parts = body_copy[:]
            self.new_part = False
        else:
            body_copy = self.body_parts[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body_parts = body_copy[:]

    def add_part(self):
        self.new_part = True
    
    def update_head_direction(self):
        head_direction = self.body_parts[1] - self.body_parts[0]
        if head_direction == Vector2(-1,0):
            self.head = self.head_right
        if head_direction == Vector2(1,0):
            self.head = self.head_left
        if head_direction == Vector2(0,1):
            self.head = self.head_up
        if head_direction == Vector2(0,-1):
            self.head = self.head_down

    def update_tail_direction(self):
        tail_direction = self.body_parts[-2] - self.body_parts[-1]
        if tail_direction == Vector2(1,0):
            self.tail = self.tail_right
        if tail_direction == Vector2(-1,0):
            self.tail = self.tail_left
        if tail_direction == Vector2(0,-1):
            self.tail = self.tail_up
        if tail_direction == Vector2(0,1):
            self.tail = self.tail_down

    def eat_sound(self):
        self.crunch_sound.play()
    
    def Game_Over_Sound(self):
        self.collision_sound.play()
        time.sleep(0.5)
        self.game_over_sound.play()

    def reset(self):
        self.body_parts = [Vector2(4,10),Vector2(3,10),Vector2(2,10)]
        self.direction = Vector2(1,0)

# Score Board Class
class Score:
    def __init__(self):
        pass

    def score(self):
        score_text = str(len(snake.body_parts) - 3)
        score_surface = score_font.render(score_text,True,(56,74,12))
        score_x = cell_size*0 + 60
        score_y = cell_size*0 + 40
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple_img.get_rect(center = (score_rect.left-15,score_rect.centery-3))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top-2,apple_rect.width + score_rect.width+10,apple_rect.height+5)

        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple_img,apple_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2)
        

        
# Game Variables
snake = Snake()
fruit = Fruit()
score = Score()


# Game Loop
run = True
while run:
    
    # Checking for controllers 
    for event in pygame.event.get():
        # Closing the game using top right 'X' button
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Checking if movement buttons are pressed
        # Also checks for moving in opposite direction simultaneosly
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if snake.direction.y != 1:
                    snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if snake.direction.y != -1:
                    snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if snake.direction.x != -1:
                    snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if snake.direction.x != 1:
                    snake.direction = Vector2(-1,0)


    # Check for collision between snake head and fruit
    if fruit.pos == snake.body_parts[0]:
        # Replacing thee fruit
        fruit.place_fruit()
        # Adding new block to snake
        snake.add_part()
        # Playing eat sound
        snake.eat_sound()

    # Game Ending Conditions
    # Checks whether the snake collided with boundaries
    if not 0 <= snake.body_parts[0].x < cell_no or not 0 <= snake.body_parts[0].y < cell_no :
        snake.Game_Over_Sound()
        time.sleep(0.5)
        snake.reset()
    # Checks whether the snake collide with itself
    for part in snake.body_parts[1:]:
        if part == snake.body_parts[0]:
            snake.Game_Over_Sound()
            time.sleep(0.5)
            snake.reset()

    screen.fill(pygame.Color((175,215,70)))  

    bg_pattern()
    fruit.draw() 
    snake.draw()
    snake.move()
    score.score()

    clock.tick(fps) 
       
    # Updates the Game Screen
    pygame.display.update()
