import matplotlib
import matplotlib.pyplot as plt
import pandas as pandas
import numpy as np
import random
import math

import structure as s

def simulanneal():
	#number of cycles
	cycle = 50

	#number of trials per cycle
	trial = 50

	#probability of accepting worse solution at start
	pstart_worst = 0.7

	#probability of accepting worse solution at end
	pend_worst = 0.001

	#initial temperature
	temp_init = -1.0/math.log(pstart_worst)

	#final temperature
	temp_fin = -1.0/math.log(pend_worst)


def accept(current, best):
	if current.get_std() > current.get_std():
		if random.random() < acc_prob(): return True
		else: return False
	else:
		return True

def acc_prob(current, best):
	delta_E = abs(current.get_std(), best.get_std())




