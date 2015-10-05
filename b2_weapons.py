from b2_classes import *

class Weapon(object):
	def __init__(self, owner, weapon_range, cooldown = 0.0):
		self.owner = owner
		self.weapon_range = weapon_range
		self.cooldown = cooldown

	def deactivate(self):
		pass

class Projectile(GameObject):
	''' PROJECTILE.IMAGE0 SHOLD BE HORIZONTAL FACING RIGHT'''

	def __init__(self, world, owner, size, startingPos,  startingImpulse, bullet=False, image0= None,lifetime = -1, density=1, boxShape = True, angle = 0,damage = 1,targetGroup = enemyGroup):
		self.world = world
		self.owner = owner
		self.startingPos = startingPos
		self.size = size
		self.startingImpulse = startingImpulse
		self.lifetime= lifetime
		self.alivetime = 0.0
		self.targetGroup = targetGroup
		self.damage = damage
		self.image0 = image0

		if boxShape :
			self.body = world.CreateDynamicBody(position = pygame_to_box2d(startingPos), bullet=bullet)
			self.fixture = self.body.CreatePolygonFixture(box = pixel_to_meter(size), density = density, friction = 0.3, userData = self)
		self.groups = allGroup, projectileGroup, reboundGroup
		GameObject.__init__(self, lifetime = lifetime)

		self.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec(self.impulse), self.fixture.body.worldCenter, wake = True)



	def update(self, seconds):

		GameObject.update(self,seconds)

		collidegroup = pygame.sprite.spritecollide(self, self.targetGroup, False)
		if collidegroup:
			speed = geo.absolute(self.vel.x + self.vel.y)
			for unit in collidegroup :

				unit.loseHitpoints(speed*self.damage)

	def die(self):
		self.kill()



# bat
#-----------------------------------------------------------------------------------------------
class BaseballBat(Weapon):
	name = 'Bat'
	def __init__(self, owner, power= 1000, aoe = (50,50), weapon_range = 200):
		Weapon.__init__(self,owner, weapon_range)
		self.power = power
		self.aoe = aoe


	def activate(self, mousePos):
		area = AOE(mousePos, self.aoe)
		collidegroup = pygame.sprite.spritecollide(area, enemyGroup, False)
		vec = geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)
		for item in collidegroup :
			item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((vec[0]*self.power,vec[1]*self.power)), item.fixture.body.worldCenter, wake = True)
		area.kill()

# Grenade
# -------------------------------------------------------------------------------------------------
class Grenade(Weapon):
	name = 'Grenade'
	start_range = 20
	size = (25,25)
	weapon_range = 1000 #distance a laquelle tu peux cliquer
	def __init__(self, owner, power = 40, blast_aoe = (100,100), blast_power = 500):#power : init velocity
		Weapon.__init__(self,owner, Grenade.weapon_range)
		self.power = power
		self.blast_aoe = blast_aoe
		self.blast_power = blast_power

	def activate(self, mousePos): #pos = position mouse
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)

		# push objects from starting point else bug
		# push_area = AOE((self.owner.pos[0] + vec[0]*Grenade.start_range,self.owner.pos[1] + vec[1]*Grenade.start_range), (28,28))
		# collidegroup = pygame.sprite.spritecollide(push_area, enemyGroup, False)

		# for item in collidegroup:
		# 	tempVec = geo.normalizeVector(item.rect.centerx - push_area.rect.centerx, item.rect.centery - push_area.rect.centery)
		# 	item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.power,tempVec[1]*self.power)), item.fixture.body.worldCenter, wake = True)
		# -------------------------------------------
		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1])
		Projectile_Grenade(self.owner, pos, self.power, blast_aoe = self.blast_aoe, blast_power = self.blast_power)

#	Grenade Projectile
#-------------------------------------------------------------------------------------------------------------------------

