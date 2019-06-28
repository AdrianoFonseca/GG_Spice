import numpy as np
import math
import matplotlib.pyplot as plt
from stamps import *

def diodefunc(v,a,b):
	return(a*(np.exp(v/b)-1))

def diodederiv(v,a,b):
	return((a/b)*np.exp(v/b))

def update_diodes(NR_A,NR_b,xn,nd,diodes):
	NR_A = np.zeros([NR_A.shape[0],NR_A.shape[0]])
	NR_b = np.zeros([NR_b.shape[0],1])

	for i in range(0,nd):
		if (diodes[4*i] == 0):
			vd = -xn[diodes[4*i+1]-1]
		elif (diodes[4*i+1] == 0):
			vd= xn[diodes[4*i]-1]
		else:
			vd = xn[diodes[4*i]-1]-xn[diodes[4*i+1]-1]

		if vd > 0.8:
			vd = 0.8

		G =  diodederiv(vd,diodes[4*i+2],diodes[4*i+3])

		resistor_stamp(NR_A,diodes[4*i],diodes[4*i+1],G)

		NR_b[diodes[4*i]][0] += -1*(diodefunc(vd,diodes[4*i+2],diodes[4*i+3])-G*vd)
		NR_b[diodes[4*i+1]][0] += (diodefunc(vd,diodes[4*i+2],diodes[4*i+3])-G*vd)

	return(NR_A,NR_b)

def NR_DC(A,b,diodes,hmin,MAXITER):
	if not diodes:
		A = np.asmatrix(A[1:,1:])
		b = np.asmatrix(b[1:])
		return np.linalg.solve(A,b)
	else:
		nd = len(diodes)/4
		NR_A = np.zeros([A.shape[0],A.shape[0]])
		NR_b = np.zeros([b.shape[0],1])

		xo = np.zeros([b[1:].shape[0],1])

		[NR_A,NR_b] = update_diodes(NR_A,NR_b,xo,nd,diodes)

		xn = np.linalg.solve(np.asmatrix(A[1:,1:]+NR_A[1:,1:]),np.asmatrix(b[1:]+NR_b[1:]))

		while(np.linalg.norm(xn-xo) > 1e-6):
			[NR_A,NR_b] = update_diodes(NR_A,NR_b,xn,nd,diodes)
			xo = xn
			xn = np.linalg.solve(np.asmatrix(A[1:,1:]+NR_A[1:,1:]),np.asmatrix(b[1:]+NR_b[1:]))
		return xn