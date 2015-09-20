'''
gestion des vecteurs, de la geometrie etc
'''
import math

def vectorLength(x, y):
    return math.sqrt(x*x + y*y)

def normalizeVector(x, y):
	norm = vectorLength(x, y)
	if norm == 0:
		return 0, 0
	else :
		return x/norm, y/norm

def distance(a,b):
	s1 = (b[0]-a[0])*(b[0]-a[0])
	s2 = (b[1]-a[1])*(b[1]-a[1])
	return math.sqrt(s1 + s2)
	
#def write(msg, color):

def diagonalDistance(a,b) : #Movement cost D = 10, diagonal 14 (aprrox sqrt(2)*D)
	dx = abs(a[0] - b[0])
	dy = abs(a[1] - b[1])
	return 10*(dx+dy)- 6*min(dx,dy) #formula is D*(dx+dy) - (sqrt(2)*D - 2*D)*min(dx,dy)

def absolute(a):
	return abs(a)