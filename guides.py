''' GUIDE : 
  Armes
  ------------------------------------------------------------------------------------



  	1. faire weapon et dependencies(ex projectile) dans b2_weapons
  		template'''

 class WeaponName(Weapon):
	name = 'ShortDisplayName' # =========> le Name doit etre 'petit' (moins de jsais pas 10 characters) sinon ca bug jsuis flemmé de faire un truc pour le text:)
	start_range = 5
	weapon_range = 2000
	def __init__(self, owner, power = 20, cooldown = 0.0 ): # power = force a laquelle l'item est projeté
		Weapon.__init__(self, owner, self.weapon_range)
		
		self.power =power
		self.cooldown = cooldown

	def activate(self, mousePos):
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery) #calcule le vecteur entre le cursor et le owner de l'arme (pour la direction et position)
		
		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1]) # position = position de l'owner + la startrange (dans la direction de la souris par vec)
		Projectile_BouncingBall(self.owner, pos, power= self.power) #init du projectile avec pos et power








	''' 2. dans images/icons ajouter l'icone format 40x40
			icones trouvables http://game-icons.net/tags.html
			ou dans le dossier images/789balblalba
	'''







 	''' 3. dnas GUI.WeaponIcon ajouter le weapon
 		template :'''
 class WeaponIcon(Icon):

	def __init__(self, pos, weapon = None):

		

		if self.weapon.__class__.__name__ == 'Rifle' :
			imagepath = 'images/icons/rifle_icon.png'
		elif self.weapon.__class__.__name__== 'BaseballBat' :
			imagepath = 'images/icons/baseballbat_icon.png'


		''' ===================== ZONE A RAJOUTER ========================= '''
		elif self.weapon.__class__.__name__== 'ClassName' : #<====== attention la c'est la ClassName en string pas le name (sinon c'est bancal)
			imagepath = 'images/icons/weaponname_icon.png' #<==================== le nom de l'image en miniscule_icon si possible (je prefere metre tout en minuscule sans espaces sans caraacteres 
														#							speciaux blablba tout ce qui touche a la gestion de fichier sur le disque pour eviter toute relouterie)
		''' ===================== ZONE A RAJOUTER ========================= '''

		









	'''
 		4. pour test dans main : ajouter a la list weapons1
 		alentours du truc xD:
 	'''
 	# --------------------------------------------------------
	# --- Game setup -----------------------------------------
	mainLoop = True
	player = Player(_world, (600,400))
	# vampire1 = Vampire(_world, (800, 400), target = player)
	zombie = Zombie(_world, (800,400), target =player)
	Zombie(_world, (900,300), target =player)
	Zombie(_world, (1100,400), target =player)
	Zombie(_world, (1000,200), target =player)
	scrollx = 0
	scrolly = 0


	'''========================= C ICI KIKOU ================================================================================================================================'''
	weapons1 = [Rifle(player), Hadouken(player), BaseballBat(player), megaBall(player),GrapplingHook(player), Grenade(player), BouncingBall(player)] # Key_X cycle la liste, (Key_W cycle la liste weapons2)
	'''====================================================================================================================================================================='''


	weapons2 = [megaBall(player),GrapplingHook(player), Grenade(player)]
	weapon1_index = 0
	weapon2_index = 0
	player.weapon1 = weapons1[0]
	player.weapon2 = weapons2[2]

	gui = GUI.GameGUI(_world, ground, player)




	while mainLoop :
 		milliseconds = clock.tick(TARGET_FPS)
		seconds = milliseconds / 1000.0