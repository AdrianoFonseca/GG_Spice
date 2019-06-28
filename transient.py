import numpy as np
import math
import matplotlib.pyplot as plt
from stamps import *


def update_dynamic(out,A,b,dynamic,hmin,tinit,dt):
	ne = len(dynamic)/5
	dyn_A = np.zeros([A.shape[0],A.shape[0]])
	dyn_b = np.zeros([b.shape[0],1])

	for i in range(0,ne):
		if (dynamic[5*i].lower()=='sin'):
			dyn_b[dynamic[5*i+1]-1][0] += -1*np.exp(-1*dynamic[5*i+4]*(tinit+(dt*hmin)))*dynamic[5*i+2]*np.sin(2*np.pi*dynamic[5*i+3]*(tinit+(dt*hmin)))
		if (dynamic[5*i].lower()[0]=='c'):
			dv = 0
			a = np.sort([int(dynamic[5*i+1]),int(dynamic[5*i+2])])
			resistor_stamp(dyn_A,a[0],a[1],(dynamic[5*i+3])/hmin)
			
			if (dynamic[5*i+1]==0):
				dv = -out[int(dynamic[5*i+2])-1]
			elif (dynamic[5*i+2]==0):
				dv = out[int(dynamic[5*i+1])-1]
			else:
				dv = out[int(dynamic[5*i+1])-1] - out[int(dynamic[5*i+2])-1]

			dyn_b[int(dynamic[5*i+1])][0] += dv*(float(dynamic[5*i+3]))/(hmin)
			dyn_b[int(dynamic[5*i+2])][0] -= dv*(float(dynamic[5*i+3]))/(hmin)

	return (A+dyn_A),(b+dyn_b)