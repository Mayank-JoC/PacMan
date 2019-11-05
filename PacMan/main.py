"""
@author- Mayank Joshi
"""

import pygame
from pygame.locals import *
from numpy import loadtxt
import time
from enemy import *


#Constants for the game
WIDTH, HEIGHT = (12, 12)
WALL_COLOR = pygame.Color(0, 0, 255, 255) # BLUE
PACMAN_COLOR = pygame.Color(255, 0, 0, 255) # RED
COIN_COLOR = pygame.Color(255, 255, 0, 255) # RED
DOWN = (0,1)
RIGHT = (1,0)
TOP = (0,-1)
LEFT = (-1,0)
move_direction=(0,0)
coins_eaten=[]
coins_pos=[]
wall_pos=[]
count=count1=0
rest_state=True
first_state=True
score=0
start_time=time.time()

move_up=[pygame.image.load('up.png'), pygame.image.load('pac.png'), pygame.image.load('up1.png') , pygame.image.load('pac.png')]
move_down=[pygame.image.load('down.png'), pygame.image.load('pac.png'), pygame.image.load('down1.png'), pygame.image.load('pac.png')]
move_left=[pygame.image.load('left.png'), pygame.image.load('pac.png'), pygame.image.load('left1.png'), pygame.image.load('pac.png')]
move_right=[pygame.image.load('right.png'), pygame.image.load('pac.png'), pygame.image.load('right1.png'), pygame.image.load('pac.png')]
coin_pic=[pygame.image.load('coin1.png'), pygame.image.load('coin3.png'), pygame.image.load('coin2.png'),pygame.image.load('coin3.png')]
#def move(clok,):

clock=pygame.time.Clock()


#Draws a rectangle for the wall
def draw_wall(screen, pos):
	pixels = pixels_from_points(pos)
	pygame.draw.rect(screen, WALL_COLOR, [pixels, (WIDTH, HEIGHT)])

#Draws a rectangle for the player
def draw_pacman(screen, pacman_position,move_dir,temp_dir,count): 
	pixels = pixels_from_points(pos)
	#pygame.draw.rect(screen, PACMAN_COLOR, [pixels, (WIDTH, HEIGHT)])
	if move_dir== DOWN or (temp_dir==DOWN and move_dir==(0,0)):
		screen.blit(move_down[count%4], (12 * pacman_position[0], 12 * pacman_position[1]))
	elif move_dir== TOP or (temp_dir==TOP and move_dir==(0,0)):
		screen.blit(move_up[count%4], (12 * pacman_position[0], 12 * pacman_position[1]))
	elif move_dir== LEFT or (temp_dir==LEFT and move_dir==(0,0)):
		screen.blit(move_left[count%4], (12 * pacman_position[0], 12 * pacman_position[1]))
	elif move_dir== RIGHT or (temp_dir==RIGHT and move_dir==(0,0)):
		screen.blit(move_right[count%4], (12 * pacman_position[0], 12 * pacman_position[1]))


