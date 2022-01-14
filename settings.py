
from os import path

IMG_DIR = 'assets/sprites/'
CAR_IMG_DIR = IMG_DIR + 'car/'
AUDIO_DIR = 'assets/audios/'
FONT_DIR = 'assets/fonts/'

# screen settings.
WIDTH = 720
HEIGHT = 1280
FPS = 60

# define colors.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
BLUE = (0, 0, 210)
GRAY = (230, 230, 230)
GREEN = (0, 180, 0)
BROWN = (101, 67, 33)

PIXEL_PER_SECOND = 100

# highway settings.
ROAD_SIZE = (480, HEIGHT)

# strip settings.
STRIP_SIZE = (10, 100)
STRIP_GAP = 120
STRIP_VEL = 4

# tree settings and images.
tree_index = 0
TREE_GAP = 20
TREES = [
	{
		'filename': IMG_DIR + 'big-tree.png',
		'size': (170, 170)
	},
	{
		'filename': IMG_DIR + 'small-tree.png',
		'size': (120, 140)
	}
]

# player settings.
PLAYER = {
	'normal': CAR_IMG_DIR + 'Audi.png',
	'fly': [CAR_IMG_DIR + f'fly_animation/{i}.png' for i in range(1, 6)]
}  
PLAYER_SIZE = (200, 160)
PLAYER_VEL = 3.2
FLY_TIMES = [100, 90, 350, 90, 100]

# fly stats sttings.
FLY_BLOCK_WIDTH = 40
MAX_FLY = 5

# car settings and images.
CAR_GAPS_Y = list(range(-2000, 0, 500))
way_num = -1
CARS = [
	{
		'file': [CAR_IMG_DIR + f'Ambulance_animation/{i}.png' for i in range(1, 4)],
		'size': (300, 200),
		'vel': 1,
		'minus': (0, 40),
		'pos': (4, 0)
	},
	{
		'file': CAR_IMG_DIR + 'Car.png',
		'size': PLAYER_SIZE,
		'vel': 2.7,
		'minus': (16, 120)
	},
	{
		'file': CAR_IMG_DIR + 'truck.png',
		'size': (300, 320),
		'vel': 1.5, 
		'minus': (0, 0),
		'pos': (10, 0)
	},
	{
		'file': CAR_IMG_DIR + 'Mini_truck.png',
		'size': (260, 220),
		'vel': 2,
		'minus': (0, 70),
		'pos': (10, 10)
	},
	{
		'file': CAR_IMG_DIR + 'Mini_van.png',
		'size': (260, 200),
		'vel': 1.7,
		'minus': (10, 100),
		'pos': (7, 0)
	},
	{
		'file': [CAR_IMG_DIR + f'Police_animation/{i}.png' for i in range(1, 4)],
		'size': (200, 160),
		'vel': 2.9,
		'minus': (0, 20)
	},
	{
		'file': CAR_IMG_DIR + 'taxi.png',
		'size': (180, 160),
		'vel': 2.5,
		'minus': (20, 100),
		'pos': (3, 0)
	}
]

# explosion settings and images.
EXPLOSIONS = [IMG_DIR + f'Explosion/regularExplosion0{i}.png' for i in range(9)]

