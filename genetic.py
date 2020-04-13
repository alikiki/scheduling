import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import random
import math

import structure as s

################## GENETIC ALGORITHM ##################
def genetic(people, ind, cycles):
	Pop = s.DutyGEN(people, ind)

	#list for collecting best fitness scores from each generation
	best = []

	#generation cycles(int) generations
	for i in range(cycles):
		Pop.newpop()
		best.append(Pop.best_fitness())
		#print status updates
		Pop.status(i)

	#print("Hours: {}".format(Pop.sum_single(Pop.best_individual())))
	#print("Visualized: \n{}".format(Pop.convert(Pop.best_individual())))
	return(Pop.best_fitness())

	#plots best results per cycle
	#plt.plot(best, 'b.-')
	#plt.xlabel('Generation')
	#plt.show()

#outputs scatterplot with best fitness scores for a set number of trials
def genetic_testing(ind, cycles, trials):
	alphabet = [
	'a','b','c','d','e','f','g','h','i','j','k',
	'l','m','n','o','p','q','r','s','t','u','v',
	'w','x','y','z']

	#data bank with (number of people, best fitness score)
	bank = {'people' : [], 'fitness' : []}
	for i in range(7,26):
		workers = alphabet[:i]
		for _ in range(trials):
			bank['people'].append(i)
			bank['fitness'].append(genetic(workers, ind, cycles))

	df = pd.DataFrame(bank)

	plot = sns.scatterplot(x=df['people'], y=df['fitness'], alpha=.4)
	plot.set(xlabel="Number of Workers", ylabel="Fitness of Best Individual")
	plt.savefig('./images/results/limits.jpg', bbox_inches='tight')
	plt.show()

#print(genetic(['a','b','c','d','e','f','g','h', 'i'], 30, 15))
#genetic_testing(20,10,50)

