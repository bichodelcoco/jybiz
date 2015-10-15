from b2_classes import *
from b2_units import *

class MonsterSpawn(pygame.sprite.Sprite):

	def __init__(self,world, pos, monsterClass,monsterValues = [], monster_cooldown = 10.0, duration = -1, online = False):

		self.world = world
		self.pos = pos
		self.monsterClass = monsterClass
		self.monsterValues = monsterValues
		self.monster_cooldown = monster_cooldown
		self.duration = duration
		self.elapsedTime = 0.0
		self.groups = allGroup, spawnGroup
		self.online = online

		pygame.sprite.Sprite.__init__(self, self.groups)
	
			

	def update(self, seconds):
		if self.online :
			self.elapsedTime += seconds
			if self.elapsedTime >= self.monster_cooldown:
				self.spawn()
				self.elapsedTime = 0.0

	def draw(self):
		pass


	def spawn(self):
		if self.monsterClass.__name__ == 'Skull' :
			if self.monsterValues == []:
				Skull(self.world, self.pos,attack_range = 400, maxSpeed = 30, accel = 120, target = None)
			else :
				Skull(self.world, self.pos, maxSpeed = monsterValues[0], accel = monsterValues[1], target = monsterValues[2],attack_range = monsterValues[3])
		elif self.monsterClass.__name__ == 'Zombie' :
			if self.monsterValues == []:
				Zombie(self.world, self.pos, maxSpeed = 30, accel = 180, target = None)
			else :
				Zombie(self.world, self.pos, maxSpeed = monsterValues[0], accel = monsterValues[1], target = monsterValues[2])
		elif self.monsterClass.__name__ == 'Vampire' :
			if self.monsterValues == []:
				Vampire(self.world, self.pos, maxSpeed = 30, accel = 120, target = None)
			else :
				Vampire(self.world, self.pos, maxSpeed = monsterValues[0], accel = monsterValues[1], target = monsterValues[2])
		




	def turnOn(self):
		self.online = True
	def turnOff(self):
		self.online = False

