from b2_classes import *
from b2_units import *

class MonsterSpawn(object):

	def __init__(self,world, pos, monsterClass,monsterValues = [], monster_cooldown = 10.0, duration = -1, online = False):

		self.world = world
		self.pos = pos
		self.monsterClass = monsterClass
		self.monsterValues = monsterValues
		self.monster_cooldown = monster_cooldown
		self.duration = duration
		self.elapsedTime = 0.0
		if online :
			self.turnOn()

	def update(self, seconds):
		self.elapsedTime += seconds
		if self.elapsedTime >= self.monster_cooldown:
			self.spawn()
			self.elapsedTime = 0.0


	def spawn(self):
		if self.monsterClass.__name__ == 'Skull' :
			if self.monsterValues == []:
				Skull(self.world, self.pos,attack_range = 400, maxSpeed = 30, accel = 120, target = None)
			else :
				Skull(self.world, self.pos,attack_range = monsterValues[0], maxSpeed = monsterValues[1], accel = monsterValues[2], target = monsterValues[3])



	def turnOn(self):
		if self not in g.TIMERS:
			g.TIMERS.append(self)
	def turnOff(self):
		if self in g.TIMERS:
			g.TIMERS.remove(self)