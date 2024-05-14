from copy import deepcopy

class SortContainer:
	def __init__(self, data):
		self.data = data
		self.operations = []
		self.original_data = deepcopy(data)
		self.index = 0
	def less_than(self, x, y):
		#print(f"{self.data[x]} {['>=', '<'][self.data[x] < self.data[y]]} {self.data[y]}")
		self.operations.append(["compare", x, y])
		return self.data[x] < self.data[y]
	def equal_to(self, x, y):
		#print(f"{self.data[x]} {['!=', '=='][self.data[x] == self.data[y]]} {self.data[y]}")
		self.operations.append(["compare", x, y])
		return self.data[x] == self.data[y]
	def greater_than(self, x, y):
		#print(f"{self.data[x]} {['<=', '>'][self.data[x] > self.data[y]]} {self.data[y]}")
		self.operations.append(["compare", x, y])
		return self.data[x] > self.data[y]
	def swap(self, x, y):
		#print(f"Swapping {self.data[x]} and {self.data[y]}")
		self.operations.append(["swap", x, y])
		temp = self.data[x]
		self.data[x] = self.data[y]
		self.data[y] = temp
	def draw(self, screen):
		buffer1 = numpy.sin(2 * numpy.pi * numpy.arange(44100) * (900 * self.original_data[self.operations[self.index][1]] / max(self.original_data) + 100) / 44100).astype(numpy.float32)
		buffer2 = numpy.sin(2 * numpy.pi * numpy.arange(44100) * (900 * self.original_data[self.operations[self.index][2]] / max(self.original_data) + 100) / 44100).astype(numpy.float32)
		sound1 = pygame.mixer.Sound(buffer1)
		sound2 = pygame.mixer.Sound(buffer2)
		for i in range(len(self.original_data)):
			if i in self.operations[self.index][1 : ]:
				color = "red"
			else:
				color = "white"
			height = 600 * self.original_data[i] / max(self.original_data)
			pygame.draw.rect(screen, color, pygame.Rect(i * 800 / len(self.original_data), 600 - height, 800 / len(self.original_data), height))
		if self.operations[self.index][0] == "swap":
			temp = self.original_data[self.operations[self.index][1]]
			self.original_data[self.operations[self.index][1]] = self.original_data[self.operations[self.index][2]]
			self.original_data[self.operations[self.index][2]] = temp
		self.index += 1
		sound1.set_volume(0.1)
		sound2.set_volume(0.1)
		sound1.play(0, maxtime = 10)
		sound2.play(0, maxtime = 10)
		return self.index < len(self.operations)

def insertion_sort(data):
	container = SortContainer(data)
	i = 1
	while i < len(data):
		j = i
		while j > 0 and container.greater_than(j - 1, j):
			container.swap(j, j - 1)
			j -= 1
		i += 1
	return container

def quicksort(data):
	container = SortContainer(data)
	def _quicksort(lo, hi):
		if lo >= 0 and hi >= 0 and lo < hi:
			p = partition(lo, hi)
			_quicksort(lo, p)
			_quicksort(p + 1, hi)
	def partition(lo, hi):
		i = lo - 1
		j = hi + 1
		while True:
			i += 1
			while container.less_than(i, lo):
				i += 1
			j -= 1
			while container.greater_than(j, lo):
				j -= 1
			if i >= j:
				return j
			container.swap(i, j)
	_quicksort(0, len(data) - 1)
	return container

if __name__ == "__main__":
	import random, pygame, numpy, math
	# numbers = []
	# x = -3
	# while x <= 3:
	# 	numbers.append(math.exp(-x**2 / 2))
	# 	x += 0.01
	numbers = list(range(800))
	random.shuffle(numbers)
	container = quicksort(numbers)
	pygame.init()
	screen = pygame.display.set_mode((800, 600))
	pygame.mixer.init(size = 32)
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				break
		screen.fill("black")
		running = container.draw(screen)
		pygame.display.flip()
	pygame.quit()