from math import *
from arcade.math import *

def magnitude(num):
    return sqrt(num**2)
    
def normalized(num):
    mag = magnitude(num)
    if mag == 0:
        return 0
    return num / mag

def magnitude2D(num1,num2):
    return sqrt(num1**2 + num2**2)

def normalized2D(X,y):
    mag = magnitude2D(X,y)
    if mag == 0:
        return (0, 0)
    return (X / mag, y / mag)

def GetDist(pointStart,pointEnd):
    return magnitude(pointEnd - pointStart)

def GetPointInCircle(degrees,radius,pointX,pointY):
    x = pointX + radius  * cos(radians(degrees))       
    y = pointY - radius  * sin(radians(degrees))
    return x,y 

def GetPointInCircleFlatten(degrees,radius,pointX,pointY,digit = 0):
    x = pointX + radius  * round(cos(radians(degrees)), digit)     
    y = pointY - radius  * round(sin(radians(degrees)), digit)
    return x,y

