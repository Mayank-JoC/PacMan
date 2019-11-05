"""
@author- Mayank Joshi
"""

import random
import pygame



DOWN = (0,1)
RIGHT = (1,0)
TOP = (0,-1)
LEFT = (-1,0)
enemy_pics=[pygame.image.load('E0.png'),pygame.image.load('E1.png'),pygame.image.load('E2.png'),pygame.image.load('E3.png')]

class enemy:
	def __init__(self,pos,count,wall_pos):
		self.position=pos
		self.direction=(-1,0)
		self.all_directions=[LEFT,RIGHT,TOP,DOWN]
		self.count=count
		self.wall_pos=wall_pos

	def random_movement(self,screen):
		temp_list=self.all_directions[:]
		tup=(self.direction[0]*-1, self.direction[1]*-1)
		
		if self.position==(-1,16):
			self.position=(27,16)
		elif self.position==(28,16):
			self.position=(0,16)
			
		while True:
			next_direction=temp_list[random.randint(0,3)]
			if (self.add_to_pos(next_direction) not in self.wall_pos) and next_direction!=tup:
				self.position=self.add_to_pos(next_direction)
				self.direction=next_direction
				#self.draw_enemy()
				break
		self.draw_enemy(screen)

	def add_to_pos(self,pos2):
		return (self.position[0]+pos2[0], self.position[1]+pos2[1])

	def draw_enemy(self,screen):
		if self.count>40:
			self.count=0
		else:
			self.count+=1
		screen.blit(enemy_pics[self.count%4], (12 * self.position[0], 12 * self.position[1]))
