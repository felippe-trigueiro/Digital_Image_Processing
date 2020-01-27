import numpy as np

def imconv (Xi, vmin_i, vmax_i, vmin_o, vmax_o):
	Xo = (Xi - vmin_i)*((vmax_o - vmin_o)/(vmax_i - vmin_i)) + vmin_o
	Xo = Xo.astype(int)
	
	return Xo	
