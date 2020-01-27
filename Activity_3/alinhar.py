'''
Código de teste para os algoritmos de alinhamento de texto
São testadas os algoritmos de alinhamento por projeção horizontal e alinhamento por
Transformada de Hough.

Autor: Felippe Trigueiro Angelo
'''

from skimage import io
import numpy as np
from skimage import color
import matplotlib.pyplot as plt
import sys
import os.path
import align_algorithms

inputImage = sys.argv[1]
mode = int(sys.argv[2])
outputImage = sys.argv[3]

#Verifica se a pasta de saída existe e a cria se necessário
if not os.path.exists(os.getcwd() + '/Output_Images/'): 
    os.makedirs(os.getcwd() + '/Output_Images/')

if(os.path.isfile(inputImage)):
    if(mode >= 1 and mode <= 2):
        if (outputImage[outputImage.find('.'):len(outputImage)] != '.png'):
            print("A imagem de saída deve estar no formato .png.")
            exit()

        inpImage = io.imread(inputImage)

        if (mode == 1): #Projeção Horizontal
            transformedImage, angle = align_algorithms.align_projection(inpImage)

        else: #Hough
            transformedImage, angle = align_algorithms.align_hough(inpImage)

        print("O ângulo de rotação utilizado pelo método escolhido foi: " + str(angle))
        plt.subplot(1, 2, 1)
        plt.imshow(inpImage)
        plt.xlabel("Imagem Original")

        plt.subplot(1, 2, 2)
        plt.imshow(transformedImage)
        plt.xlabel("Imagem Alinhada")

        plt.show()

        #Salvando a Imagem
        plt.imshow(transformedImage)
        plt.axis('off')
        plt.savefig(os.getcwd() + '/Output_Images/' + outputImage, bbox_inches='tight', pad_inches=0)
    
    else:
        print("Selecione uma entrada válida!")
        print("1. Algoritmo de detecção de inclinação baseado em projeção horizontal.")
        print("2. Algoritmo de detecção de inclinação baseado na transformada de Hough.")
else:
    print("A imagem " + inputImage + " não foi encontrada!")