class Projectile_Grenade(Projectile):
	image0 = None
	def __init__(self, owner, pos, power = 40, blast_aoe = (200,200),blast_power = 500):
		# image loading management
		if Projectile_Grenade.image0 == None :
			Projectile_Grenade.image0 = pygame.image.load('images/weapons/grenade.png')
			Projectile_Grenade.image0.set_colorkey(WHITE)
		#--------------------------



		self.power = power
		self.blast_aoe = blast_aoe
		self.blast_power = blast_power
		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		self.impulse = (vec[0]*power, vec[1]*power)
		startingPos = (vec[0]*50 +owner.pos[0], vec[1]*50+ owner.pos[1])

		Projectile.__init__(self, owner.world,owner, Grenade.size, startingPos, self.impulse, image0 = Projectile_Grenade.image0,lifetime = 3)


	def die(self):
		area = AOE(self.pos, self.blast_aoe)
		collidegroup = pygame.sprite.spritecollide(area, unitGroup, False)
		for item in collidegroup:
			tempVec = geo.normalizeVector(item.pos[0]- area.pos[0], item.pos[1] - area.pos[1])
			item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.blast_power,tempVec[1]*self.blast_power)), item.fixture.body.worldCenter, wake = True)

		Projectile.die(self)

	def update(self, seconds):

		Projectile.update(self,seconds)

# Rifle
# ------------------------------------------------------------------------------------------------------------------

class Rifle(Weapon):
	name = 'Rifle'
	start_range = 20
	size = (5,5)
	weapon_range = 1000
	def __init__(self, owner, power = 150):
		Weapon.__init__(self,owner, Rifle.weapon_range)
		self.power = power

	def activate(self, mousePos):
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)

		# ----------------------------------------
		#push objects from starting point else bug
		# push_area = AOE((vec[0]*Rifle.start_range,vec[1]*megaBall.start_range), (6,6))
		# collidegroup = pygame.sprite.spritecollide(push_area, enemyGroup, False)

		# for item in collidegroup:
		# 	tempVec = geo.normalizeVector(item.rect.centerx - push_area.rect.centerx, item.rect.centery - push_area.rect.centery)
		# 	item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.power,tempVec[1]*self.power)), item.fixture.body.worldCenter, wake = True)
		# -------------------------------------------
		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1])
		Projectile_Rifle(self.owner, pos, power=self.power)

# Rifle projectile
# ------------------------------------------------------------------------------------------------------------------
class Projectile_Rifle(Projectile):
	image0 = None
	def __init__(self, owner, pos, power = 150, damage = 0.2):
		# image loading management
		if Projectile_Rifle.image0 == None :
			Projectile_Rifle.image0 = pygame.Surface((5,5))
			Projectile_Rifle.image0.fill(BLACK)
			Projectile_Rifle.image0.set_colorkey(WHITE)
		#--------------------------



		self.power = power
		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		self.impulse = (vec[0]*power, vec[1]*power)
		startingPos = (vec[0]*50 +owner.pos[0], vec[1]*50+ owner.pos[1])

		Projectile.__init__(self, owner.world,owner, Rifle.size, startingPos, self.impulse, bullet=True, image0 = Projectile_Rifle.image0,lifetime = 1, density=20, damage = damage)


	def update(self, seconds):

		Projectile.update(self,seconds)

# Vampire Rifle
# ------------------------------------------------------------------------------------------------------------------

class VampireRifle(Weapon):
	name = 'Rifle'
	start_range = 20
	size = (5,5)
	weapon_range = 1000
	def __init__(self, owner, power = 150):
		Weapon.__init__(self,owner, Rifle.weapon_range)
		self.power = power

	def activate(self, mousePos):
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)

		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1])
		Projectile_VampireRifle(self.owner, pos, power=self.power)

# Vampire Rifle projectile
# ------------------------------------------------------------------------------------------------------------------
class Projectile_VampireRifle(Projectile):
	image0 = None
	size = (10,7)
	def __init__(self, owner, pos, power = 150, targetGroup = playerGroup):
		# image loadinVampireg management
		if self.image0 == None :
			Projectile_VampireRifle.image0 = pygame.Surface(self.size)
			Projectile_VampireRifle.image0.fill(BLACK)
			Projectile_VampireRifle.image0.set_colorkey(WHITE)
		#--------------------------



		self.power = power
		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		self.impulse = (vec[0]*power, vec[1]*power)
		startingPos = (vec[0]*50 +owner.pos[0], vec[1]*50+ owner.pos[1])

		Projectile.__init__(self, owner.world,owner, self.size, startingPos, self.impulse, bullet=True, image0 = Projectile_VampireRifle.image0,lifetime = 1, density=20, targetGroup = targetGroup)


	def update(self, seconds):

		Projectile.update(self,seconds)
# MegaBall
# ------------------------------------------------------------------------------------------------------------------

