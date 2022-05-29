from numpy import random, exp, dot
from pygame import Rect, draw
import math
from utils import distPoints

class Network:
	def __init__(self, sizes):
		self.num_layers = len(sizes)
		self.sizes = sizes
		self.biases = [random.randn(y, 1) for y in sizes[1:]]
		self.weights = [random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

	def _sigmoid(self, z):
		return 1.0/(1.0+exp(-z))

	def feedforward(self, a):
		for b, w in zip(self.biases, self.weights):
			a = self._sigmoid(dot(w, a)+b)
		return a

class GameObject:
	QTD_SENSORES = 5
	def __init__(self, position, size, color, velocity):
		self.rect = Rect(position, size)
		self.color = color
		self.velocity = velocity
		self.direction = [0, 0]
		self.sensores = [None for _ in range(self.QTD_SENSORES)]
		self.drawSensores = [None for _ in range(self.QTD_SENSORES)]
		self.angle = 0
		self.brain = None

	def draw(self, surface):
		draw.circle(surface, self.color, self.rect.center, self.rect.width/2)
		for sensor in self.drawSensores:
			print(sensor)
			draw.line(surface, (0, 0, 0), sensor[0], sensor[1])

	def move(self):
		self.rect = self.rect.move(self.direction)
		self.direction = [0, 0]

	def look(self, game_objects):
		if self.brain:
			objects = game_objects[:]
			objects.remove(self)
			rects = []
			for i in objects:
				rects.append(i.rect)
			
			for i in range(self.QTD_SENSORES):
				vision = Rect(0, 0, self.rect.height/5, self.rect.height/5)
				a = self.angle - 90 + i * 180 / (self.QTD_SENSORES - 1)
				direction = math.cos(a*math.pi/180.0), math.sin(a*math.pi/180.0)
				dist = 0
				tp = 0
				pos_float = [self.rect.centerx, self.rect.centery]
				while dist <= 150:
					pos_float[0] += direction[0]
					pos_float[1] += direction[1]
					vision.x = pos_float[0]
					vision.y = pos_float[1]
					dist = distPoints(self.rect, vision)
					index = vision.collidelist(rects)
					if index != -1:
						types = ['', 'Grass', 'Bambi', 'Lion']
						for i in range(1, len(types)):
							if isinstance(objects[index], types[i]):
								tp = i
								break
						break
				self.drawSensores[i] = (self.rect.centerx, self.rect.centery), (vision.x, vision.y)
				self.sensores[i] = dist, tp

	def think(self):
		if self.brain:
			entrada = []
			for s in self.sensores:
				entrada.append(s[0])
				entrada.append(s[1])
			saida = self.feedforward(entrada)
			print(saida)
			

	def collides_with(self, others_obj):
		self.rect.collidelist(others_obj)

class Lion(GameObject):
	def __init__(self, position, size):
		super().__init__(position, size, (255, 255, 0), 1)
		#self.brain = Network([self.QTD_SENSORES*2, 10, 6])

class Bambi(GameObject):
	def __init__(self, position, size):
		super().__init__(position, size, (0, 0, 0), 1)
		#self.brain = Network([self.QTD_SENSORES*2, 8, 7])

class Grass(GameObject):
	def __inti__(self, position, size):
		super().__init__(position, size, (0, 255, 0), 0)