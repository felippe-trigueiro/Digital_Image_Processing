'''
Autor: Felippe Trigueiro Angelo

This code just tests the interpolation methods described in the interpolation_methods.py file.
The nearest neighbor method is referred as ne
The bilinear method is referred as bl
The bicubic method is referred as bc
The lagrange method is referred as la 
'''

from skimage import io
import numpy as np
from skimage import color
import matplotlib.pyplot as plt
import sys
import os.path
import interpolation_methods

operation = sys.argv[1]
if (operation == '-d'):
    width = float(sys.argv[2])
    height = float(sys.argv[3])
    interpolationMode = sys.argv[4]
    inputImage = sys.argv[5]
    outputImage = sys.argv[6]
    parameter = None 
else:
    parameter = float(sys.argv[2])
    interpolationMode = sys.argv[3]
    inputImage = sys.argv[4]
    outputImage = sys.argv[5]
    width = None
    height = None

#Verifica se a pasta de saída existe e a cria se necessário
if not os.path.exists(os.getcwd() + '/Output_Images/'): 
    os.makedirs(os.getcwd() + '/Output_Images/')

if(os.path.isfile(inputImage)):
    if(operation == '-d' or operation == '-a' or operation == '-e' or operation == '-m' or 
       operation == '-i' or operation == '-o'):
        if (outputImage[outputImage.find('.'):len(outputImage)] != '.png'):
            print("A imagem de saída deve estar no formato .png.")
            exit()

        inpImage = io.imread(inputImage)

        iHeigh = inpImage.shape[0]
        iWidth = inpImage.shape[1]

        if (operation == '-d' and interpolationMode == 'ne'):
            sx = width/iWidth
            sy = height/iHeigh

            outImage = interpolation_methods.nearest_neighbor(inpImage, sx, sy, None)
        elif (operation == '-a' and interpolationMode == 'ne'):
            outImage = interpolation_methods.nearest_neighbor(inpImage, None, None, parameter)
        elif (operation == '-e' and interpolationMode == 'ne'):
            outImage = interpolation_methods.nearest_neighbor(inpImage, parameter, parameter, None)
        elif (operation == '-d' and interpolationMode == 'bl'):
            sx = width/iWidth
            sy = height/iHeigh

            outImage = interpolation_methods.bilinear(inpImage, sx, sy, None)
        elif (operation == '-a' and interpolationMode == 'bl'):
            outImage = interpolation_methods.bilinear(inpImage, None, None, parameter)
        elif (operation == '-e' and interpolationMode == 'bl'):
            outImage = interpolation_methods.bilinear(inpImage, parameter, parameter, None)
        elif (operation == '-d' and interpolationMode == 'bc'):
            sx = width/iWidth
            sy = height/iHeigh

            outImage = interpolation_methods.bicubic(inpImage, sx, sy, None)
        elif (operation == '-a' and interpolationMode == 'bc'):
            outImage = interpolation_methods.bicubic(inpImage, None, None, parameter)
        elif (operation == '-e' and interpolationMode == 'bc'):
            outImage = interpolation_methods.bicubic(inpImage, parameter, parameter, None)
        elif (operation == '-d' and interpolationMode == 'la'):
            sx = width/iWidth
            sy = height/iHeigh

            outImage = interpolation_methods.lagrange(inpImage, sx, sy, None)
        elif (operation == '-a' and interpolationMode == 'la'):
            outImage = interpolation_methods.lagrange(inpImage, None, None, parameter)
        elif (operation == '-e' and interpolationMode == 'la'):
            outImage = interpolation_methods.lagrange(inpImage, parameter, parameter, None)
        
        plt.subplot(1, 2, 1)
        plt.imshow(inpImage, cmap='gray')
        plt.xlabel("Imagem Original")

        plt.subplot(1, 2, 2)
        plt.imshow(outImage, cmap='gray')
        plt.xlabel("Imagem Interpolada")

        plt.show()

        io.imsave(os.getcwd() + '/Output_Images/' + outputImage, outImage)    
    else:
        print("Selecione uma operação válida!")
        print("[-a ângulo].")
        print("[-e fator de escala]")
        print("[-d largura altura]")
        print("[-m interpolação]")
        print("[-i imagem]")
        print("[-o imagem]")
else:
    print("A imagem " + inputImage + " não foi encontrada!")