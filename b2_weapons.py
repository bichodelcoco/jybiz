# -*- coding: utf-8 -*-
'''pour que python casse pas les couilles avec les accents !! éééééèèèèè'''
from b2_classes import *

class Weapon(object):
	def __init__(self, owner, weapon_range, cooldown = 0.0):
		self.owner = owner
		self.weapon_range = weapon_range
		self.cooldown = cooldown

	def deactivate(self, mousePos):
		pass

class Projectile(GameObject):
	''' PROJECTILE.IMAGE0 SHOULD BE HORIZONTAL FACING RIGHT'''

	def __init__(self, world, owner, size, startingPos,  startingImpulse, bullet=False, image0= None,lifetime = -1, density=1,
	 boxShape = True, angle = 0,collisiondamage = 0.1, damage = 5,targetGroup = enemyGroup):
		self.world = world
		self.owner = owner
		self.startingPos = startingPos
		self.size = size
		self.startingImpulse = startingImpulse
		self.lifetime= lifetime
		self.alivetime = 0.0
		self.targetGroup = targetGroup
		self.collisiondamage = collisiondamage
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

			for unit in collidegroup :

				self.hit(unit)

	def die(self):
		self.kill()

	def hit(self, unit):
		collisionspeed = geo.absolute(self.vel.x+unit.vel.x + self.vel.y+unit.vel.y)
		unit.loseHitpoints(collisionspeed*self.collisiondamage+self.damage)



# bat
#-----------------------------------------------------------------------------------------------
class BaseballBat(Weapon):
	name = 'Bat'
	def __init__(self, owner, power= 1000, aoe = (100,100), weapon_range = 150, maxChargeTime = 6.0, maxDamage = 100):
		Weapon.__init__(self,owner, weapon_range)
		self.power = power
		self.aoe = aoe
		self.timer = Timer()
		self.maxChargeTime = maxChargeTime
		self.activated = False
		self.maxDamage = maxDamage
	def activate(self, mousePos):
		self.timer.reset()
		g.TIMERS.append(self.timer)
		self.activated = True


	def deactivate(self, mousePos):
		if self.activated :
			chargeTime = geo.minimum(self.timer.elapsedTime, self.maxChargeTime)
			g.TIMERS.remove(self.timer)

			chargeStr = geo.maximum(chargeTime / self.maxChargeTime, 0.1)



			area = AOE(mousePos, self.aoe)
			collidegroup = pygame.sprite.spritecollide(area, enemyGroup, False)
			vec = geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)
			for item in collidegroup :
				item.body.ApplyLinearImpulse(pygameVec_to_box2dVec((vec[0]*self.power*chargeStr,vec[1]*self.power*chargeStr)), item.fixture.body.worldCenter, wake = True)
				item.loseHitpoints(chargeStr*2 * self.maxDamage)
			area.kill()
			self.activated = False

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
	def __init__(self, owner, pos, power = 40, blast_aoe = (200,200),blast_power = 500, collisiondamage = 0.1, damage = 0):
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

		Projectile.__init__(self, owner.world,owner, Grenade.size, startingPos, self.impulse, image0 = Projectile_Grenade.image0,lifetime = 3, collisiondamage= collisiondamage, damage = damage)


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
	start_range = 5
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
	def __init__(self, owner, pos, power = 150, collisiondamage = 0.1, damage = 1):
		# image loading management
		if Projectile_Rifle.image0 == None :
			Projectile_Rifle.image0 = pygame.Surface((5,5))
			Projectile_Rifle.image0.fill(BLACK)
			Projectile_Rifle.image0.set_colorkey(WHITE)
		#--------------------------


		self.power = power

		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		self.impulse = (vec[0]*power, vec[1]*power)
		startingPos = (vec[0]*Rifle.start_range +owner.pos[0], vec[1]*Rifle.start_range+ owner.pos[1])

		Projectile.__init__(self, owner.world,owner, Rifle.size, startingPos, self.impulse, bullet=True, image0 = Projectile_Rifle.image0,
			lifetime = 1, density=20,collisiondamage = collisiondamage, damage = damage)


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
	def __init__(self, owner, pos, power = 20000, blast_aoe = (210,210), blast_power = 10, collisiondamage = 0, damage = 0):


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

		Projectile.__init__(self, owner.world, owner, megaBall.size, startingPos, self.impulse, image0 = Projectile_megaBall.image0,lifetime = 5, density=500, collisiondamage = collisiondamage, damage = damage)

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

	def __init__(self, owner, pos, speed = 5, power = 800, recoil = 10, collisiondamage = 1, damage = 20):

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

		Projectile.__init__(self, self.world, owner, self.size, startingPos, self.impulse,bullet= True, image0 = self.image0,
		 lifetime = 1.5, boxShape = False,collisiondamage = collisiondamage, damage = damage)

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
		hook = Hook(self.owner, mousePos, self.pull_power)
		self.garbage_bin.append(hook)

	def deactivate(self, mousePos):
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

	def kill(self):
		self.latched = False
		pygame.sprite.Sprite.kill(self)


