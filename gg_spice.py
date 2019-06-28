import numpy as np
import math
import matplotlib.pyplot as plt
from newton_raphson import *
from stamps import *
from transient import *
from create_matrix import *

net = raw_input("Escreva o nome e endereco do arquivo da netlist:\n")


A,b,names,dynamic,diodes,analysis,hmin,MAXITER,tinit,tfinal = create_matrix(net)

if analysis == 1:
	stat_A = A
	stat_b = b
	out = np.zeros([b.shape[0],1])
	if dynamic == []:
			print(NR_DC(A,b,diodes,hmin,MAXITER))
	else:
			A,b = update_dynamic(out,stat_A,stat_b,dynamic,1e12,0,0)
			print(NR_DC(A,b,diodes,hmin,MAXITER))
elif analysis == 2:
	result = []
	stat_A = A
	stat_b = b
	out = np.zeros([b.shape[0],1])
	sim = raw_input("Escolha o elemento a ser plotado (onde o primeiro elemento e o elemento 1):\n")

	A,b = update_dynamic(out,stat_A,stat_b,dynamic,1e12,0,0)
	out = NR_DC(A,b,diodes,hmin,MAXITER)

	print(out)

	for dt in range(0,int((tfinal-tinit)/hmin)):
		if dynamic == []:
			print(NR_DC(A,b,diodes,hmin,MAXITER))
		else:
			A,b = update_dynamic(out,stat_A,stat_b,dynamic,hmin,tinit,dt)
			out = NR_DC(A,b,diodes,hmin,MAXITER)
			result.append(float(out[int(sim)-1][0]))
else:
   	print("not implemented")

t = tinit+np.linspace(0,len(result),len(result))*hmin

plt.plot(t,result,'k-')
plt.ylabel(names[int(sim)-1]+' V')
plt.xlabel('t (s)')
plt.show()