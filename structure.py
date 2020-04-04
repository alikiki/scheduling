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

		gengeneration = generates 
	"""

	weekdays = [
		'Monday', 'Tuesday', 'Wednesday',
		'Thursday', 'Friday', 'Saturday', 'Sunday'
		]

	def __init__(self, people, ind):
		#names list
		self.people = people

		#initial state : assigns people to slots randomly
		#### weekdays have 2 slots : 0800 ~ 0900, 1700 ~ 2400
		#### weekends have 3 slots : 0800 ~ 0900, 0900 ~ 1700, 1700 ~ 2400
		self.pdtable = Duty.change_state_random(self)

		#generations table : initial pool
		self.gentable = np.random.random_integers(0, len(self.people), size=(ind,16))

		#fitness
		self.fitness = Duty.fitness(self)

	#returns people and schedule
	def __repr__(self):
		return("people : {} \nschedule :\n{}".format(self.people, self.pdtable))

	#total working hours for single person
	#person (string)
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

	########### GENETIC #############

	#helper : returns fitness of individuals
	def fitness_single(self, ind):
		hours = np.array([1,7,1,7,1,7,1,7,1,7,1,7,8,1,7,8])
		sums = []

		for i in range(len(self.people)):
			wherepeople = (ind == i).astype(int)
			single_sum = np.sum(np.dot(hours, wherepeople))
			sums.append(single_sum)

		return(np.std(sums))

	#returns fitness of generation (list)
	def fitness(self):
		number_of_ind = len(self.gentable)

		fitness = []
		for i in range(number_of_ind):
			fitness.append(Duty.fitness_single(self, self.gentable[i]))

		return(np.array(fitness))

	#next generation
	def selection(self):
		ind = np.argpartition(self.fitness, 2)[:2]
		parents = self.gentable[ind]
		parents_fitness = self.fitness[ind]

		return(parents, parents_fitness)


################ tests ################
test = Duty(['alpha', 'bravo', 'charlie', 'delta', 'echo', 'hotel', 'india'], 10**4)
#print(test)
#print(test.get_std())
#print(test.people)
#print(test.table)
#print(test.pdtable)
#print(test.get_hours('echo'))
#print(test.get_hours_all())
#print(test.get_std())
#test.change_state_switch()

print("Generation: \n{}".format(test.gentable))
print("Fitness: \n{}".format(test.fitness))

#print(test.selection())









		

	

