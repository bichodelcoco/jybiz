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
	# --- pybox2d world setup -----------------------------------
	# Create the world
	_world = world(gravity=(0,-10),doSleep=True)

	# And a static body to hold the ground shape
	ground=_world.CreateStaticBody(
	    position=(0,0),
	    shapes=polygonShape(box=(3000/PPM,50/PPM)),
	    )

	# add a crate

	crate = Crate( _world,(400,400))
	crate2 = Crate( _world,(200,400), (100,20))
	for i in xrange(200):
		Crate(_world, (randint(0, 700), randint(0, 400)))
	ledge = Ledge(_world, ground, (800,600), 400)
	Ledge(_world, ground, (200,200), 500)
	Ledge(_world, ground, (500,250), 500)


	# --------------------------------------------------------
	# --- Game setup -----------------------------------------
	mainLoop = True
	player = Player(_world, (200,200))
	goingRight = False
	goingLeft = False
	frames = 0




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

			if event.type == MOUSEMOTION :
				cursor.update()

			if event.type == MOUSEBUTTONDOWN :
				if event.button == 1:
					g.LEFT_CLICK = True
					if geo.distance(player.rect.center, cursor.rect.topleft) <= player.weapon.weapon_range :
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




		screen.fill(WHITE)
		pygame.draw.line(screen,RED, (-3000, SCREEN_HEIGHT - 50), (3000, SCREEN_HEIGHT - 50))
		# for body in _world.bodies:
		# 	for fixture in body.fixtures:
		# 		fixture.shape.draw(body, fixture)



		allGroup.update(seconds)
		# destroy bodies out of the time step else issues
		for body in g.TO_DESTROY :
			_world.DestroyBody(body)
		g.TO_DESTROY = []

		_world.Step(TIME_STEP, 10, 10)
		allGroup.draw(screen)
		pygame.display.flip()

main()
