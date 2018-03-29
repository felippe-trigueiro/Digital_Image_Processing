from scipy import misc
import improc
import numpy as np
import matplotlib.pyplot as plt
import sys
import os.path

if not os.path.exists(os.getcwd() + '/Output_Images/'): #Verifica se a pasta de saída existe e a cria se necessário
    os.makedirs(os.getcwd() + '/Output_Images/')

#Reliza as operações requeridas para todas as imagens passadas como argumento
for i in range(len(sys.argv)-1):
	if (os.path.isfile(sys.argv[i+1])): #sys.arg[0] consiste no nome do programa, assim sys.arg[i+1] consiste no nome das imagens
		img = misc.imread(sys.argv[i+1])
		
		p1 = plt.figure()
		p1.canvas.set_window_title(sys.argv[i+1])
		
		#Imagem e histograma da IMAGEM ORIGINAL
		plt.subplot(3,2,1)
		plt.imshow(img, cmap='gray')
		
		bins = np.linspace(0, 256, 257)
		hist = np.histogram(img, bins)
		hist = hist[0]	   #Seleciona apenas os valores do histograma em si e não os bins
		
		shape = img.shape #shape[0] - Largura; shape[1] - Altura
		
		print("Informações da imagem " + sys.argv[i+1] + "\n")
		print('Largura: ' + str(shape[0]) + 
					  '\nAltura: ' + str(shape[1]) + 
					  '\nIntensidade Mínima: ' + str(img.min()) + 
					  '\nIntensidade Máxima: ' + str(img.max()) + 
					  '\nIntensidade Média: ' + str(img.mean()) + '\n\n')
		
		plt.subplot(3,2,2)
		plt.plot(bins[0:256], hist/(shape[0]*shape[1])) #Mostra o histograma normalizado
		plt.ylabel("Frequência Relativa")
		
		#Imagem e histograma da IMAGEM NEGATIVA
		img_neg = 255-img       #Calcula o negativo da imagem
		
		plt.subplot(3,2,3)
		plt.imshow(img_neg, cmap='gray')
		img_name = sys.argv[i+1]
		misc.imsave(os.getcwd() + '/Output_Images/' + img_name[0:img_name.find('.')] + '_neg.png', img_neg)
		
		bins = np.linspace(0, 256, 257)
		hist_neg = np.histogram(img_neg, bins)
		hist_neg = hist_neg[0]	   #Seleciona apenas os valores do histograma em si e não os bins
		
		plt.subplot(3,2,4)
		plt.plot(bins[0:256], hist_neg/(shape[0]*shape[1])) #Mostra o histograma normalizado
		plt.ylabel("Frequência Relativa")
		
		#imagem e histograma da IMAGEM EM OUTRA ESCALA
		img_transf = improc.imconv(img, 0, 255, 120, 180) #Converte as intensidades de uma imagem de uma escala para outra
		plt.subplot(3,2,5)
		plt.imshow(img_transf, cmap='gray', vmin = 0, vmax = 255)
		misc.imsave(os.getcwd() + '/Output_Images/' + img_name[0:img_name.find('.')] + '_conv.jpg', img_transf)			
		
		bins = np.linspace(0, 256, 257)
		hist_transf = np.histogram(img_transf, bins)
		hist_transf = hist_transf[0]	   #Seleciona apenas os valores do histograma em si e não os bins
		
		plt.subplot(3,2,6)
		plt.plot(bins[0:256], hist_transf/(shape[0]*shape[1])) #Mostra o histograma normalizado
		
		plt.xlabel("Níveis de Cinza")
		plt.ylabel("Frequência Relativa")
		
	else:
		print("A imagem " + sys.argv[i+1] + " não foi encontrada!")
	
plt.show()
