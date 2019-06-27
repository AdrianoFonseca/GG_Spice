import numpy as np
import math
import matplotlib.pyplot as plt

net = raw_input("Escreva o nome e endereco do arquivo da netlist:\n")

def carimbo(A,i,j,valor):
	if (i!=j):
		A[i,i] += valor
		A[i,j] += -1*valor
		A[j,i] += -1*valor
		A[j,j] += valor
	else:
		A[i,i] += valor


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
			carimbo(A,a[0],a[1],1/sip2num(data[3]))
			
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




		elif elemento == 'm':
		# 	G D S B
			# carimbo(A,int(data[1]),int(data[4]),1/(10e12)) #CGB
			# carimbo(A,int(data[1]),int(data[3]),1/(10e12)) #CGS
			# carimbo(A,int(data[3]),int(data[4]),1/(10e12)) #CSB
			# carimbo(A,int(data[2]),int(data[4]),1/(10e12)) #CDB
			# carimbo(A,int(data[1]),int(data[2]),1/(10e12)) #CGD

			carimbo(A,int(data[2]),int(data[3]),1/(2e6)) #RDS

			A[int(data[2])][int(data[1])] += sip2num('20m') #gmvgs
			A[int(data[2])][int(data[3])] += -1*sip2num('20m')
			A[int(data[3])][int(data[1])] += -1*sip2num('20m')
			A[int(data[3])][int(data[3])] += sip2num('20m')
	
		# elif elemento == 'o':
		# 	print('Esse e o AMP-OP: ' + data[0])
		# 	print('nos entrada: ' + data[1] + ' e ' + data[2] + '\n')
		# 	print('nos saida: ' + data[3] + ' e ' + data[4] + '\n')
	
		elif elemento == '.':
			if data[0].lower() == '.subckt':
				print('Esse e o subcircuito: ' + data[0])
			elif data[0].lower() == '.dc':
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


A,b,names,dynamic,diodes,analysis,hmin,MAXITER,tinit,tfinal = create_matrix(net)

def diodefunc(v,a,b):
	return(a*(np.exp(v/b)-1))

def diodederiv(v,a,b):
	return((a/b)*np.exp(v/b))

def update_diodes(vn,xn,diodes):
	nd = len(diodes)/4

	for i in range(0,nd):
		if (diodes[4*i] == 0):
			vnn = -xn[diodes[4*i+1]-1]
		elif (diodes[4*i+1] == 0):
			vnn = xn[diodes[4*i]-1]
		else:
			vnn = xn[diodes[4*i]-1]-xn[diodes[4*i+1]-1]

		if vnn > 0.8:
			vnn = 0.8

		Go = diodederiv(vn[i],diodes[4*i+2],diodes[4*i+3])

		G =  diodederiv(vnn,diodes[4*i+2],diodes[4*i+3])


		carimbo(A,diodes[4*i],diodes[4*i+1],-Go)

		carimbo(A,diodes[4*i],diodes[4*i+1],G)


		b[diodes[4*i]][0] -= -1*(diodefunc(vn[i],diodes[4*i+2],diodes[4*i+3])-Go*vn[i])

		b[diodes[4*i]][0] += -1*(diodefunc(vnn,diodes[4*i+2],diodes[4*i+3])-G*vnn)


		b[diodes[4*i+1]][0] -= (diodefunc(vn[i],diodes[4*i+2],diodes[4*i+3])-Go*vn[i])

		b[diodes[4*i+1]][0] += (diodefunc(vnn,diodes[4*i+2],diodes[4*i+3])-G*vnn)

		vn[i] = vnn
		
	return(vn)

def add_diodes(diodes,A,b):
	nd = len(diodes)/4
	vn = np.ones(nd)*0.6

	xo = np.zeros([b[1:].shape[0],1])

	for i in range(0,nd):
		G =   diodederiv(vn[i],diodes[4*i+2],diodes[4*i+3])
		
		carimbo(A,diodes[4*i],diodes[4*i+1],G)

		b[diodes[4*i]][0] += -1*(diodefunc(vn[i],diodes[4*i+2],diodes[4*i+3])-G*vn[i])
		b[diodes[4*i+1]][0] += (diodefunc(vn[i],diodes[4*i+2],diodes[4*i+3])-G*vn[i])

	xn = np.linalg.solve(np.asmatrix(A[1:,1:]),np.asmatrix(b[1:]))


	while(np.linalg.norm(xn-xo) > 1e-6):
		vn = update_diodes(vn,xn,diodes)
		xo = xn
		xn = np.linalg.solve(np.asmatrix(A[1:,1:]),np.asmatrix(b[1:]))

		
	return xn

def NR_DC(A,b,diodes,hmin,MAXITER):
	if not diodes:
		A = np.asmatrix(A[1:,1:])
		b = np.asmatrix(b[1:])
		return np.linalg.solve(A,b)
	else:
		xn = add_diodes(diodes,A,b)
		return  xn


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
			carimbo(dyn_A,a[0],a[1],(dynamic[5*i+3])/hmin)
			
			if (dynamic[5*i+1]==0):
				dv = -out[int(dynamic[5*i+2])-1]
			elif (dynamic[5*i+2]==0):
				dv = out[int(dynamic[5*i+1])-1]
			else:
				dv = out[int(dynamic[5*i+1])-1] - out[int(dynamic[5*i+2])-1]

			dyn_b[int(dynamic[5*i+1])][0] += dv*(float(dynamic[5*i+3]))/(hmin)
			dyn_b[int(dynamic[5*i+2])][0] -= dv*(float(dynamic[5*i+3]))/(hmin)

	return (stat_A+dyn_A),(stat_b+dyn_b)
			

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