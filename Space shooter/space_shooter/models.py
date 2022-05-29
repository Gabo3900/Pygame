from utils import load_sprite, load_sound, limit
from pygame import Rect, font, PixelArray

class Background:
	def __init__(self, image, velocity):
		self.img = load_sprite(image, False)
		self.coord = [0, 0]
		self.coord2 = [-self.img.get_rect().width, 0]
		self.x_original = self.coord[0]
		self.x2_original = self.coord2[0]
		self.velocity = velocity

	def move(self):
		self.coord[0] += self.velocity
		self.coord2[0] += self.velocity
		if self.coord2[0] >= 0:
			self.coord[0] = self.x_original
			self.coord2[0] = self.x2_original

	def draw(self, surface):
		surface.blit(self.img, self.coord)
		surface.blit(self.img, self.coord2)

class GameObject:
	def __init__(self, position, sprite, velocity):
		self.sprite = sprite
		self.rect = self.sprite.get_rect()
		self.rect.move_ip(position)
		self.velocity = velocity

	def draw(self, surface):
		surface.blit(self.sprite, self.rect)

	def move(self, surface):
		self.rect = self.rect.move(self.velocity)

class Text(GameObject):
	def __init__(self, position, text, size, color):
		self.font = font.Font('assets/fonts/ElecstromRegular.ttf', size)
		self.color = color
		sprite = self.font.render(text, True, color)
		super().__init__(position, sprite, (0, 0))

	def update(self, text):
		self.sprite = self.font.render(text, True, self.color)

class Ship(GameObject):
	def __init__(self, position, sprite, create_bullet_callback):
		self.create_bullet_callback = create_bullet_callback
		self.bullet_delay = 0
		self.health = 10
		self.bullet_height = 4
		self.bullet_speed = 3
		self.bullet_damage = 1
		super().__init__(position, sprite, (0, 1))

	def shoot(self, bullet_speed):
		if self.bullet_delay > 20:
			bullet = Bullet((self.rect.centerx, self.rect.centery), bullet_speed, self.bullet_damage, self.bullet_height, self.__class__.__name__)
			bullet.sound.play()
			self.create_bullet_callback(bullet)
			self.bullet_delay = 0

	def hit(self, damage):
		self.health -= damage

class Player(Ship):
	VELOCITY = 2

	def __init__(self, position, create_bullet_callback):
		super().__init__(position, load_sprite("player"), create_bullet_callback)
		self.rect.height = 22

	def accelerate(self, direction):
		self.velocity = self.velocity[0], direction * self.VELOCITY

	def move(self, surface):
		super().move(surface)
		self.rect = limit(surface, self.rect)
		self.bullet_delay += 1

	def shoot(self):
		super().shoot((self.bullet_speed, 0))

class Enemy(Ship):
	def __init__(self, position, type, create_bullet_callback):
		self.type = f'{type:06b}'
		super().__init__(position, load_sprite("enemy"), create_bullet_callback)
		self.velocity = 0, (int(self.type[-1])+1)*self.velocity[1]
		self.health = (int(self.type[-2])+1)*self.health
		self.bullet_height = (int(self.type[-3])+1)*self.bullet_height
		self.bullet_speed = (int(self.type[-4])+1)*self.bullet_speed
		self.bullet_damage = (int(self.type[-5])+1)*self.bullet_damage
	
	def move(self, surface):
		super().move(surface)
		if self.rect.top < 0 or self.rect.bottom > surface.get_size()[1]:
			self.velocity = self.velocity[0], -self.velocity[1]
		self.bullet_delay += 1

	def draw(self, surface):
		pxarray = PixelArray(self.sprite)
		color1 = int(self.type[-6:-4], 2) * 85, int(self.type[-4:-2], 2) * 85, int(self.type[-2:], 2) * 85
		color2 = 255 - color1[0], 255 - color1[1], 255 - color1[2]
		pxarray.replace((51, 51, 0), color1)
		pxarray.replace((51, 153, 0), color2)
		pxarray.close()
		super().draw(surface)

	def shoot(self):
		super().shoot((-self.bullet_speed, 0))

class Bullet(GameObject):
	def __init__(self, position, speed, damage, height, cl):
		self.damage = damage
		self.classe = cl
		super().__init__(position, load_sprite("bullet"), speed)
		self.sound = load_sound('laser')
		self.rect.height = height

	def explode(self, create_explode_callback):
		explosion = Explosion((self.rect.centerx, self.rect.centery))
		explosion.sound.play()
		create_explode_callback(explosion)

class Explosion(GameObject):
	def __init__(self, position):
		super().__init__(position, load_sprite('explosion'), (0, 0))
		self.frame = Rect(0, 0, self.rect.h, self.rect.h)
		self.sound = load_sound('hit')

	def move(self, surface):
		self.frame = self.frame.move(self.rect.h, 0)
		if self.frame.right > self.rect.h * 6:
			del self

	def draw(self, surface):
		surface.blit(self.sprite, self.rect, self.frame)
			

