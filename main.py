from random import *
import pygame
from pygame.locals import *

import Box2D
from Box2D.b2 import * # maps b2Vec b2World to vec, world etc

from b2_classes import *


# Constants
# -----------------------------------------------------------

# class Config(object):
# 	_world = world(gravity=(0,-10),doSleep=True)

# Utility functions
# ----------------------------------------------------------

def pygame_to_box2d(pygame_position):
	return pygame_position[0]/PPM,(SCREEN_HEIGHT - pygame_position[1])/PPM



def main():

	# Pygame set up
	# -----------------------------------------------------------
	screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), 0, 32)
	pygame.display.set_caption('Simple pygame example')
	clock=pygame.time.Clock()
	seed()

	bigmap = pygame.Surface((g.BIGMAP_WIDTH, g.BIGMAP_HEIGHT))
	bigmap.fill(WHITE)
		# ------- create background ---------------- subsurface of bigmap (what will be on the screen)
	background = pygame.Surface(screen.get_size()) #surface the size of the screen
	backgroundRect = background.get_rect() #create rectangle the size of background/the screen
	background = bigmap.subsurface((g.CORNERPOINT[0], g.CORNERPOINT[1], SCREEN_WIDTH, SCREEN_HEIGHT)) #take snapshot of bigmap
	background = background.convert()



	# --- pybox2d world setup -----------------------------------
	# Create the world
	_world = world(gravity=(0,-10),doSleep=True)

	# And a static body to hold the ground shape
	ground= StaticObject(_world, (0, g.BIGMAP_HEIGHT - 20), (g.BIGMAP_WIDTH,15))
	leftEdge = StaticObject(_world, (0,0), (20, g.BIGMAP_HEIGHT))
	rightEdge = StaticObject(_world, (g.BIGMAP_WIDTH,0), (20, g.BIGMAP_HEIGHT))
	roof = StaticObject(_world, (0,0), (g.BIGMAP_WIDTH, 20))

	# add a crate

	crate = Crate( _world,(400,400))
	crate2 = Crate( _world,(200,400), (100,20))
	for i in xrange(200):
		Crate(_world, (randint(0, 700), randint(0, 400)))
	ledge = Ledge(_world, ground, leftpoint = (800,600), width = 400)
	Ledge(_world, ground, leftpoint = (200,200), width = 500)
	Ledge(_world, ground, leftpoint = (500,250), width = 500)


	# --------------------------------------------------------
	# --- Game setup -----------------------------------------
	mainLoop = True
	player = Player(_world, (200,200))
	goingRight = False
	goingLeft = False
	frames = 0
	scrollx = 0
	scrolly = 0

	weapons = [rifle(player), Hadouken(player), BaseballBat(player), GrapplingHook(player)]
	weapon_index = 0




	while mainLoop :
 		milliseconds = clock.tick(TARGET_FPS)
		seconds = milliseconds / 1000.0


		for event in pygame.event.get():
			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				mainLoop = False

			elif event.type == KEYDOWN :
				if event.key == K_d :
					goingRight = True
				elif event.key == K_q :
					goingLeft = True
				if event.key == K_SPACE :
					player.jump()
				elif event.key == K_s :
					player.slowing = True
				elif event.key == K_z :
					player.stand()

			elif event.type == KEYUP:
				if event.key == K_d :
					goingRight = False
				elif event.key == K_q :
					goingLeft = False
				elif event.key == K_s :
					player.slowing = False
				elif event.key == K_x :
					weapon_index = (weapon_index +1) % len(weapons)
					player.weapon = weapons[weapon_index]


			if event.type == MOUSEMOTION :
				cursor.update()

			if event.type == MOUSEBUTTONDOWN :
				if event.button == 1:
					g.LEFT_CLICK = True
					if geo.distance(player.pos, cursor.pos) <= player.weapon.weapon_range :
						player.left_click(cursor.rect.topleft)
				elif event.button == 4 :
					player.rotateLeft()
				elif event.button == 5 :
					player.rotateRight()
			elif event.type == MOUSEBUTTONUP :
				if event.button == 1:
					g.LEFT_CLICK = False
					player.weapon.deactivate()

		# if pygame.sprite.spritecollideany(player.feet, ledgeGroup):
		# 	player.onLedge = True
		# else :
		# 	player.onLedge = False


		if goingRight :
			player.goRight()

		elif goingLeft :
			player.goLeft()


		# -------- Scrolling  with keyboard------------------
		
		pressedKeys = pygame.key.get_pressed()
		# what happens when u press an arrow to move screen
		if pressedKeys[K_LEFT]:
			scrollx -= g.scrollStepx
		if pressedKeys[K_RIGHT]:
			scrollx += g.scrollStepx
		if pressedKeys[K_DOWN]:
			scrolly += g.scrollStepy
		if pressedKeys[K_UP]:
			scrolly -= g.scrollStepy
		# ---- scroll the screen --------
		g.CORNERPOINT[0] += scrollx
		g.CORNERPOINT[1] += scrolly
		#----- prevent scrolling out of the map
		if g.CORNERPOINT[0] < 0:
			g.CORNERPOINT[0]=0
			scrollx = 0
		elif g.CORNERPOINT[0] > g.BIGMAP_WIDTH - SCREEN_WIDTH :
			g.CORNERPOINT[0] = g.BIGMAP_WIDTH - SCREEN_WIDTH
			scrollx = 0
		if g.CORNERPOINT[1] < 0:
			g.CORNERPOINT[1] = 0
			scrolly = 0
		elif g.CORNERPOINT[1] > g.BIGMAP_HEIGHT - SCREEN_HEIGHT :
			g.CORNERPOINT[1] = g.BIGMAP_HEIGHT - SCREEN_HEIGHT
			scrolly =0



		# ---- update shit and draw allGroup ----------------
		background = bigmap.subsurface((g.CORNERPOINT[0], g.CORNERPOINT[1], SCREEN_WIDTH, SCREEN_HEIGHT))
		screen.blit(background, (0,0))
		allGroup.update(seconds)

		# destroy bodies out of the time step else issues
		for body in g.TO_DESTROY :
			_world.DestroyBody(body)
		g.TO_DESTROY = []
		# take a time step in box2d engine
		_world.Step(TIME_STEP, 10, 10)
		allGroup.draw(screen)
		pygame.display.flip()

main()
