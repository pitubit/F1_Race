
import pygame as pg
import random as rd
from settings import *
from myutility import GameSprite, AnimateSprite

class Player(pg.sprite.Sprite):
	"""Player model of game."""
	def __init__(self, game):
		super().__init__()
		self.game = game
		self.run = GameSprite(PLAYER["normal"])
		self.fly = AnimateSprite(PLAYER["fly"])
		
		self.run.scale(PLAYER_SIZE)
		self.fly.scale((PLAYER_SIZE[0] + 80, PLAYER_SIZE[1] + 80), 2)
		self.fly.scale((PLAYER_SIZE[0] + 20, PLAYER_SIZE[1] + 20), 1, 3)
		self.fly.scale(PLAYER_SIZE, 0, 4)
		self.fly.setRandomTimes(FLY_TIMES)
		
		self.image = self.run.image
		self.rect = self.image.get_rect()
		self.rect.center = WIDTH / 2, HEIGHT - 200
		
		self.inside_rect = self.rect.copy()
		self.inside_rect.width = self.inside_rect.width / 3 + 6
		self.inside_rect.height -= 60
		self.inside_rect.center = self.rect.center
		
		self.vx = PLAYER_VEL
		self.pos = float(self.rect.centerx)
		self.moving_left = False
		self.moving_right = False
		self.bl_fly = False
		self.crashed = False
		self.car_passed = 1
		
	def getRectAndCenter(self):
		center = self.rect.center
		self.rect = self.image.get_rect()
		self.rect.center = center
	
	def update(self, dt):
		if self.moving_left and self.inside_rect.left >= self.game.road.rect.left + 30:
			self.pos -= self.vx * dt * PIXEL_PER_SECOND
		if self.moving_right and self.inside_rect.right <= self.game.road.rect.right - 30:
			self.pos += self.vx * dt * PIXEL_PER_SECOND
		
		self.rect.centerx = self.pos
		self.inside_rect.centerx = self.rect.centerx
		
		if self.bl_fly:
			if self.fly.randomTimeAnimate(dt*1000) != 0:
				self.image = self.fly.image
				self.getRectAndCenter()
			else:
				self.bl_fly = False
				self.image = self.run.image
				self.getRectAndCenter()
		
	def draw(self, surf):
		surf.blit(self.image, self.rect)
		
		
class FlyStats:
	def __init__(self, road):
		self.button = GameSprite(IMG_DIR + "up-chevron.png")
		self.button.rect.center = road.rect.right + 40, 1000
		
		self.fly_bar = pg.Rect(0, 0, FLY_BLOCK_WIDTH, FLY_BLOCK_WIDTH * MAX_FLY)
		self.fly_current = pg.Rect(0, 0, FLY_BLOCK_WIDTH, FLY_BLOCK_WIDTH)
		
		self.fly_current.centerx = self.fly_bar.centerx = self.button.rect.centerx
		self.fly_current.bottom = self.fly_bar.bottom = self.button.rect.top + 12
		
		self.fly_current.h = FLY_BLOCK_WIDTH
		self.progress = [False] * 5
		self.count = 1
		self.max = False
		
	def update(self):
		if not False in self.progress and not self.max:
			self.progress = [False] * 5
			self.count += 1
		if self.count == MAX_FLY:
			self.max = True
		else:
			self.max = False
		
		self.fly_current.h = FLY_BLOCK_WIDTH * self.count
		self.fly_current.bottom = self.button.rect.top + 12
		
	def draw(self, surf):
		pg.draw.rect(surf, BLUE, self.fly_current, 0)
		pg.draw.rect(surf, BLACK, self.fly_bar, 4)
		surf.blit(self.button.image, self.button.rect)
		if self.progress[1]:
			pg.draw.circle(surf, RED, self.button.rect.center, 60, 18, *self.progress[:-1])
	
	
class Car(GameSprite):
	"""Random car used to draw randomly."""
	def __init__(self, car):
		super().__init__(car["file"])
		self.vy = car["vel"]
		
		self.inside_rect = self.rect.copy()
		self.inside_rect.w = (self.inside_rect.w / 3) - car["minus"][0]
		self.inside_rect.h -= car["minus"][1]
		
		self.scale(car["size"])
		self.flip(False, True)
		self.passed = False
		
	def update(self, dt):
		self.rect.centery += (STRIP_VEL + self.vy) * dt * PIXEL_PER_SECOND
		self.inside_rect.centery += (STRIP_VEL + self.vy) * dt * PIXEL_PER_SECOND
		if self.rect.top >= HEIGHT:
			self.kill()
						
		
