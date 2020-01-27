#This function receives the orinal Image and the scales that were used for the transformation.
# The function maps interpolates the pixel values by the nearest neighbor method
#If the transformation is scale put angle as Null
#If the transformation is rotation, put sx and sy as Null

#Author: Felippe Trigueiro Angelo - 210479

import numpy as np
import math

def nearest_neighbor (original_Image, sx, sy, angle):
    
    oWidth = original_Image.shape[1]
    oHeight = original_Image.shape[0]
    
    if (angle == None):
        nHeight = round(oHeight*sy)
        nWidth = round(oWidth*sx)
        
        newImage = np.zeros((nHeight, nWidth))
        
        for l in range(round(nHeight)):
            for c in range(round(nWidth)):
                x = round(c/sx)
                y = round(l/sy)

                if (x == 0):
                    x = 1
                if (y == 0):
                    y = 1

                newImage[l][c] = original_Image[y-1][x-1]

    elif (sx == None and sy == None):
        radAngle = math.radians(angle)
        newImage = np.zeros((oHeight, oWidth))

        mHeight = round(oHeight/2)
        mWidth = round(oWidth/2)

        #Rotation and aligment
        for l in range(oHeight):
            for c in range(oWidth):
                x = round(c*math.cos(radAngle)-l*math.sin(radAngle) - mWidth*math.cos(radAngle) 
                          + mHeight*math.sin(radAngle) + mWidth)
                y = round(l*math.cos(radAngle)+c*math.sin(radAngle) - mWidth*math.sin(radAngle) 
                          - mHeight*math.cos(radAngle) + mHeight)
                
                if (x >= 0 and x < oWidth and y >= 0 and y < oHeight):
                    newImage[l][c] = original_Image[y][x]
    
    newImage = newImage.astype(int)
    return newImage

def bilinear(original_Image, sx, sy, angle):
    oWidth = original_Image.shape[1]
    oHeight = original_Image.shape[0]

    if (angle == None):
        nHeight = round(oHeight*sy)
        nWidth = round(oWidth*sx)
        
        newImage = np.zeros((nHeight, nWidth))

        for l in range(round(nHeight)):
            for c in range(round(nWidth)):
                x = c/sx - 2
                y = l/sy - 2

                dx = math.fabs(round(x) - x)
                dy = math.fabs(round(y) - y)

                fxy = original_Image[round(y)][round(x)]
                fx1y = original_Image[round(y)][round(x+1)]
                fxy1 = original_Image[round(y+1)][round(x)]
                fx1y1 = original_Image[round(y+1)][round(x+1)]

                bil = (1 - dx)*(1-dy)*fxy + dx*(1-dy)*fx1y + (1 - dx)*dy*fxy1 + dx*dy*fx1y1

                newImage[l][c] = bil
    elif (sx == None and sy == None):
        radAngle = math.radians(angle)
        newImage = np.zeros((oHeight, oWidth))

        mHeight = round(oHeight/2)
        mWidth = round(oWidth/2)

        #Rotation and aligment
        for l in range(oHeight):
            for c in range(oWidth):
                x = round(c*math.cos(radAngle)-l*math.sin(radAngle) - mWidth*math.cos(radAngle) 
                          + mHeight*math.sin(radAngle) + mWidth)
                y = round(l*math.cos(radAngle)+c*math.sin(radAngle) - mWidth*math.sin(radAngle) 
                          - mHeight*math.cos(radAngle) + mHeight)
                
                if (x >= 0 and x < oWidth - 1 and y >= 0 and y < oHeight - 1):
                    dx = math.fabs(round(x) - x)
                    dy = math.fabs(round(y) - y)

                    fxy = original_Image[round(y)][round(x)]
                    fx1y = original_Image[round(y)][round(x+1)]
                    fxy1 = original_Image[round(y+1)][round(x)]
                    fx1y1 = original_Image[round(y+1)][round(x+1)]

                    bil = (1 - dx)*(1-dy)*fxy + dx*(1-dy)*fx1y + (1 - dx)*dy*fxy1 + dx*dy*fx1y1

                    newImage[l][c] = bil

    
    newImage = newImage.astype(int)
    return newImage

def p(t):
    if (t > 0):
        return t
    else:
        return 0
    
def r(s):
    return 1/6*(pow(p(s + 2), 3) - 4*pow(p(s + 1), 3) + 6*pow(p(s), 3) - 4*pow(p(s - 1), 3))