# Bouncing Ball
#----------------------------------------------------------------------------------------------------------
class BouncingBall(Weapon):
	name = 'Bouncing'
	start_range = 20
	weapon_range = 2000
	def __init__(self, owner, power = 500, cooldown = 0.0 ):
		Weapon.__init__(self, owner, self.weapon_range)

		self.power =power
		self.cooldown = cooldown

	def activate(self, mousePos):
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)

		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1])
		Projectile_BouncingBall(self.owner, pos, power= self.power)

#Boucing ball projectile
#----------------------------------------------------------------------------------------
class Projectile_BouncingBall(Projectile):
	image0 = None
	size = (30,30)

	def __init__(self, owner, pos,power = 500, collisiondamage = 1, damage = 0):

		vec = (pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		if vec[1] <= 0:
			self.angle =geo.vecAngle((1,0), vec)
		else :
			self.angle = -geo.vecAngle((1,0), vec)

		# image loading management
		if Projectile_BouncingBall.image0 == None :
			Projectile_BouncingBall.image0= pygame.image.load('images/weapons/bouncingball.png').convert()
			#Projectile_BouncingBall.image0 = pygame.transform.rotate(Projectile_BouncingBall.image0, self.angle)
			setColorkey(Projectile_BouncingBall.image0)


		#--------------------------

		self.power = power


		self.world = owner.world
		self.body = self.world.CreateDynamicBody(position = pygame_to_box2d(pos), bullet = True, angle = self.angle)
		self.fixture = self.body.CreateCircleFixture(radius = real_pixel_to_meter(15), restitution = 1.2, density = 2, friction = 0, userData = self)


		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		self.impulse = (vec[0]*self.power, vec[1]* self.power)


		Projectile.__init__(self, self.world, owner, self.size, pos, self.impulse,bullet= True, image0 = self.image0, lifetime = 15, boxShape = False,collisiondamage = collisiondamage, damage = damage)



# Fragmented Ball
#-------------------------------------------------------------------------------------
class FragmentedBall(Weapon):
	name = 'Frag' # =========> le Name doit etre 'petit' (moins de jsais pas 10 characters) sinon ca bug jsuis flemmé de faire un truc pour le text:)
	start_range = 5
	weapon_range = 2000
	def __init__(self, owner, power = 1000, cooldown = 0.0 ): # power = force a laquelle l'item est projeté
		Weapon.__init__(self, owner, self.weapon_range)

		self.power =power
		self.cooldown = cooldown

	def activate(self, mousePos):
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery) #calcule le vecteur entre le cursor et le owner de l'arme (pour la direction et position)

		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1]) # position = position de l'owner + la startrange (dans la direction de la souris par vec)
		Projectile_FragmentedBall1(self.owner, pos) #init du projectile avec pos et power


# Fragmented Ball Projectile 1
#-------------------------------------------------------------------------------------
class Projectile_FragmentedBall1(Projectile):
	image0 = None
	size = (48,48)

	def __init__(self, owner, pos,power = 1000, collisiondamage = 10, damage = 0):

		vec = (pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		if vec[1] <= 0:
			self.angle =geo.vecAngle((1,0), vec)
		else :
			self.angle = -geo.vecAngle((1,0), vec)

		# image loading management
		if Projectile_FragmentedBall1.image0 == None :
			Projectile_FragmentedBall1.image0= pygame.image.load('images/weapons/fragBall1_48.png').convert()
			setColorkey(Projectile_FragmentedBall1.image0)


		#--------------------------

		self.power = power

		self.world = owner.world
		self.body = self.world.CreateDynamicBody(position = pygame_to_box2d(pos), angle = self.angle)
		self.fixture = self.body.CreateCircleFixture(radius = real_pixel_to_meter(24), density = 5, friction = 0, userData = self)


		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		self.impulse = (vec[0]*self.power, vec[1]* self.power)


		Projectile.__init__(self, self.world, owner, self.size, pos, self.impulse, image0 = self.image0, lifetime = 0.1, boxShape = False,collisiondamage = collisiondamage, damage = damage)


	def die(self):


		for i in [-1,0,1]:
			frag_angle=i*(math.pi/4)
			end_pos_frag=self.pos[:]
			Projectile_FragmentedBall2(self.owner, end_pos_frag, frag_angle=frag_angle) #utiliser angle_frag pour l'angle dans fragball2


		Projectile.die(self)



# Fragmented Ball projectile 2
#-------------------------------------------------------------------------------------
class Projectile_FragmentedBall2(Projectile):
	image0 = None

	def __init__(self, owner, pos,power = 333, collisiondamage = 10, damage = 0, frag_angle=0, second_round=False):
		if second_round==False:
			self.size = (32,32)
		else:
			self.size=(16,16)

		vec = (pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		if geo.vectorLength(vec[0],vec[1]) == 0:
			self.angle = 0
		elif vec[1] <= 0:
			self.angle =geo.vecAngle((1,0), vec)
		else :
			self.angle = -geo.vecAngle((1,0), vec)

		# image loading management
		if Projectile_FragmentedBall2.image0 == None or second_round==False:
			Projectile_FragmentedBall2.image0= pygame.image.load('images/weapons/fragBall2_32.png').convert()
			setColorkey(Projectile_FragmentedBall2.image0)
		elif second_round==True:
			Projectile_FragmentedBall2.image0= pygame.image.load('images/weapons/fragBall2_16.png').convert()
			setColorkey(Projectile_FragmentedBall2.image0)

		#--------------------------

		self.second_round=second_round
		self.world = owner.world
		temp_pos=pygame_to_box2d(pos)
		self.body = self.world.CreateDynamicBody(position = temp_pos, angle = self.angle)
		if second_round==False:
			self.fixture = self.body.CreateCircleFixture(radius = real_pixel_to_meter(16), density = 10, friction = 0, userData = self)
			self.power = power*2
		else:
			self.fixture = self.body.CreateCircleFixture(radius = real_pixel_to_meter(8), density = 10, friction = 0, userData = self)
			self.power=power

		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])

		rotated=geo.rotation(vec, frag_angle)

		self.impulse = rotated[0]*self.power, rotated[1]*self.power

		if second_round==False:
			Projectile.__init__(self, self.world, owner, self.size, pos, self.impulse, image0 = self.image0, lifetime = 0.2, boxShape = False,collisiondamage = collisiondamage, damage = damage)
		else:
			Projectile.__init__(self, self.world, owner, self.size, pos, self.impulse, image0 = self.image0, lifetime = 0.4, boxShape = False,collisiondamage = collisiondamage, damage = damage)

	def die(self):
		if self.second_round==False:
			for i in [-1,0,1]:
				frag_angle=i*(math.pi/4)
				end_pos_frag=self.pos[:]
				Projectile_FragmentedBall2(self.owner, end_pos_frag, frag_angle=frag_angle, second_round=True) #utiliser angle_frag pour l'angle dans fragball2

			Projectile.die(self)
		else:
			Projectile.die(self)


