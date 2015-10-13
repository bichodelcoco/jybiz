''' GUIDE : 
  Armes
  ------------------------------------------------------------------------------------



  	1. faire weapon et dependencies(ex projectile) dans b2_weapons
  		template'''

 class WeaponName(Weapon):
	name = 'ShortDisplayName' # =========> le Name doit etre 'petit' (moins de jsais pas 10 characters) sinon ca bug jsuis flemmé de faire un truc pour le text:)
	
	def __init__(self, owner, power = 20, cooldown = 0.0 ): # power = force a laquelle l'item est projeté
	

	def activate(self, mousePos):
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery) #calcule le vecteur entre le cursor et le owner de l'arme (pour la direction et position)
		
		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1]) # position = position de l'owner + la startrange (dans la direction de la souris par vec)
		Projectile_BouncingBall(self.owner, pos, power= self.power) #init du projectile avec pos et power





	''' 2. dans images/icons ajouter l'icone format 40x40
			icones trouvables http://game-icons.net/tags.html
			ou dans le dossier images/789balblalba
	'''




 	''' 3. dnas GUI.WeaponIcon.__init__ ajouter le weapon
 		template :'''
 
		elif self.weapon.__class__.__name__== 'ClassName' : #<====== attention la c'est la ClassName en string pas le name (sinon c'est bancal)
			imagepath = 'images/icons/weaponname_icon.png' #<==================== le nom de l'image en miniscule_icon si possible (je prefere metre tout en minuscule sans espaces sans caraacteres 
														#							speciaux blablba tout ce qui touche a la gestion de fichier sur le disque pour eviter toute relouterie)
		



	'''
 		4. pour test dans main : ajouter a la list weapons1
 		alentours du truc xD:
 	'''
 

	weapons1 = [Rifle(player), Hadouken(player), BaseballBat(player), megaBall(player),GrapplingHook(player), Grenade(player), BouncingBall(player)] # Key_X cycle la liste, (Key_W cycle la liste weapons2)




""" ================================================================================================================================================================================================="""
""" ================================================================================================================================================================================================="""
	
	"""MonsterSpawn.monsterValues  teamplates
	   ----------------------------------------------"""
	#Pour les MonsterSpawn :
	MonsterSpawn(self,world, pos, monsterClass,monsterValues = [], monster_cooldown = 10.0, duration = -1, online = False)

	"""si monsterValues pas assigné ca fait les valeurs par defaut du monsterValues
		sinon on peut mettre une liste monsterValues qui doivent absolument respecter ces templates :

	1. Skull"""

		monsterValues = [attack_range , maxSpeed, accel , target]

	"""
	2. Zombie """
		monsterValues = [maxSPeed, accel, target]

	"""
	2. Vampire """
		monsterValues = [maxSPeed, accel, target]



















































