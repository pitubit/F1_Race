,
import sys
import importlib
import os
import pygame as pg
from pygame.locals import *

import random as rd
from settings import *
import gamefunctions as gf
from classes import *
from myutility import GameSprite

en = importlib.import_module('..entity', package='games')

class F1Race:
	'''Game class of f1 race.'''
	def __init__( self ):
		'''Initialize the pygame, make screen, etc.'''
		pg.init( )
		pg.mixer.init( )
		self.screen = pg.display.set_mode( (WIDTH, HEIGHT), HWSURFACE )
		self.clock = pg.time.Clock( )
		#self.font = pg.font.Font( None, 50 )
		self.done = False
	
	def new( self ):
		'''Initialize all the components of game.'''
		pg.mixer.music.load( AUDIO_DIR + 'background.wav' )
		pg.mixer.music.set_volume( 0.8 )
		self.game_over = False
		self.level = 1
		
		# Create a road.
		self.road = GameSprite( IMG_DIR + 'black-road.png' )
		self.road.scale( ROAD_SIZE )
		self.road.rect.center = WIDTH / 2, HEIGHT / 2
		
		# Create strips of the road.
		self.strips = pg.sprite.Group( )
		strip = Strips( self.road )
		self.strips.add( strip )
		
		# Create side trees of the road.
		self.trees = pg.sprite.Group( )
		tree = SideTrees( self.road, TREES[0] )
		self.trees.add( tree )
		
		# Create random cars and add it.
		self.cars = pg.sprite.Group( )
		for i in range( 2 ):
			gf.makeRandomCar( self.cars, self.road, self.level )
	
		# Create more strips and side trees and add it.
		for i in range( 10 ):
			gf.makeStrips( self.strips, self.road )
			gf.makeSideTrees( self.trees, self.road )
	
		self.player = Player( self )
		
		self.sound = Sound( )
		
		self.fly_stats = FlyStats( self.road )

		self.explosions = pg.sprite.Group( )
		
		self.score = Score()
	
		
		
# --------------------GAME LOOP SECTION---------------------
	def run( self ):
		'''Start the game loop.'''
		pg.mixer.music.play( loops=-1 )
		
		while not self.game_over:
			# Run the frame as fps and get deltatime.
			dt = self.clock.tick( FPS ) / 1000
			
			self.check_events( )
			self.update( dt )
			self.draw( )
	
	def check_events( self ):
		'''Game loop - check events.'''
		for event in pg.event.get():
			# Respond fingerdown event.
			if event.type == FINGERDOWN:
				x, y = int(event.x * WIDTH), int(event.y * HEIGHT)
				# check user pressed fly button.
				if self.fly_stats.button.rect.collidepoint( x, y ) and self.fly_stats.count > 0:
					self.player.bl_fly = True
					self.fly_stats.count -= 1
					self.sound.jump.play( )
				elif event.x < 0.25:
					self.player.moving_left = True
				elif event.x > 0.75:
					self.player.moving_right = True
					
			# Respond fingerup event.
			elif event.type == FINGERUP:
				if event.x < 0.25:
					self.player.moving_left = False
				elif event.x > 0.75:
					self.player.moving_right = False
	
	def update( self, dt ):
		'''Game loop - update'''
		gf.checkEnough( self.strips, self.trees, self.cars, self.road, self.level )
		gf.checkCrash( self.player, self.cars, self.explosions, self.sound)
		gf.checkCarPassed( self, self.player )
		
		if not self.player.crashed:
			# Update all the components of game.
			self.strips.update( dt )
			self.trees.update( dt )
			self.cars.update( dt )
			self.player.update( dt )
			self.fly_stats.update( )
		else:
			self.explosions.update( )
	
	def draw( self ):
		'''Game loop - draw'''
		self.screen.fill( GREEN )
		self.road.draw( self.screen )
		gf.drawRoadMargins( self.screen, self.road )
		
		# Draw strips and trees
		for strip in self.strips:
			strip.draw( self.screen )
		for tree in self.trees:
			tree.draw( self.screen )
			
		# Draw cars, player and fly_stats.
		self.cars.draw( self.screen )
		self.player.draw( self.screen )
		self.fly_stats.draw( self.screen )
		self.score.draw( self.screen )
		
		# Draw explosions if player crashed.
		if self.player.crashed:
			self.explosions.draw( self.screen )
			if not self.explosions.sprites( ):
				self.game_over = True
				
		# Flip the entire screen.
		pg.display.flip()
# ------------------END GAME LOOP SECTION-------------------
	
	def menu_screen( self ):
		'''Display the menu screen.'''
		car = GameSprite( IMG_DIR + 'red-car.jpg' )
		car.image.set_colorkey( WHITE )
		car.rect.center = WIDTH / 2, 300
		
		font = pg.font.Font( FONT_DIR + 'intro.otf', 180 )
		f1 = font.render( 'F1', True, RED )
		font = pg.font.Font( FONT_DIR + 'intro.otf', 100 )
		race = font.render( 'race', True, BLACK )
		
		font = pg.font.Font( FONT_DIR + 'EvilEmpire.ttf', 80 )
		play = font.render( 'New Game', True, BLACK )
		exit = font.render( 'Exit', True, BLACK )
		pr = play.get_rect()
		pr.center = WIDTH / 2, HEIGHT / 2 + 100
		er = exit.get_rect()
		er.center = WIDTH / 2, pr.bottom + 100
		
		while True:
			for event in pg.event.get():
				if event.type == FINGERDOWN:
					x, y = event.x * WIDTH, event.y * HEIGHT
					if pr.collidepoint(x, y):
						pg.time.wait( 200 )
						return False
					if er.collidepoint(x, y):
						return True
						
			self.screen.fill( WHITE )
			
			car.draw( self.screen )
			self.screen.blit( f1, (WIDTH / 12 - 10, 400) )
			self.screen.blit( race, (WIDTH / 3 + 50, 458) )
			self.screen.blit( play, pr )
			self.screen.blit( exit, er )
			
			pg.display.flip( )
			self.clock.tick( FPS )
			
	def game_over_screen( self ):
		'''Display the game over screen.'''
		pg.mixer.music.stop( )
		font = pg.font.Font( FONT_DIR + 'EvilEmpire.ttf', 130 )
		game_over = font.render( 'Game over', True, BLACK )
		score = font.render( str(self.score.value), True, RED )
		sr = score.get_rect()
		sr.center = WIDTH / 2, HEIGHT / 2
		
		while True:
			for event in pg.event.get():
				if event.type == FINGERDOWN:
					return
			
			self.screen.fill(WHITE)
			
			self.screen.blit(game_over, (100, 400))
			self.screen.blit(score, sr)
			
			pg.display.flip( )
			self.clock.tick( FPS )
		
	def play( self ):
		'''play/start the game.'''
		while not self.done:
			self.done = self.menu_screen( )
			if not self.done:
				self.new( )
				self.run( )
				self.game_over_screen( )
		

if __name__ == '__main__':
	game = F1Race()
	game.play()
	








