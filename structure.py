import pandas as pd
import random

class duty:
	"""
	Duty schedule 

	Instance variables: 
		people (list)
		table (dictionary)
		pdtable (pandas DataFrame)

	Methods:
		get_hours = gets number of hours worked for single person
		get_hours_all = gets number of hours worked for all people
	
	"""

	weekdays = [
		'Monday', 'Tuesday', 'Wednesday',
		'Thursday', 'Friday', 'Saturday', 'Sunday'
		]

	def __init__(self, people):
		#names list
		self.people = people

		#initial state : assigns people to slots randomly
		#### weekdays have 2 slots : 0800 ~ 0900, 1700 ~ 2400
		#### weekends have 3 slots : 0800 ~ 0900, 0900 ~ 1700, 1700 ~ 2400
		self.pdtable = pd.DataFrame(
			{hour : [random.choice(self.people) for _ in range(7)]
			if hour < 2 else [0 for i in range(5)]+[random.choice(self.people) for _ in range(2)]
			for hour in range(3)},index=duty.weekdays)


	#returns people and schedule
	def __repr__(self):
		return("people : {} \nschedule : {}".format(self.people, self.pdtable))

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
		return(pd.DataFrame({name : duty.get_hours(self, name) for name in self.people}, index=[0]))


################ tests ################
test = duty(['alpha', 'bravo', 'charlie', 'delta', 'echo', 'hotel', 'india'])
#print(test)
#print(test.people)
#print(test.table)
#print(test.pdtable)
#print(test.get_hours('echo'))
#print(test.get_hours_all())





		

	