def bicubic (original_Image, sx, sy, angle):
    oWidth = original_Image.shape[1]
    oHeight = original_Image.shape[0]
    
    if (angle == None):
        nHeight = round(oHeight*sy)
        nWidth = round(oWidth*sx)
        
        newImage = np.zeros((nHeight, nWidth))
        
        for l in range(round(nHeight)):
            for c in range(round(nWidth)):
                x = c/sx - 2
                y = l/sy - 2

                dx = math.fabs(round(x) - x)
                dy = math.fabs(round(y) - y)

                accum = 0

                for n in range(-1, 3, 1):
                    for m in range(-1, 3, 1):
                        nx = round(x) + m
                        ny = round(y) + n

                        if (nx >= 0 and nx < oWidth and ny >= 0 and ny < oHeight):
                            accum += original_Image[ny][nx]*r(m - dx)*r(dy - n)
                newImage[l][c] = accum            
    elif (sx == None and sy == None):
        radAngle = math.radians(angle)
        newImage = np.zeros((oHeight, oWidth))

        mHeight = round(oHeight/2)
        mWidth = round(oWidth/2)

        #Rotation and aligment
        for l in range(oHeight):
            for c in range(oWidth):
                x = round(c*math.cos(radAngle)-l*math.sin(radAngle) - mWidth*math.cos(radAngle) 
                          + mHeight*math.sin(radAngle) + mWidth)
                y = round(l*math.cos(radAngle)+c*math.sin(radAngle) - mWidth*math.sin(radAngle) 
                          - mHeight*math.cos(radAngle) + mHeight)

                dx = math.fabs(round(x) - x)
                dy = math.fabs(round(y) - y)

                accum = 0

                for n in range(-1, 3, 1):
                    for m in range(-1, 3, 1):
                        nx = round(x) + m
                        ny = round(y) + n

                        if (nx >= 0 and nx < oWidth and ny >= 0 and ny < oHeight):
                            accum += original_Image[ny][nx]*r(m - dx)*r(dy - n)
                newImage[l][c] = accum       

    newImage = newImage.astype(int)        
    return newImage

def L (original_Image, x, y, dx, dy, n):
    oWidth = original_Image.shape[1]
    oHeight = original_Image.shape[0]

    L = 0
    if (x > 1 and x < oWidth - 2 and y > 0 and y < oHeight - 2):
        L = (-dx*(dx-1)*(dx-2)*original_Image[y+n-2][x-1]/6  + 
            (dx+1)*(dx-1)*(dx-2)*original_Image[y+n-2][x]/2 -
            dx*(dx+1)*(dx-2)*original_Image[y+n-2][x+1]/2  +
            dx*(dx+1)*(dx-1)*original_Image[y+n-2][x+2]/6)
    return L

def lagrange (original_Image, sx, sy, angle):
    oWidth = original_Image.shape[1]
    oHeight = original_Image.shape[0]
    
    if (angle == None):
        nHeight = round(oHeight*sy)
        nWidth = round(oWidth*sx)
        
        newImage = np.zeros((nHeight, nWidth))
        
        for l in range(nHeight):
            for c in range(nWidth):
                x = c/sx
                y = l/sy

                dx = math.fabs(round(x) - x)
                dy = math.fabs(round(y) - y)

                aux = round(-dy*(dy-1)*(dy-2)*L(original_Image, round(x), round(y), dx, dy, 1)/6 +
                            (dy+1)*(dy-1)*(dy-2)*L(original_Image, round(x), round(y), dx, dy, 2)/2 - 
                            dy*(dy+1)*(dy-2)*L(original_Image, round(x), round(y), dx, dy, 3)/2 + 
                            dy*(dy+1)*(dy-1)*L(original_Image, round(x), round(y), dx, dy, 4)/6
                           )
                
                if (aux > 255):
                    aux = 255
                elif (aux < 0):
                    aux = 0
                newImage[l][c] = aux
    elif (sx == None and sy == None):
        radAngle = math.radians(angle)
        newImage = np.zeros((oHeight, oWidth))

        mHeight = round(oHeight/2)
        mWidth = round(oWidth/2)

        #Rotation and aligment
        for l in range(oHeight):
            for c in range(oWidth):
                x = round(c*math.cos(radAngle)-l*math.sin(radAngle) - mWidth*math.cos(radAngle) 
                          + mHeight*math.sin(radAngle) + mWidth)
                y = round(l*math.cos(radAngle)+c*math.sin(radAngle) - mWidth*math.sin(radAngle) 
                          - mHeight*math.cos(radAngle) + mHeight)

                dx = math.fabs(round(x) - x)
                dy = math.fabs(round(y) - y)

                aux = round(-dy*(dy-1)*(dy-2)*L(original_Image, round(x), round(y), dx, dy, 1)/6 +
                            (dy+1)*(dy-1)*(dy-2)*L(original_Image, round(x), round(y), dx, dy, 2)/2 - 
                            dy*(dy+1)*(dy-2)*L(original_Image, round(x), round(y), dx, dy, 3)/2 + 
                            dy*(dy+1)*(dy-1)*L(original_Image, round(x), round(y), dx, dy, 4)/6
                           )
                
                if (aux > 255):
                    aux = 255
                elif (aux < 0):
                    aux = 0
                newImage[l][c] = aux

    newImage = newImage.astype(int)
    return newImage


