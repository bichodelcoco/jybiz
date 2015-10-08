'''
gestion des vecteurs, de la geometrie etc
'''
import math

def vectorLength(x, y):
    return math.sqrt(x*x + y*y)

def vecLength(vec):
	return vectorLength(vec[0], vec[1])

def vecProduct(vec1,vec2):
	return vec1[0]*vec2[0]+vec1[1]*vec2[1]

def vecAngle(a,b):
	product = vecProduct(a,b)

	return math.acos(product/(vecLength(a)*vecLength(b)))

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

def distance_oneDim(a,b):
	return abs(a-b)


#def write(msg, color):

def diagonalDistance(a,b) : #Movement cost D = 10, diagonal 14 (aprrox sqrt(2)*D)
	dx = abs(a[0] - b[0])
	dy = abs(a[1] - b[1])
	return 10*(dx+dy)- 6*min(dx,dy) #formula is D*(dx+dy) - (sqrt(2)*D - 2*D)*min(dx,dy)

def absolute(a):
	return abs(a)
def maximum(a,b):
	return max(a,b)
def minimum(a,b):
	return min(a,b)

def rotation((a,b),theta):
    return (a*math.cos(theta)-b*math.sin(theta), a*math.sin(theta)+b*math.cos(theta)) ''' /!\ theta must be in rad not degrees'''