class AnimatedCar(pg.sprite.Sprite):
	"""A class of animated car."""
	def __init__(self, car):
		super().__init__()
		
		self.images = []
		self.index = 0
		self.vy = car["vel"]
		self.frameCount = -1
		
		for fn in car["file"]:
			image = pg.image.load(fn)
			image = pg.transform.scale(image, car["size"])
			self.images.append(pg.transform.flip(image, False, True))
			
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		
		self.inside_rect = self.rect.copy()
		self.inside_rect.w = (self.inside_rect.w / 3) - car["minus"][0]
		self.inside_rect.h -= car["minus"][1]
		
		self.passed = False
			
	def update(self, dt=1):
		self.rect.centery += (STRIP_VEL + self.vy) * dt * PIXEL_PER_SECOND
		self.inside_rect.centery += (STRIP_VEL + self.vy) * dt * PIXEL_PER_SECOND
		if self.frameCount == 0:
			self.index = (self.index + 1) % 3
			self.image = self.images[self.index]
		self.frameCount = (self.frameCount + 1) % 10
		if self.rect.top >= HEIGHT:
			self.kill()
		
	def draw(self, surf):
		surf.blit(self.image, self.rect)
		

class SideTrees(pg.sprite.Sprite):
	"""Brush class draw on side."""
	def __init__(self, road, tree):
		super().__init__()
		
		self.left = GameSprite(tree["filename"])
		self.right = GameSprite(tree["filename"])
		
		self.left.scale(tree["size"])
		self.right.scale(tree["size"])
		self.right.flip(True, False)
		
		self.left.rect.centerx = road.rect.left - 50
		self.right.rect.centerx = road.rect.right + 50
		self.left.rect.bottom = self.right.rect.bottom = HEIGHT
		
	def update(self, dt=1):
		self.left.rect.y += STRIP_VEL * dt * PIXEL_PER_SECOND
		self.right.rect.y += STRIP_VEL * dt * PIXEL_PER_SECOND
		if self.left.rect.top >= HEIGHT:
			self.kill()
	
	def draw(self, surf):
		surf.blit(self.left.image, self.left.rect)
		surf.blit(self.right.image, self.right.rect)
	
	
class Strips(pg.sprite.Sprite):
	"""Strip model draw on highway."""
	def __init__(self, road):
		super().__init__()
		
		self.rect1 = pg.Rect((0, 0), STRIP_SIZE)
		self.rect2 = pg.Rect((0, 0), STRIP_SIZE)
		
		x = ROAD_SIZE[0] / 3
		self.rect1.centerx = road.rect.left + x
		self.rect2.centerx = road.rect.left + x * 2
		self.rect1.bottom = self.rect2.bottom = HEIGHT
		
	def update(self, dt=1):
		"""Update the strip"""
		self.rect1.y += STRIP_VEL * dt * PIXEL_PER_SECOND
		self.rect2.y += STRIP_VEL * dt * PIXEL_PER_SECOND
		if self.rect1.top >= HEIGHT:
			self.kill() 
		
	def draw(self, surf):
		"""Draw the rects."""
		pg.draw.rect(surf, GRAY, self.rect1)
		pg.draw.rect(surf, GRAY, self.rect2)
		
		
class Sound:
	def __init__(self):
		self.crash = pg.mixer.Sound("assets/audios/Crash.wav")
		self.jump = pg.mixer.Sound("assets/audios/jump.wav")


class Explosion(pg.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		
		self.images = []
		for fn in EXPLOSIONS:
			image = pg.transform.scale(pg.image.load(fn).convert_alpha(), (100, 100))
			self.images.append(image)
			
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.fr = 0
		self.frame_rate = 50
		self.last_update = pg.time.get_ticks()
	
	def update(self, dt=1):
		now = pg.time.get_ticks()
		if now - self.last_update >= self.frame_rate:
			self.last_update = now
			self.fr += 1
			if self.fr == len(self.images):
				self.kill()
			else:
				center = self.rect.center
				self.image = self.images[self.fr]
				self.rect = self.image.get_rect()
				self.rect.center = center
	
	def draw(self, surf):
		surf.blit(self.image, self.rect)
		

class Score:
	def __init__(self):
		self.font = pg.font.Font(FONT_DIR + 'score.ttf', 100)
		self.text_surf = self.font.render('0', True, WHITE)
		self.value = 0
		
	def update(self):
		self.value += 1
		self.text_surf = self.font.render(str(self.value), True, WHITE)
		
	def draw(self, surf):
		surf.blit(self.text_surf, (20, 20))
		
		