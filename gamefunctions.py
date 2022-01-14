
import pygame as pg
import sys
import random as rd

from classes import *
import settings as s


def makeStrips(strips, road):
	"""Create N new strip object and set its position."""
	prev = strips.sprites()[-1]
	# Create a new strip
	strip = Strips(road)
	strip.rect1.bottom = strip.rect2.bottom = prev.rect1.top - STRIP_GAP
	strips.add(strip)
	
	
def makeRandomCar(cars, road, level):
	"""Create random car and set its position."""
	car_info = rd.choice(CARS)
	s.way_num = (s.way_num + 1) % 3
	if type(car_info["file"]) == list:
		car = AnimatedCar(car_info)
	else:
		car = Car(car_info)
		
	car.rect.centery = rd.choice(CAR_GAPS_Y)
	car.rect.centerx = road.rect.left + road.rect.w / 6 + (road.rect.w / 3 * s.way_num + 1)
	car.inside_rect.center = car.rect.center
	try:
		car.inside_rect.centerx = car.rect.centerx - car_info["pos"][0]
		car.inside_rect.centery = car.rect.centery - car_info["pos"][1]
	except KeyError:
		pass
	car.vy += 0.4 * level
	cars.add(car)
	
	
def makeSideTrees(trees, road):
	"""Create new brush and set its positions."""
	prev = trees.sprites()[-1]
	s.tree_index = (s.tree_index + 1) % 2
	# Create a new side tress
	tree = SideTrees(road, TREES[s.tree_index])
	tree.left.rect.bottom = tree.right.rect.bottom = prev.left.rect.top - TREE_GAP
	trees.add(tree)
	
	
def checkEnough( strips, trees, cars, road, level ):
	'''Check every components is enough or not
		if not make a new one.'''
	if len(strips) < 9:
		makeStrips(strips, road)
			
	if len(trees) < 11:
		makeSideTrees(trees, road)
		
	if len(cars) < 4:
		makeRandomCar(cars, road, level)


def checkCarPassed(game, player):
	for car in game.cars:
		if car.rect.top >= player.rect.top and not car.passed:
			car.passed = True
			player.car_passed += 1
			game.score.update()
			# Check level increment.
			if player.car_passed % 5 == 0:
				if game.level < 10:
					game.level += 1
			# Check fly progress.
			if not game.fly_stats.max:
				if not game.fly_stats.progress[1]:
					game.fly_stats.progress[1] = True
				elif not game.fly_stats.progress[2]:
					game.fly_stats.progress[2] = True
				elif not game.fly_stats.progress[3]:
					game.fly_stats.progress[3] = True
				elif not game.fly_stats.progress[0]:
					game.fly_stats.progress[0] = True
				elif not game.fly_stats.progress[4]:
					game.fly_stats.progress[4] = True
			
			
def checkCrash(player, cars, exps, sound):
	for car in cars:
		if player.inside_rect.colliderect(car.inside_rect) and not player.bl_fly and not player.crashed:
			player.crashed = True
			sound.crash.play()
			left = Explosion(player.inside_rect.topleft)
			right = Explosion(player.inside_rect.topright)
			exps.add(left)
			exps.add(right)
			
			
def drawRoadMargins(screen, road):
	"""Draw the both margin of the road."""
	pg.draw.line(screen, GRAY, (road.rect.x, 0), (road.rect.x, HEIGHT), 20)
	pg.draw.line(screen, BROWN, (road.rect.x, 0), (road.rect.x, HEIGHT), 10)
	
	pg.draw.line(screen, GRAY, (road.rect.right, 0), (road.rect.right, HEIGHT), 20)
	pg.draw.line(screen, BROWN, (road.rect.right, 0), (road.rect.right, HEIGHT), 10)
	