class megaBall(Weapon):
	name = 'Mega Ball'
	start_range = 250
	size = (75,75)
	weapon_range = 1000
	def __init__(self, owner, power = 10000):
		Weapon.__init__(self,owner, megaBall.weapon_range)
		self.power = power

	def activate(self, mousePos):
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)

		# ----------------------------------------
		#push objects from starting point else bug
		push_area = AOE((vec[0]*megaBall.start_range,vec[1]*megaBall.start_range), (76,76))
		collidegroup = pygame.sprite.spritecollide(push_area, enemyGroup, False)

		for item in collidegroup:
			tempVec = geo.normalizeVector(item.rect.centerx - push_area.rect.centerx, item.rect.centery - push_area.rect.centery)
			item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.power,tempVec[1]*self.power)), item.fixture.body.worldCenter, wake = True)
		# -------------------------------------------
		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1])
		Projectile_megaBall(self.owner, pos, power=self.power)

# MegaBall projectile
# -----------------------------------------------------------------------------------------------------------------------------------

class Projectile_megaBall(Projectile):
	image0 = None
	def __init__(self, owner, pos, power = 10000, blast_aoe = (210,210), blast_power = 10):


		# image loading management
		if Projectile_megaBall.image0 == None :
			Projectile_megaBall.image0 = pygame.image.load('images/weapons/megaSquare75.png')
			Projectile_megaBall.image0.set_colorkey(WHITE)
		#--------------------------

		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])

		self.power = power
		self.blast_aoe=blast_aoe
		self.blast_power=blast_power

		self.impulse = (vec[0]*power, vec[1]*power)
		startingPos = (vec[0]*50 +owner.pos[0], vec[1]*50+ owner.pos[1])

		Projectile.__init__(self, owner.world, owner, megaBall.size, startingPos, self.impulse, image0 = Projectile_megaBall.image0,lifetime = 5, density=500)

		self.fixture.body.gravityScale = 0

	def die(self):
		area = AOE(self.pos, self.blast_aoe)
		collidegroup = pygame.sprite.spritecollide(area, enemyGroup, False)
		for item in collidegroup:
			tempVec = geo.normalizeVector(item.pos[0] - area.pos[0], item.pos[1] - area.pos[1])
			item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.blast_power,tempVec[1]*self.blast_power)), item.fixture.body.worldCenter, wake = True)

		Projectile.die(self)

	def update(self, seconds):

		Projectile.update(self,seconds)
# Hadouken
# ----------------------------------------------------------------------------------------------------------------------------------

class Hadouken(Weapon):
	name = 'Hadouken'
	start_range = 70
	weapon_range = 2000
	def __init__(self, owner, speed = 5, recoil = 10, power = 90000, cooldown = 0.0 ):
		Weapon.__init__(self, owner, Hadouken.weapon_range)
		self.speed = speed
		self.recoil = recoil
		self.power =power
		self.cooldown = cooldown

	def activate(self, mousePos):
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)
		# ----------------------------------------
		# #push objects from starting point else bug
		# push_area = AOE((self.owner.pos[0] + vec[0]*Hadouken.start_range,self.owner.pos[1] + vec[1]*Hadouken.start_range), (221,221))
		# collidegroup = pygame.sprite.spritecollide(push_area, enemyGroup, False)

		# for item in collidegroup:
		# 	tempVec = geo.normalizeVector(item.rect.centerx - push_area.rect.centerx, item.rect.centery - push_area.rect.centery)
		# 	item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.power,tempVec[1]*self.power)), item.fixture.body.worldCenter, wake = True)
		# -------------------------------------------
		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1])
		Projectile_Hadouken(self.owner, pos, power= self.power, speed = self.speed, recoil = self.recoil)

# Hadouken projectile
# -------------------------------------------------------------------------------------------------------------------------------------------

