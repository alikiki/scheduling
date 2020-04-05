import pandas as pd
import numpy as np
import random


class Duty:
	"""
	Duty : schedule data structure

	Instance variables: 
		people (list)
		pdtable (pandas DataFrame)

	Methods:
		get_hours = gets number of hours worked for single person
		get_hours_all = gets number of hours worked for all people
		get_std = gets standard deviation of number of hours worked
		change_state_random = randomly changes all slots of schedule
		change_state_switch = randomly chooses two slots, then switches them

		helpers:
			switcher = switches two slots 

		fitness_gen = returns fitness of current generation
		selection = selects best individuals of population 
		crossover = crosses chromosomes of best individuals of population
		mutation = applies random point mutation to offspring of best parents
		newpop = combines parents and offspring to make a next generation
		best_fitness = returns best fitness score of current generation
		return_optimal = returns best individual and best fitness 

		helpers: 
			fitness_single = returns fitness of single generation
	"""

	weekdays = [
		'Monday', 'Tuesday', 'Wednesday',
		'Thursday', 'Friday', 'Saturday', 'Sunday'
		]

	def __init__(self, people, ind):
		#.......... simulated annealing..........
		#names list
		self.people = people

		#initial state : assigns people to slots randomly
		self.pdtable = Duty.change_state_random(self)


		#.......... genetic algorithm ...........
		#number of individuals per population
		self.ind = ind

		#generations table : initial pool
		self.gentable = np.random.random_integers(0, len(self.people), size=(ind,16))

		#fitness of generation
		self.fitness = Duty.fitness_gen(self, self.gentable)

	#returns object variables
	def __repr__(self):
		return("people : {} \nschedule :\n{} \ngenerations : \n{} \nfitness : {}".format(
			self.people, self.pdtable, self.gentable, self.fitness))

	#total working hours for single person
	def get_hours(self, person):
		sum = 0
		#how many hours in each shift
		hours = [1,7,8]
		for i in range(3):
			sum += hours[i]*(self.pdtable[i] == person).sum()
		return(sum)

	#total working hours for all people
	def get_hours_all(self):
		return(pd.DataFrame({name : Duty.get_hours(self, name) for name in self.people}, index=[0]))

	#gets standard deviation of hours worked
	def get_std(self):
		return(Duty.get_hours_all(self).values.std(ddof=1))


	############ SIMULATED ANNEALING ############


	#changes state by randomly assigning people to slots in schedule
	def change_state_random(self):
		self.pdtable = pd.DataFrame(
			{hour : [random.choice(self.people) for _ in range(7)]
			if hour < 2 else [0 for i in range(5)]+[random.choice(self.people) for _ in range(2)]
			for hour in range(3)},index=Duty.weekdays)
		return(self.pdtable)


	#changes state by randomly switching two slots
	def change_state_switch(self):
		weekendOrday = random.randrange(0,2)
		#weekends < -- > weekends
		if weekendOrday == 0: Duty.switcher(self, 0, 2, 0, 5)
		#weekdays < -- > weekdays
		else: Duty.switcher(self, 0, 3, 5, 7)


	#helper : switches two slots
	def switcher(self, first1, second1, first2, second2):
		#list of random slot coordinates
		places = [0,0,0,0]
		for i in range(4):
			if i % 2 == 0:
				places[i] = random.randrange(first1, second1)
			else:
				places[i] = random.randrange(first2, second2)

		#switching up
		first = self.pdtable[places[0]][places[1]]
		self.pdtable[places[0]][places[1]] = self.pdtable[places[2]][places[3]]
		self.pdtable[places[2]][places[3]] = first

		return(self.pdtable)


	############ GENETIC IMPLEMENTATION ############
	

	#helper : returns fitness of an individual
	def fitness_single(self, ind):
		hours = np.array([1,7,1,7,1,7,1,7,1,7,1,7,8,1,7,8])
		sums = []

		#takes dot product of hours vector and binary individual vector
		for i in range(len(self.people)):
			wherepeople = (ind == i).astype(int)
			single_sum = np.sum(np.dot(hours, wherepeople))
			sums.append(single_sum)

		return(np.std(sums))

	#returns fitness of whole generation (list)
	def fitness_gen(self, generation):
		fitness = []
		for i in range(len(generation)):
			fitness.append(Duty.fitness_single(self, generation[i]))

		return(np.array(fitness))

	#selection of best parent_num individuals in current gen
	def selection(self, parent_num):
		ind = np.argpartition(self.fitness, parent_num)[:parent_num]
		parents = self.gentable[ind]
		parents_fitness = self.fitness[ind]

		return(parents)

	#crossover : swaps halves of parents and generates offspringsize children
	def crossover(self, parents, offspringsize):
		offspring = np.empty((offspringsize,16))
		crossover_point = 8

		#swaps halves between parents on a ring
		for k in range(offspringsize):
			par1_idx = k%parents.shape[0]
			par2_idx = (k+1)%parents.shape[0]

			#swapping/crossover
			offspring[k, 0:crossover_point] = parents[par1_idx, 0:crossover_point]
			offspring[k, crossover_point:] = parents[par2_idx, crossover_point:]

		return(offspring)

	#mutation : randomly changes one slot in the schedule to a random person
	def mutation(self, offspring):
		for ind in range(len(offspring)):
			rand_ind = random.randrange(0,16)
			rand_point = random.randrange(0, len(self.people))
			offspring[ind, rand_ind] = rand_point

		return(offspring) 

	#combines parent and offspring to make a new population/generation
	def newpop(self):
		parents = Duty.selection(self, int((self.ind)/2))
		offspring = Duty.mutation(self, Duty.crossover(self, parents, self.ind - len(parents))).astype(int)
		self.gentable =  np.concatenate([parents, offspring])
		self.fitness = Duty.fitness_gen(self, self.gentable)

	#returns best fitness 
	def best_fitness(self):
		return(self.fitness[np.argmin(self.fitness)])

	#returns best schedule and best fitness
	def return_optimal(self):
		return("Best schedule: {} \nFitness: {}".format(
			self.gentable[np.argmin(self.fitness)], 
			self.fitness[np.argmin(self.fitness)]))

################ tests ################
#test = Duty(['alpha', 'bravo', 'charlie', 'delta', 'echo', 'hotel', 'india'], 100)
#print(test)
#print(test.get_std())
#print(test.people)
#print(test.table)
#print(test.pdtable)
#print(test.get_hours('echo'))
#print(test.get_hours_all())
#print(test.get_std())
#test.change_state_switch()

#print("Generation: \n{}".format(test.gentable))
#print("Fitness: \n{}".format(test.fitness))
#print(test.selection(5))
#print(test.fitness_gen(test.selection(5)))
#print(test.crossover(test.selection(5), 5))
#print(test.fitness_gen(test.crossover(test.selection(5), 5)))
#print(test.mutation(test.crossover(test.selection(5), 5)))
#print(test.fitness_gen(test.mutation(test.crossover(test.selection(5), 5))))
