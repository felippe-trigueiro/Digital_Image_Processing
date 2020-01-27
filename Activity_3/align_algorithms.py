'''Arquivo contendo as funções que executam os algoritmos de alinhamento dos textos

A função align_projection, realiza o alinhamento por meio da projeção horizontal da imagem
e depois disso maximiza uma função objetivo, que nesse caso é o erro quadrático.

A função align_hough, realiza o alinhamento por meio da transformada de Hough.

Autor: Felippe Trigueiro Angelo
'''

import numpy as np
from skimage import color, transform, filters, feature, io
import matplotlib.pylab as plt

def border_remove (transformedImage):
    transformedImage2 = np.copy(transformedImage)
    transformedImage3 = np.copy(transformedImage)
    transformedImage2[transformedImage2 == 0] = 1
    
    transImGray = color.rgb2gray(transformedImage2)
    BintransImage = transImGray <= 0.8
    BintransImage = BintransImage*1
    
    projHori = np.sum(BintransImage, axis=1) #Soma os valores de uma linha
    projVert = np.sum(BintransImage, axis=0) #Soma os valores de uma coluna

    #Seleciona um retângulo que contenha o texto
    #Nos vetores de projeção, os valores iniciais são baixos devido haverem uma maioria de pixels
    #brancos (branco = 0 nas imagens binárias). Assim, os valores que passam esse limiar são 
    #tratados como texto e não como borda resultante da rotação
    projHori[projHori < 40 ] = 0 
    projVert[projVert < 14 ] = 0

    sup = np.argmax(projHori > 0) + 1
    left = np.argmax(projVert > 0) + 1

    projHori = projHori[::-1]
    projVert = projVert[::-1]

    inf = np.argmax(projHori > 0) + 1
    right = np.argmax(projVert > 0) + 1

    #Muda a região de fora do retângulo para 1
    transformedImage3[0:(sup-2), :] = 1
    transformedImage3[:, 0:(left-2)] = 1
    transformedImage3[(2-inf):, :] = 1
    transformedImage3[:, (4-right):] = 1

    return transformedImage3

def align_projection(input_Image): 
    monImage = color.rgb2gray(input_Image)
    
    maxHistRotate = np.zeros(2) #Armazena o erro máximo e o respectivo ângulo de rotação
    for k in range(1, 181):
        binImRotate = transform.rotate(monImage, k)
        binImRotate = binImRotate <= 0.8
        binImRotate = binImRotate*1
        
        projHist = np.sum(binImRotate, axis=1)

        #Cálculo das diferenças entre células adjacentes da projeção
        difProj = projHist[0:(len(projHist)-1)] - projHist[1:len(projHist)]
        squareError = np.sum(difProj*difProj)

        #Verifica qual o erro máximo
        if(squareError > maxHistRotate[0]):
            maxHistRotate[0] = squareError
            maxHistRotate[1] = k
    
    angle = maxHistRotate[1]
    if (angle > 90 and angle < 180):
       angle = angle + 180

    transformedImage = transform.rotate(input_Image, angle, resize=True)

    #Pós processamento para evitar as bordas resultates da rotação
    transformedImage = border_remove(transformedImage)

    return transformedImage, angle

def align_hough(input_Image):
    #Converte a imagem do padrão RGB para uma imagem binária
    monImage = color.rgb2gray(input_Image)
    monImage = feature.canny(monImage)

    houghTransform, angles, d = transform.hough_line(monImage, theta = np.linspace(-np.pi/2, np.pi/2, 180))
    hTP, angles, d = transform.hough_line_peaks(houghTransform, angles, d)

    angles = np.rad2deg(angles) + 90
    angles = np.round(angles, 0)
    angles = angles.astype(int)
    
    angle = np.bincount(angles).argmax()

    if (angle > 90 and angle < 180):
        angle = angle + 180

    transformedImage = transform.rotate(input_Image, angle, resize=True)

    #Pós processamento para remoção das bordas resultantes da rotação
    transformedImage = border_remove(transformedImage)

    return transformedImage, angles[0]