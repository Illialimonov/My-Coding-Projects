import pygame
from pygame.math import Vector2
import sys
import random


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_grass()

    
    
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            #reposition the fruit
            # add another clock to the snake
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        #check if snake is outside the screen
        #check if snake hits itself
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block ==self.snake.body[0]:
                self.game_over()


    def game_over(self):
        pygame.quit()
        sys.exit()

    def draw_grass(self):
        grass_color = (167,209,61)
        for row in range(cell_number):
            if row%2 ==0:
                for col in range(cell_number):
                    if col%2 ==0:
                        grass_rect=pygame.Rect(col * cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect,layer=0)
            else:
                for col in range(cell_number):
                    if col%2 != 0:
                        grass_rect=pygame.Rect(col * cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect,layer=0)

        

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect  =score_surface.get_rect(center = (score_x, score_y))
        screen.blit(score_surface,score_rect)
            
    

    

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for i, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            
            # Check if it's the head block and set its color to green
            if i == 0:
                pygame.draw.rect(screen, (113, 235, 7), block_rect)
            else:
                pygame.draw.rect(screen, (66, 138, 4), block_rect)

            

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
        
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
        
class FRUIT:
    def __init__(self):
        self.randomize()
        
        #create an x, y

    def draw_fruit(self):
        #create a rectangle in right position
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        
        pygame.draw.rect(screen, (247, 154, 5), fruit_rect)
        

    def randomize(self):
        self.x= random.randint(0,cell_number -1)
        self.y=  random.randint(0,cell_number -1)
        self.pos = Vector2(self.x,self.y)



pygame.init()

cell_size = 40
cell_number = 20



SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

game_font = pygame.font.Font('PoetsenOne-Regular.ttf', 25)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
                
            
        
        

    #main events
    screen.fill((175,215,75))
    main_game.draw_elements()
    

    pygame.display.update()
    clock.tick(60)
