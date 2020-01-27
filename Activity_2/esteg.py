import numpy as np

#Insere os bits que foram obtidos do texto, nos bits bit_plane de cada um dos pixels das camadas RGB
#A sequencia de inserção inicia no pixel (0,0), vai percorrendo as colunas e depois as linhas. Ex: (0,0), (0,1) ...
#Quando todos os bits são inseridos, os loops são encerrados.
def change_image_bit(image, bit_plane, row, column, stri_bin):
	i = 0
	flag_r = 0
	flag_c = 0
	imag = np.copy(image)

	for r in range(row):
		if flag_r == 0:
			for c in range(column):
				if flag_c == 0:
					for bp in range(3):
						bin_pixel_layer = list(format(imag[r, c, bp], '08b'))
						bin_pixel_layer[7 - bit_plane] = stri_bin[i]
						bin_pixel_layer = int(''.join(bin_pixel_layer), 2)
						imag[r, c, bp] = bin_pixel_layer
						i = i + 1
						if(i == len(stri_bin)):
							flag_c = 1
							flag_r = 1
							break
				else:
					break
		else:
			break
			
	return imag
