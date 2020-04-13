import pandas as pd
import numpy as np
import random

weekdays = [
		'Monday', 'Tuesday', 'Wednesday',
		'Thursday', 'Friday', 'Saturday', 'Sunday'
		]

class DutySA:
	"""
	DutySA : schedule data structure for simulated annealing

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
	"""

	def __init__(self, people):
		#names list
		self.people = people

		#initial state : assigns people to slots randomly
		self.pdtable = DutySA.change_state_random(self)

	#returns object variables
	def __repr__(self):
		return("people : {} \nschedule :\n{}".format(
			self.people, self.pdtable))

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
		return(pd.DataFrame({name : DutySA.get_hours(self, name) for name in self.people}, index=[0]))

	#gets standard deviation of hours worked
	def get_std(self):
		return(DutySA.get_hours_all(self).values.std(ddof=1))


	############ SIMULATED ANNEALING ############


	#changes state by randomly assigning people to slots in schedule
	def change_state_random(self):
		self.pdtable = pd.DataFrame(
			{hour : [random.choice(self.people) for _ in range(7)]
			if hour < 2 else [0 for i in range(5)]+[random.choice(self.people) for _ in range(2)]
			for hour in range(3)},index=weekdays)
		return(self.pdtable)


	#changes state by randomly switching two slots
	def change_state_switch(self):
		weekendOrday = random.randrange(0,2)
		#weekends < -- > weekends
		if weekendOrday == 0: DutySA.switcher(self, 0, 2, 0, 5)
		#weekdays < -- > weekdays
		else: DutySA.switcher(self, 0, 3, 5, 7)


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

class DutyGEN:
	"""
	DutyGEN : schedule data structure

	Instance variables: 
		people (list)
		ind (integer)
		gentable (numpy array)
		fitness (numpy array)

	Methods:
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

	def __init__(self, people, ind):
		#names list
		self.people = people

		#number of individuals per population
		self.ind = ind

		#generations table : initial pool
		self.gentable = np.random.random_integers(0, len(self.people)-1, size=(ind,16))

		#fitness of generation
		self.fitness = DutyGEN.fitness_gen(self, self.gentable)

	#returns object variables
	def __repr__(self):
		return("people : {} \ngeneration : \n{} \nfitness : {}".format(
			self.people, self.gentable, self.fitness))

	#helper : returns total working hours 
	def sum_single(self, ind):
		hours = np.array([1,7,1,7,1,7,1,7,1,7,1,7,8,1,7,8])
		sums = []

		#takes dot product of hours vector and binary individual vector
		for i in range(len(self.people)):
			wherepeople = (ind == i).astype(int)
			single_sum = np.sum(np.dot(hours, wherepeople))
			sums.append(single_sum)

		return(sums)

	#helper : returns fitness of an individual
	def fitness_single(self, ind):
		return(np.std(DutyGEN.sum_single(self,ind)))

	#returns fitness of whole generation (list)
	def fitness_gen(self, generation):
		fitness = []
		for i in range(len(generation)):
			fitness.append(DutyGEN.fitness_single(self, generation[i]))

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
		parents = DutyGEN.selection(self, int((self.ind)/2))
		offspring = DutyGEN.mutation(self, DutyGEN.crossover(self, parents, self.ind - len(parents))).astype(int)
		self.gentable =  np.concatenate([parents, offspring])
		self.fitness = DutyGEN.fitness_gen(self, self.gentable)

	#returns best individual
	def best_individual(self):
		return(self.gentable[np.argmin(self.fitness)])

	#returns best fitness 
	def best_fitness(self):
		return(self.fitness[np.argmin(self.fitness)])

	#returns best schedule and best fitness
	def return_optimal(self):
		return("Best schedule: {} \nFitness: {}".format(
			DutyGEN.best_individual(self), DutyGEN.best_fitness(self)))

	#status updater
	def status(self, cycle):
		print("Generation: \n{} \n Fitness: \n{} \n Cycle: {} \n {}".format(
			self.gentable, self.fitness, cycle, DutyGEN.return_optimal(self)))

	#converts best individual to a readable schedule 
	def convert(self, sched):
		names = [self.people[i] for i in sched]
		return(pd.DataFrame({
			'Monday' : [names[0], names[1], "-"],
			'Tuesday' : [names[2], names[3], "-"],
			'Wednesday' : [names[4], names[5], "-"],
			'Thursday' : [names[6], names[7], "-"],
			'Friday' : [names[8], names[9], "-"],
			'Saturday' : [names[10], names[11], names[12]],
			'Sunday' : [names[13], names[14], names[15]]}, 
			columns=weekdays))

################ tests ################
#test = DutySA(['alpha', 'bravo', 'charlie', 'delta', 'echo', 'hotel', 'india'])
#print(test)
#print(test.get_std())
#print(test.people)
#print(test.table)
#print(test.pdtable)
#print(test.get_hours('echo'))
#print(test.get_hours_all())
#print(test.get_std())
#test.change_state_switch()

#test = DutyGEN(['a','b','c','d','e','f','g'], 100)
#print("Generation: \n{}".format(test.gentable))
#print("Fitness: \n{}".format(test.fitness))
#print(test.selection(5))
#print(test.fitness_gen(test.selection(5)))
#print(test.crossover(test.selection(5), 5))
#print(test.fitness_gen(test.crossover(test.selection(5), 5)))
#print(test.mutation(test.crossover(test.selection(5), 5)))
#print(test.fitness_gen(test.mutation(test.crossover(test.selection(5), 5))))
#print(test.convert([4, 3, 5, 4, 2, 5, 1, 3, 1, 5, 6, 6, 0, 2, 2, 1]))


