
import pygame as pg

from pygame import transform, image
from pygame.math import Vector2


class GameSprite(pg.sprite.Sprite):
	def __init__(self,  arg):
		"""Initailizing the attributes"""
		super().__init__()
		# Load the image from file.
		if type(arg) == str:
			self.image = image.load(arg).convert_alpha()
		else:
			self.image = pg.Surface(arg)
		self.image.set_colorkey((0, 0, 0), pg.RLEACCEL)
		# Get the current image rect dimension.
		self.rect = self.image.get_rect()
		
	def addMask(self):
		"""Create the mask of the image"""
		self.mask = pg.mask.from_surface(self.image)
	
	def addRadius(self, r):
		"""Create a radius var."""
		self.radius = r
	
	def addVelocity(self, x, y):
		"""Add the velocity to new var."""
		self.velocity = Vector2(x, y)
		
	def setPosition(self, x, y, center=False):
		"""Set the position of sprite"""
		# if center parameter is True set its center.
		if center:
			self.rect.center = x, y
		# else set its topleft position.
		else:
			self.rect.topleft = x, y
	
	def scale(self, size):
		"""Scale the image in given size"""
		# Store the center.
		center = self.rect.center
		
		self.image = transform.scale(self.image, size)
		self.rect = self.image.get_rect()
		# set previous center position.
		self.rect.center = center 
		
	def rotate(self, deg):
		"""Rotate the image at given angle"""
		# Store the center.
		center = self.rect.center
		
		self.image = transform.rotate(self.image, deg)
		self.rect = self.image.get_rect()
		# set previous center position.
		self.rect.center = center 
		
	def flip(self, blX, blY):
		"""Flip the image in horizontical or vertical"""
		self.image = transform.flip(self.image, blX, blY)
		
	def update(self, dt=1):
		"""Update the sprite"""
		self.rect.x += self.velocity.x * dt
		self.rect.y += self.velocity.y * dt
	
	def draw(self, surf):
		"""Draw the image in surface"""
		surf.blit(self.image, self.rect)
		

class AnimateSprite(pg.sprite.Sprite):
	def __init__(self, filenames, min=200):
		"""Initialize the attritubes."""
		super().__init__()
		# Images array and load all images.
		self.images = []
		for fn in filenames:
			self.images.append(image.load(fn).convert_alpha())
		
		self._index = 0
		self.image = self.images[self._index]
		self.rect = self.image.get_rect()
		self._time = 0
		self.imageAnimationTime = min
		
		
	def scale(self, size, *indexes):
		"""Scale the images in given size"""
		center = self.rect.center
		# check any particular indexes are given.
		if not len(indexes):
			for i in range(len(self.images)):
				self.images[i] = transform.scale(self.images[i], size)
		else:
			for i in indexes:
				self.images[i] = transform.scale(self.images[i], size)
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		# set the previous rect center
		self.rect.center = center
		
	def rotate(self, deg, *index):
		"""Rotate the images in given degree"""
		center = self.rect.center
		index = self.images.index(self.image)
		# check any particular indexes are given.
		if not len(indexes):
			for i in range(len(self.images)):
				self.images[i] = transform.rotate(self.images[i], size)
		else:
			for i in index:
				self.images[i] = transform.rotate(self.images[i], size)
		self.image = self.images[index]
		self.rect = self.image.get_rect()
		# set the previous rect center
		self.rect.center = center
	
	def flip(self, blX, blY, *index):
		"""Flip the images in horizontal or vertical."""
		center = self.rect.center
		index = self.images.index(self.image)
		# check any particular indexes are given.
		if not len(indexes):
			for i in range(len(self.images)):
				self.images[i] = transform.flip(self.images[i], blX, blY)
		else:
			for i in index:
				self.images[i] = transform.flip(self.images[i], blX, blY)
		self.image = self.images[index]
		self.rect = self.image.get_rect()
		# set the previous rect center
		self.rect.center = center
		
	def getRectAndCenter(self):
		"""Change the current image and upadte rect in a cycle."""
		center = self.rect.center
		self.image = self.images[self._index]
		self.rect = self.image.get_rect()
		self.rect.center = center
		
	def setRandomTimes(self, times):
		"""Calculate cumulative function of times array"""
		cumTimes = []
		for i in range(len(times)):
			if i == 0:
				cumTimes.append(times[i])
			else:
				cumTimes.append(cumTimes[i-1] + times[i])
		self.imageAnimationTime = cumTimes
	
	def animate(self, dt):
		"""Update the image at certain time."""
		index = self._time // self.imageAnimationTime
		
		if index == len(self.images):
			self._index = self._time = 0
			return 0
			
		self._time += dt
		if index != self._index or self._index == 0:
			self._index = index
			self.getRectAndCenter()
		# Return current time.
		return self._time
	
	def randomTimeAnimate(self, dt):
		"""update the image after completing given random time."""
		if self._time == 0:
			self._index = 0
			self.getRectAndCenter()
			
		self._time += dt
		if self._time >= self.imageAnimationTime[self._index]:
			self._index += 1
			if self._index == len(self.imageAnimationTime):
				self._index = self._time = 0
				return 0
			self.getRectAndCenter()
		return self._time



if __name__ == "__main__":

	pg.init()
	
	screen = pg.display.set_mode((720, 1280))
	clock = pg.time.Clock()
	
	sprite = GameSprite("assets/sprites/car/taxi.png")
	sprite.scale((160, 160))
	sprite.setPosition(20, 800)
	
	while True:
		
		dt = clock.tick_busy_loop(60) * 0.001
		
		for event in pg.event.get():
			if event.type == pg.FINGERDOWN:
				if event.x > 0.75:
					sprite.velocity.x = 6
				if event.x < 0.25:
					sprite.velocity.x = -6
			elif event.type == pg.FINGERUP:
				sprite.velocity.x = 0
			
		screen.fill((230, 0, 0))
		
		sprite.update()
		sprite.draw(screen)
		
		#sprite.velocity = sprite.velocity.lerp((goal, 0), 0.1)
		
		if sprite.rect.left > 720:
			sprite.rect.right = 0
		if sprite.rect.right < 0:
			sprite.rect.left = 720
		
		pg.display.flip()
		


			
