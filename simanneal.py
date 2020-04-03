import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pandas
import numpy as np
import random
import math

import structure as s

def simulanneal(people):
	best = s.Duty(people)

	#number of cycles
	cycle = 50

	#number of trials per cycle
	trial = 70

	#probability of accepting worse solution at start
	pstart_worst = 0.7

	#probability of accepting worse solution at end
	pend_worst = 0.001

	#initial temperature
	temp_init = -1.0/math.log(pstart_worst)

	#final temperature
	temp_fin = -1.0/math.log(pend_worst)

	#increments of temperature reduction
	temp_frac = (temp_fin/temp_init)**(1.0/(cycle-1.0))

	#list of best(lowest) standard deviations
	std_list = np.zeros(cycle+1)
	std_list[0] = best.get_std()

	temp = temp_init
	for i in range(cycle):
		print('Cycle: {} with temperature {}'.format(i, temp))

		for j in range(trial):
			current = s.Duty(people)

			if accept(current, best, temp):
				best = current
			else: continue
		std_list[i+1] = best.get_std()

		temp = temp_frac * temp

	print(best)
	print('Standard Deviation: {}'.format(best.get_std()))

	plt.plot(std_list)
	plt.xlabel('Cycle')

	plt.show()

def accept(current, best, temperature):
	if current.get_std() > best.get_std():
		if random.random() < acc_prob(current, best, temperature): return True
		else: return False
	else:
		return True

def acc_prob(current, best, temperature):
	delta_E = abs(current.get_std()- best.get_std())
	return(math.exp(-delta_E / temperature))

simulanneal(['a','b','c','d','e','f'])





