import numpy as np
import math
import matplotlib.pyplot as plt


#conductance matrix, node i , node j, resistor value
def resistor_stamp(A,i,j,value):
	A[i,i] += value
	A[i,j] += -value
	A[j,i] += -value
	A[j,j] += value
