import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pandas
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
		print("Generation: \n{}".format(Pop.gentable))
		print("Fitness: \n{}".format(Pop.fitness))
		Pop.newpop()
		best.append(Pop.best_fitness())
		print("Cycle: {} \n{}".format(i, Pop.return_optimal()))

	print("Hours: {}".format(Pop.sum_single(Pop.best_individual())))
	print("Visualized: \n{}".format(Pop.convert(Pop.best_individual())))

	#plots best results per cycle
	plt.plot(best, 'b.-')
	plt.xlabel('Generation')
	plt.show()

genetic(['a','b','c','d','e','f','g','h','i'], 150, 50)