#Draws a rectangle for the coin
def draw_coin(screen, pos, lens, count):
	pixels = pixels_from_points(pos)
	#pygame.draw.rect(screen, COIN_COLOR, [pixels, (WIDTH, HEIGHT)])
	screen.blit(coin_pic[(count//lens)%4],pixels)
#Uitlity functions
def add_to_pos(pos, pos2):
	return (pos[0]+pos2[0], pos[1]+pos2[1])
def pixels_from_points(pos):
	return (pos[0]*WIDTH, pos[1]*HEIGHT)

def game_over(screen,score):
	font = pygame.font.SysFont('comicsans', 50, True)
	text = font.render('GAME OVER!', 1, (0,0,0))
	screen.blit(text, (50, 110))
	text = font.render('Score: '+ str(score), 1, (0,0,0))
	screen.blit(text, (90, 170))
	pygame.display.update()

	time.sleep(4)
	quit()

def you_won(screen,score):
	font = pygame.font.SysFont('comicsans', 50, True)
	text = font.render('Hurray! You Won', 1, (0,0,0))
	screen.blit(text, (10, 110))
	text = font.render('Score: '+ str(score), 1, (0,0,0))
	screen.blit(text, (90, 170))
	pygame.display.update()

	time.sleep(4)
	quit()

#Initializing pygame
pygame.init()
screen = pygame.display.set_mode((28*12,34*12))
background = pygame.surface.Surface((320,320)).convert()

fo = open("score.txt", "r") 
line= fo.read()
highscore=int(line)

#Initializing variables
layout = loadtxt('layout.txt', dtype=str)
rows, cols = layout.shape
pacman_position = (1,3)
background.fill((255,255,255))
for col in range(cols):
	for row in range(rows):
		value = layout[row][col]
		pos = (col, row)
		if value == 'w':
			wall_pos.append(pos)
		elif value == 'c':
			coins_pos.append(pos)

enemy_list=[enemy((26,28),0,wall_pos),enemy((26,28),0,wall_pos),enemy((3,28),0,wall_pos),enemy((3,28),0,wall_pos)]


# Main game loop 
run=True
while run:
	clock.tick(40)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	screen.blit(background, (0,0))

	#Draw board from the 2d layout array.
  #In the board, '.' denote the empty space, 'w' are the walls, 'c' are the coins

	for walls in wall_pos:			
		draw_wall(screen, walls)

	for coin_pos in coins_pos:
		draw_coin(screen,coin_pos,len(coins_pos),count)
	
	for col in range(cols):
		for row in range(rows): 
			pos = (col, row)
			if pos not in wall_pos and pos not in coins_pos:
				pygame.draw.rect(screen, pygame.Color(255, 255, 255, 0), [pixels_from_points(pos), (WIDTH, HEIGHT)])
	
	#TODO: Take input from the user and update pacman moving direction, Currently hardcoded to always move down
	keys = pygame.key.get_pressed()
	
	if move_direction!=(0,0) or first_state:
		temp_dir=move_direction
		first_state=False


	if keys[pygame.K_LEFT]:
		move_direction = LEFT
		rest_state=False
	elif keys[pygame.K_RIGHT]:
		move_direction = RIGHT
		rest_state=False
	elif keys[pygame.K_UP]:
		move_direction = TOP
		rest_state=False
	elif keys[pygame.K_DOWN]:
		rest_state=False
		move_direction = DOWN
		rest_state=False
	#Update player position based on movement.

	if rest_state:
		screen.blit(move_right[0],(12 * pacman_position[0], 12 * pacman_position[1]))

	if add_to_pos(pacman_position, move_direction) in wall_pos:
		if move_direction==temp_dir:
			move_direction=(0,0)
		else:
			move_direction=temp_dir	

	pacman_position=add_to_pos(pacman_position, move_direction)

	if pacman_position==(-1,16):
		pacman_position=(27,16)
		move_direction=LEFT
	elif pacman_position==(28,16):
		pacman_position=(0,16)
		move_direction=RIGHT

	if count+1>=40:
		count=0

	if pacman_position in coins_pos:
		coins_pos.remove(pacman_position)
		score+=1
	if score>highscore:
		highscore=score
		file = open("score.txt","w")
		file.write(str(highscore))
		file.close()

	if pacman_position not in wall_pos:
		draw_pacman(screen, pacman_position,move_direction, temp_dir,count)
		
	count+=1
	#TODO: Check if player ate any coin, or collided with the wall by using the layout array.
	# player should stop when colliding with a wall
	# coin should dissapear when eating, i.e update the layout array
	
	#Draw the player
	for enemyy in enemy_list:
		if enemyy.position==pacman_position:
			game_over(screen,score)
			break

	if score==5:
		you_won(screen,score)

	for enemyy in enemy_list:
		enemyy.random_movement(screen)		

	font = pygame.font.SysFont('comicsans', 24, True)
	text = font.render('Highscore: '+ str(highscore)+'      Time: ' + str(int(time.time()-start_time)) +'       Score: ' + str(score), 1, (0,0,0))
	screen.blit(text, (10, 10))
	#Update the display
	pygame.display.update()

	#Wait for a while, computers are very fast.
	time.sleep(0.3)