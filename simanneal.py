import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pandas
import numpy as np
import random
import math

import structure as s

################## SIMULATED ANNEALING ##################
def simulanneal(people,ind):
	#best / optimal state
	best = s.DutySA(people)
	current = s.DutySA(people)

	#number of cycles
	cycle = 50

	#number of trials per cycle
	trial = 20

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

	#temperature variable
	temp = temp_init

	counter = 0
	#simulated annealing 
	for i in range(cycle):
		print('Cycle: {} with temperature {}'.format(i, temp))
		for j in range(trial):
			current.change_state_random()
			if accept(current, best, temp):
				best.pdtable = current.pdtable
			else: 
				continue

		#add cycle's best state to list
		std_list[i+1] = best.get_std()

		#lower temperature
		temp = temp_frac * temp

	print(best)
	print('Standard Deviation: {}'.format(best.get_std()))

	#plot best states per cycle
	plt.plot(std_list, 'r.-')
	plt.xlabel('Cycle')

	plt.show()

#helper : whether or not worse solution should be accepted
def accept(curr, bes, temperature):
	if curr.get_std() > bes.get_std():
		if random.random() < acc_prob(curr, bes, temperature): return True
		else: return False
	else:
		return True
#
def accept_stateswitch(curr, bes, temperature):
	if curr.get_std() > bes.get_std() or random.random() < acc_prob(curr, bes, temperature): return True
	else: return False

#helper : calculuates acceptance probability
def acc_prob(curr, bes, temperature):
	delta_E = abs(curr.get_std()- bes.get_std())
	return(math.exp(-delta_E / temperature))


#testing which change_state is better, random or switch
def whichchange(people):
	#object for change_state_random
	randomchange = s.DutySA(people)

	#object for change_state_switch
	switchchange = s.DutySA(people)

	cycle = 10**2

	#lists for collecting standard deviation at end of each cycle
	randomdata = np.zeros(cycle+1)
	switchdata = np.zeros(cycle+1)

	for i in range(cycle):
		randomdata[i+1] = randomchange.get_std()
		randomchange.change_state_random()

		#every 3 cycles, execute change_state_random
		if i % 3 == 0:
			switchdata[i+1] = switchchange.get_std()
			switchchange.change_state_random()
		else:
			switchdata[i+1] = switchchange.get_std()
			switchchange.change_state_switch()
			switchchange.change_state_switch()

	fig = plt.figure()
	ax1 = fig.add_subplot(211)
	ax1.plot(randomdata,'r.-')
	ax2 = fig.add_subplot(212)
	ax2.plot(switchdata,'b.-')

	plt.show()


simulanneal(['a','b','c','d','e','f'],0)
#whichchange(['a','b','c','d','e','f'])