# Mini Bouncing Ball
#----------------------------------------------------------------------------------------------------------
class MiniBouncingBall(Weapon):
	name = 'MiniBounce'
	start_range = 20
	weapon_range = 2000
	def __init__(self, owner, power = 500, cooldown = 0.0 ):
		Weapon.__init__(self, owner, self.weapon_range)

		self.power =power
		self.cooldown = cooldown

	def activate(self, mousePos):
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)

		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1])
		Projectile_MiniBouncingBall(self.owner, pos, power= self.power)

#Mini Boucing ball projectile
#----------------------------------------------------------------------------------------
class Projectile_MiniBouncingBall(Projectile):
	image0 = None
	size = (10,10)

	def __init__(self, owner, pos,power = 500, collisiondamage = 1, damage = 0):

		vec = (pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		if vec[1] <= 0:
			self.angle =geo.vecAngle((1,0), vec)
		else :
			self.angle = -geo.vecAngle((1,0), vec)

		# image loading management
		if Projectile_MiniBouncingBall.image0 == None :
			Projectile_MiniBouncingBall.image0= pygame.image.load('images/weapons/minibouncingball.png').convert()
			#Projectile_MiniBouncingBall.image0 = pygame.transform.rotate(Projectile_MiniBouncingBall.image0, self.angle)
			setColorkey(Projectile_MiniBouncingBall.image0)


		#--------------------------

		self.power = power


		self.world = owner.world
		self.body = self.world.CreateDynamicBody(position = pygame_to_box2d(pos), bullet = True, angle = self.angle)
		self.fixture = self.body.CreateCircleFixture(radius = real_pixel_to_meter(5), restitution = 1.2, density = 2, friction = 0, userData = self)


		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		self.impulse = (vec[0]*self.power, vec[1]* self.power)


		Projectile.__init__(self, self.world, owner, self.size, pos, self.impulse,bullet= True, image0 = self.image0, lifetime = 15, boxShape = False,collisiondamage = collisiondamage, damage = damage)

''' ===== ENEMY UNIT WEAPONS =============================================================================================================================================='''
''' ======================================================================================================================================================================='''
# often player weapons slightly customized
# Melee Hit, a general enemy weapon for all melee units
# ------------------------------------------------------------------------------------------------------------------
class MeleeHit(Weapon):
	name = 'Melee'

	def __init__(self, owner, power = 2000, weapon_range = 100, cooldown = 3.0):
		Weapon.__init__(self,owner, weapon_range)
		self.power = power

	#pousse le target selon le vecteur
	def activate(self, target):
		vec = geo.normalizeVector(target.pos[0] - self.owner.pos[0],target.pos[1] - self.owner.pos[1])

		target.body.ApplyForce((vec[0]*self.power, vec[1]*self.power),target.body.worldCenter, wake = True)





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
	def __init__(self, owner, pos, power = 150,collisiondamage = 0.1, damage = 1, targetGroup = playerGroup):
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

		Projectile.__init__(self, owner.world,owner, self.size, startingPos, self.impulse, bullet=True,
			image0 = Projectile_VampireRifle.image0,lifetime = 1, density=20, targetGroup = targetGroup,collisiondamage = collisiondamage, damage = damage)


	def update(self, seconds):

		Projectile.update(self,seconds)
