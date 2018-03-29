from skimage import color, io, measure
import numpy as np
import matplotlib.pyplot as plt
import sys
import os.path

if not os.path.exists(os.getcwd() + '/Output_Images/'): #Verifica se a pasta de saída existe e a cria se necessário
    os.makedirs(os.getcwd() + '/Output_Images/')
									       	
									       #Verifica se a imagem de entrada existe
if (os.path.isfile(sys.argv[1])): #sys.arg[0] consiste no nome do programa, assim sys.arg[1] consiste no nome das imagens
	regioes = [0, 0, 0]            #Regiões [pequena, media, grande] 
	def_tam_area = [700, 2000, 3500]
	
	img = io.imread(sys.argv[1])        
	img_shape = img.shape
	im_objects = np.ones((img_shape[0], img_shape[1])) #Cria uma matriz de floats MxN para armazenar as bordas dos objetos.
	
	img_gray = color.rgb2gray(img)               #Os valores de img_gray estão normalizados
																
	edges = measure.find_contours(img_gray, 0.8) #Encontra as bordas dos objetos. Como trata-se de um fundo branco, o limiar de 0.8 consistirá
																#no valor máximo para as bordas	
	
	bin_im = img_gray < 0.8 #Converte a imagem em tons de cinza para uma imagem binária onde, os valores menores que 0.1 (escuros, preto)
									#são mapeados como 0 (preto). Os valores restantes (>= 0.1) são mapeados como branco (1)
	
	label = measure.label(bin_im, connectivity=2)
	props = measure.regionprops(label)

	print("Número de Regiões: " + str(len(edges)) + "\n")
	
	p1 = plt.figure()                        #Exibe img e img_gray
	p1.canvas.set_window_title(sys.argv[1])
		
	#Imagem orignal e imagem em tons de cinza
	plt.subplot(1,2,1)
	plt.imshow(img)
	plt.xlabel("Imagem Colorida")
	img_name = sys.argv[1]
	io.imsave(os.getcwd() + '/Output_Images/' + img_name[0:img_name.find('.')] + '.png', img)
	
	plt.subplot(1,2,2)
	plt.imshow(img_gray, cmap='gray')
	plt.xlabel("Imagem Monocromática")
	io.imsave(os.getcwd() + '/Output_Images/' + img_name[0:img_name.find('.')] + '_gray.png', img_gray)
	
	p2 = plt.figure()                                       #Exibe os Rótulos
	p2.canvas.set_window_title(sys.argv[1] + ' - Label')
	
	for n, ed in enumerate(edges):
		ed = ed.astype(int)                   
		im_objects[ed[:, 0], ed[:, 1]] = 0      #Cria uma imagem binária contendo as bordas dos objetos, onde o preto (0) corresponde a borda 
		centr = props[n].centroid
		plt.text(centr[1] - 8, centr[0] + 5, str(n), figure=p2)
		print("Região " + str(n) + "\tPerímetro: " + str(int(props[n].perimeter)) + "\tÁrea: " + str(props[n].area))
		
		if props[n].area < 1500:
			regioes[0] = regioes[0] + 1
		elif props[n].area >= 1500 and props[n].area < 3000: 
			regioes[1] = regioes[1] + 1
		elif props[n].area >= 3000:
			regioes[2] = regioes[2] + 1
	
	img_gray[img_gray < 0.8] = 0.7                          #Pixels que foram mapeados diferente do branco são mapeados com 0.7
	plt.imshow(img_gray, cmap='gray', vmin=0, vmax=1)
	plt.xlabel("Rótulo das Imagens")
	plt.savefig(os.getcwd() + '/Output_Images/' + img_name[0:img_name.find('.')] + '_label.png')	
			
	p3 = plt.figure()                                       #Exibe as bordas
	p3.canvas.set_window_title(sys.argv[1] + ' - Bordas')
	
	im_objects = color.gray2rgb(im_objects)
	plt.imshow(im_objects)
	io.imsave(os.getcwd() + '/Output_Images/' + img_name[0:img_name.find('.')] + '_edges.png', im_objects)
	plt.xlabel("Contornos dos objetos")
	
	p4 = plt.figure()                                      #Exibe o histograma
	p4.canvas.set_window_title(sys.argv[1] + ' - Histograma')
	plt.bar(def_tam_area, regioes, width=700)
	plt.xlabel("Histograma de Área dos Objetos")
	plt.ylabel("Número de Objetos")
	
	print("\nNúmero de regiões pequenas: " + str(regioes[0]))
	print("Número de regiões médias: " + str(regioes[1]))
	print("Número de regiões grandes: " + str(regioes[2]))
		
else:
	print("A imagem " + sys.argv[1] + " não foi encontrada!")
	
plt.show()
