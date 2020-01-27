from skimage import io
import sys
import os.path

enc_image = sys.argv[1]
bit_plane = int(sys.argv[2])
output_text = sys.argv[3]
seq_bit_plane = []
list_bit_plane = []
decod_text = []

#Verifica se os parâmetros de entrada estão corretos e/ou existem
if (os.path.isfile(enc_image)): 
	if (bit_plane <= 2 and bit_plane >= 0):
	
		img = io.imread(enc_image)
		row = img.shape[0]
		column = img.shape[1]
		
		#Cria uma lista "seq_bit_plane" com todos os bits com posição bit_plane, nas 3 camadas
		for r in range(row):
			for c in range(column):
				for bp in range(3):
					bin_pixel_layer = format(img[r, c, bp], '08b')
					seq_bit_plane.append(bin_pixel_layer[7 - bit_plane])
		
		#Agrupa os bits de seq_bit_plane em grupos de bytes
		for i in range(len(seq_bit_plane)):
			list_bit_plane.append(seq_bit_plane[(8*i):(8*i+8)])
			list_bit_plane[i] = ''.join(list_bit_plane[i])
		
		#Cria uma lista "list_bit_plane" apenas com os grupos que compoem os caracteres do arquivo de texto
		end_position = list_bit_plane.index('00000000')
		list_bit_plane = list_bit_plane[0:end_position]
		
		#Converte os bytes para os caracteres correspondentes
		for i in range(len(list_bit_plane)):
			decod_text.append(chr(int(list_bit_plane[i], 2)))
		decod_text = ''.join(decod_text)
	
		with open(output_text, 'w') as file_object:
			file_object.write(decod_text)
			
		print("Texto decodificado, " + output_text + " criado com sucesso!")
	
	else:
		print("O plano de bits " + str(bit_plane) + " inserido está fora de faixa permitida!")
else:
	print("A imagem " + enc_image + " não foi encontrada!")
