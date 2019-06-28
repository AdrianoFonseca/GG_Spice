import numpy as np
import math
import matplotlib.pyplot as plt
from stamps import *


def sip2num(input):
	pos_postfixes = ['k', 'M', 'G', 'T']
	neg_postfixes = ['m', 'u', 'n', 'p', 'f']

	num_postfix = input[-1]
	if num_postfix in pos_postfixes:
		num = float(input[:-1])
		num*=10**((pos_postfixes.index(num_postfix)+1)*3)
	elif num_postfix in neg_postfixes:
		num = float(input[:-1])
		num*=10**(-(neg_postfixes.index(num_postfix)+1)*3)
	else:
		num = float(input)
	return num


def create_matrix(netlist):
	f = open(netlist, "r")
	dynamic = []
	diodes = []
	names = []
	i = 1
	analysis = 0

	for x in f:
		if i == 1:
			data = x.split() 
			nodes = int(data[0])+1
			A = np.zeros([nodes,nodes])
			b = np.zeros([nodes,1])
			i +=1
			for k in range(1,nodes):
				names.append("e"+str(k))
			continue

		elemento = x[0].lower()
		data = x.split() 

		if elemento == 'r':
			a = np.sort([int(data[1]),int(data[2])])
			resistor_stamp(A,a[0],a[1],1/sip2num(data[3]))
			
		# elif elemento == 'l':
		# 	print('Esse e o indutor: ' + data[0])
		# 	print('Entre os nos: ' + data[1] + ' e ' + data[2] + '\n')
		# 	print('Valor: ' + str(sip2num(data[3])) + ' H\n')

		elif elemento == 'd':

			diodes.append(int(data[1]))
			diodes.append(int(data[2]))
			diodes.append(sip2num(data[3]))
			diodes.append(sip2num(data[4]))


		elif elemento == 'c':
		# 	print('Esse e o capacitor: ' + data[0])
		# 	print('Entre os nos: ' + data[1] + ' e ' + data[2] + '\n')
		# 	print('Valor: ' + str(sip2num(data[3])) + ' F\n')
			dynamic.append(data[0])
			dynamic.append(sip2num(data[1]))
			dynamic.append(sip2num(data[2]))
			dynamic.append(sip2num(data[3]))
			if (len(data) == 5):
				dynamic.append(sip2num(data[4]))
			else:
				dynamic.append(0)


		# elif elemento == 'k':
		# 	print('Esse e o transformador: ' + data[0])
		# 	print('Entre os indutores: ' + data[1] + ' e ' + data[2] + '\n')
		# 	print('Fator de acoplamento: ' + str(sip2num(data[3])) + '\n')
	
		# elif elemento == 'e':
		# 	print('Esse e o VCVS: ' + data[0])
		# 	print('nos controladores: ' + data[1] + ' e ' + data[2] + '\n')
		# 	print('nos controlados: ' + data[3] + ' e ' + data[4] + '\n')
		# 	print('Ganho: ' + str(sip2num(data[3])) + '\n')
	
		#elif elemento == 'f':
		# 	print('Esse e o CCVS: ' + data[0])
		# 	print('nos controladores: ' + data[1] + ' e ' + data[2] + '\n')
		# 	print('nos controlados: ' + data[3] + ' e ' + data[4] + '\n')
		# 	print('Transresistencia: ' + str(sip2num(data[3])) + '\n')


		elif elemento == 'g':
			A[int(data[1])][int(data[3])] += sip2num(data[5])
			A[int(data[1])][int(data[4])] += -1*sip2num(data[5])
			A[int(data[2])][int(data[3])] += -1*sip2num(data[5])
			A[int(data[2])][int(data[4])] += sip2num(data[5])


		elif elemento == 'h':
			An = np.zeros([A.shape[0]+1,A.shape[0]+1])
			An[:A.shape[0],:A.shape[1]] = A
			bn = np.zeros([b.shape[0]+1,1])
			bn[:b.shape[0]] = b
			A = An
			b = bn

			A[int(data[1])][-1] += sip2num(data[5])
			A[int(data[2])][-1] += -sip2num(data[5])
			A[int(data[3])][-1] += 1
			A[int(data[4])][-1] += -1
			A[-1][int(data[3])] += -1
			A[-1][int(data[4])] += 1

			names.append("j"+data[0])


		elif elemento == 'v':
			
			if data[3] == 'DC':
				An = np.zeros([A.shape[0]+1,A.shape[0]+1])
				An[:A.shape[0],:A.shape[1]] = A
				bn = np.zeros([b.shape[0]+1,1])
				bn[:b.shape[0]] = b
				A = An
				b = bn			
			
				A[int(data[1])][-1] += 1
				A[int(data[2])][-1] += -1
				A[-1][int(data[1])] += -1
				A[-1][int(data[2])] += 1
		

				b[-1][0] = -float(sip2num(data[4]))

				names.append("j"+data[0])
				
			elif data[3] == 'SIN':
				#<nivel continuo> <amplitude> <frequencia em Hz>
				An = np.zeros([A.shape[0]+1,A.shape[0]+1])
				An[:A.shape[0],:A.shape[1]] = A
				bn = np.zeros([b.shape[0]+1,1])
				bn[:b.shape[0]] = b
				A = An
				b = bn			
			
				A[int(data[1])][-1] += 1
				A[int(data[2])][-1] += -1
				A[-1][int(data[1])] += -1
				A[-1][int(data[2])] += 1
		

				b[-1][0] = -float(sip2num(data[4]))
				dynamic.append(data[3])
				dynamic.append(A.shape[0])
				dynamic.append(sip2num(data[5]))
				dynamic.append(sip2num(data[6]))
				dynamic.append(sip2num(data[7]))

				names.append("j"+data[0])


		elif elemento == 'i':

			b[int(data[1])][0] += -sip2num(data[3])
			b[int(data[2])][0] += sip2num(data[3])
			

		elif elemento == 'q':
			#C B E beta is vt
			diodes.append(int(data[2]))
			diodes.append(int(data[1]))
			diodes.append(sip2num(data[5]))
			diodes.append(sip2num(data[6]))

			beta = sip2num(data[4])
			alpha = beta/(1+beta)
			
			print(A.shape[0])

			An = np.zeros([A.shape[0]+2,A.shape[0]+2])
			An[:A.shape[0],:A.shape[1]] = A
			bn = np.zeros([b.shape[0]+2,1])
			bn[:b.shape[0]] = b
			A = An
			b = bn

			A[int(data[1])][-1] += alpha
			A[int(data[2])][-1] += -alpha

			A[-2][-1] += 1
			A[int(data[3])][-1] += -1

			A[-1][-2] += -1
			A[-1][int(data[3])] += 1

			diodes.append(int(data[2]))
			diodes.append(A.shape[0]-2)
			diodes.append(sip2num(data[5]))
			diodes.append(sip2num(data[6]))

			names.append("e"+data[0])
			names.append("j"+data[0])

		elif elemento == '.':
			if data[0].lower() == '.dc':
				hmin = float(data[1])
				MAXITER = float(data[1])
				analysis = 1
			elif data[0].lower() == '.trans':
				hmin = sip2num(data[1])
				tinit = sip2num(data[2])
				tfinal = sip2num(data[3])
				analysis = 2
		else:
		 	print('Elemento invalido! Erro na netlist')
		i+=1
	print(names)
	if analysis == 0:
		print("No simulation command")
		return(0)
	if analysis == 1:
		return(A,b,names,dynamic,diodes,analysis,hmin,MAXITER,0,0)
	if analysis == 2:
		return(A,b,names,dynamic,diodes,analysis,hmin,0,tinit,tfinal)

