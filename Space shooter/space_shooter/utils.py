from pygame.image import load
from pygame.mixer import Sound
from pygame import Rect

def load_sprite(name, with_alpha=True):
	path = f"assets/sprites/{name}.png"
	loaded_sprite = load(path)

	if with_alpha:
		return loaded_sprite.convert_alpha()
	else:
		return loaded_sprite.convert()

def load_sound(name):
	path = f"assets/sounds/{name}.wav"
	return Sound(path)

def limit(surface, rect):
	y = rect.y
	if rect.top < 0:
		y = 0
	if rect.bottom > surface.get_size()[1]:
		y = surface.get_size()[1] - rect.h
	return Rect((rect.left, y), rect.size)

def partitions(level):
	sums = []
	array = [0 for _ in range(7)]
	
	def findSum(sum, max, idx, count):
	    if sum == 0:
	        sums.append(array[1:idx])
	        return
	    if count == 0:
	        return
	
	    for i in range(max, 0, -1):
	        if i > sum:
	            continue
	        elif i <= sum:
	            array[idx] = i
	            findSum(sum-i, i, idx+1, count-1)
	
	findSum(level, level, 1, 6)
	return sums
