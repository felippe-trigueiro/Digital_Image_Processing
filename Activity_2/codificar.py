from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import sys
import os.path
import esteg

input_image = sys.argv[1]
text_message = sys.argv[2]
bit_plane = int(sys.argv[3])
output_image = sys.argv[4]
bit_plane_list = [0, 1, 2, 7]

#Verifica se os parâmetros de entrada estão corretos e/ou existem
if (os.path.isfile(input_image)): 
	if (os.path.isfile(text_message)): 
		if (bit_plane <= 2 and bit_plane >= 0): 
		
			if (output_image[output_image.find('.'):len(output_image)] != '.png'):
				print("O nome da imagem de saída deve estar no formato .png!")
				exit()
			
			with open(text_message, 'r') as file_object: #abre o arquivo de texto
				stri = file_object.read()
			stri += '\0'                      #Insere um sinal para fim de mensagem
			stri_bin = ''.join(format(ord(x), '08b') for x in stri)   #Converte a string para bytes                                
			
			im_inp = io.imread(input_image)
			row = im_inp.shape[0]
			column = im_inp.shape[1]
	
			print("Tamanho da mensagem: " + str(len(stri_bin)) + " caracteres")
			print("Tamanho de mensagem máximo permitido: " + str(row*column*3) + " caracteres")
			
			if (len(stri_bin) > (row*column*3)):
				print("Tamanho de mensagem maior que o permitido!")
				print("Imagem codificada, " + output_image + " não criada!")
				exit()
			
			
			print("Codificando a mensagem...")
			#Codificação da imagem com o plano de bits passado pelo usuário
			im = esteg.change_image_bit(im_inp, bit_plane, row, column, stri_bin)
			io.imsave(output_image, im)
			print("Imagem codificada, " + output_image + " criada com sucesso!")
					
			#Impressão dos planos de bits 0, 1, 2, 7
			p1 = plt.figure()
			p1.canvas.set_window_title(input_image + ' - Bit_Plane 0')
			img = esteg.change_image_bit(im_inp, 0, row, column, stri_bin)
			plt.imshow(im_inp)
							
			p2 = plt.figure()
			p2.canvas.set_window_title(input_image + ' - Bit_Plane 1')
			img = esteg.change_image_bit(im_inp, 1, row, column, stri_bin)
			plt.imshow(img)

			p3 = plt.figure()
			p3.canvas.set_window_title(input_image + ' - Bit_Plane 2')
			img = esteg.change_image_bit(im_inp, 2, row, column, stri_bin)
			plt.imshow(img)

			p4 = plt.figure()
			p4.canvas.set_window_title(input_image + ' - Bit_Plane 7')
			img = esteg.change_image_bit(im_inp, 7, row, column, stri_bin)
			plt.imshow(img)
			
			plt.show()				 			
		else:
			print("O plano de bits " + str(bit_plane) + " inserido está fora de faixa permitida!")
	else:
		print("O arquivo " + text_message + " não foi encontrado!")
else:
	print("A imagem " + input_image + " não foi encontrada!")	