class Projectile_Hadouken(Projectile):
	start_range = 70
	image0 = None
	size = (58,58)

	def __init__(self, owner, pos, speed = 5, power = 800, recoil = 10):

		vec = (pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		if vec[1] <= 0:
			self.angle =geo.vecAngle((1,0), vec)
		else :
			self.angle = -geo.vecAngle((1,0), vec)

		# image loading management
		if Projectile_Hadouken.image0 == None :
			Projectile_Hadouken.image0= pygame.image.load('images/weapons/hadouken.png')
			#Projectile_Hadouken.image0 = pygame.transform.rotate(Projectile_Hadouken.image0, self.angle)
			Projectile_Hadouken.image0.set_colorkey(WHITE)
		#--------------------------

		self.power = power
		self.speed = speed
		self.recoil = recoil

		self.world = owner.world
		self.body = self.world.CreateDynamicBody(position = pygame_to_box2d(pos), bullet = True, angle = self.angle)
		self.body.gravityScale = 0
		self.fixture = self.body.CreateCircleFixture(radius = real_pixel_to_meter(29), restitution = 0.8, density = 500, friction = 0, userData = self)


		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		self.impulse = (vec[0]*self.power, vec[1]* self.power)
		startingPos = (vec[0]*self.start_range + owner.pos[0], vec[1]*self.start_range + owner.pos[1])

		Projectile.__init__(self, self.world, owner, self.size, startingPos, self.impulse,bullet= True, image0 = self.image0, lifetime = 1.5, boxShape = False)

# Grappling Hook
# ----------------------------------------------------------------------------------

class GrapplingHook(Weapon):
	name = 'Hook'
	weapon_range = 1000

	def __init__(self,owner, pull_power =500):

		Weapon.__init__(self, owner, GrapplingHook.weapon_range)
		self.pull_power = pull_power
		self.garbage_bin = []

	def activate(self, mousePos):
		self.hook = Hook(self.owner, mousePos, self.pull_power)
		self.garbage_bin.append(self.hook)

	def deactivate(self):
		for hook in self.garbage_bin :
			hook.kill()
			self.garbage_bin.remove(hook)

# Hook not a regular projectile : has no collision
# ---------------------------------------------------------------------------------------

class Hook(pygame.sprite.Sprite):
	def __init__(self, owner, mousePos, pull_power = 400, traveling_speed = 40):

		self.owner = owner
		self.mousePos = mousePos
		self.pull_power = pull_power
		self.traveling_speed = traveling_speed
		self.latched = False
		self.vec = geo.normalizeVector(self.mousePos[0] - self.owner.rect.centerx,self.mousePos[1] - self.owner.rect.centery)

		self.groups = allGroup, effectGroup
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.image = pygame.Surface((10,10))
		self.image.fill(GREY)

		self.rect = self.image.get_rect()
		self.pos= self.owner.pos[:]
	def update(self, seconds):

		if self.latched == False :
			temp = pygame.sprite.spritecollideany(self, terrainGroup)
			if temp :
				self.latched = True


			else :
				self.pos = (self.pos[0] +self.vec[0]* self.traveling_speed, self.pos[1] +self.vec[1]* self.traveling_speed)

		else :
			self.pull_vec = geo.normalizeVector(self.rect.centerx -self.owner.rect.centerx, self.rect.centery -self.owner.rect.centery)
			self.owner.fixture.body.ApplyForce(pygameVec_to_box2dVec((self.pull_vec[0]*self.pull_power, self.pull_vec[1]*self.pull_power)), self.owner.fixture.body.worldCenter, wake = True)

		self.rect.center = rect(self.pos)

class BouncingBall(Weapon):
	name = 'Bouncing'
	start_range = 5
	weapon_range = 2000
	def __init__(self, owner, power = 20, cooldown = 0.0 ):
		Weapon.__init__(self, owner, self.weapon_range)
		
		self.power =power
		self.cooldown = cooldown

	def activate(self, mousePos):
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)
		
		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1])
		Projectile_BouncingBall(self.owner, pos, power= self.power)

class Projectile_BouncingBall(Projectile):
	image0 = None
	size = (30,30)

	def __init__(self, owner, pos,power = 20):

		vec = (pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		if vec[1] <= 0:
			self.angle =geo.vecAngle((1,0), vec)
		else :
			self.angle = -geo.vecAngle((1,0), vec)

		# image loading management
		if Projectile_BouncingBall.image0 == None :
			Projectile_BouncingBall.image0= pygame.image.load('images/weapons/bouncingball.png')
			#Projectile_BouncingBall.image0 = pygame.transform.rotate(Projectile_BouncingBall.image0, self.angle)
			setColorkey(Projectile_BouncingBall.image0)
		
		#--------------------------

		self.power = power
		

		self.world = owner.world
		self.body = self.world.CreateDynamicBody(position = pygame_to_box2d(pos), bullet = True, angle = self.angle)
		self.fixture = self.body.CreateCircleFixture(radius = real_pixel_to_meter(15), restitution = 1.2, density = 2, friction = 0, userData = self)


		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		self.impulse = (vec[0]*self.power, vec[1]* self.power)
		

		Projectile.__init__(self, self.world, owner, self.size, pos, self.impulse,bullet= True, image0 = self.image0, lifetime = 15, boxShape = False)


