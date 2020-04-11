# Duty Scheduling
I was a soldier in the past year, and something my superiors and my fellow soldiers always got worked up about was how to schedule watch duty. As always, in trying to make my life easier, this is my attempt at making a sufficiently fair watch duty schedule. 

## Overview
The problem involves the slotting of a number of people into 3 time slots over the course of the week. I used two methods: simulated annealing and a genetic algorithm. 

1. Simulated Annealing

   My high school math teacher used simulated annealing to make schedules for the entire school. I thought I'd try my hand at it. I actually started making this version when I was deployed, but it was made in Excel VBA; it actually didn't perform that badly though.

   This implementation was made in Python, using a pandas-centric data structure.

2. (Genetic Implementation)

   While looking for papers that would improve my simulated annealing implementation, I stumbled on using genetic algorithms for block scheduling. I've always been excited by biology (and yes, I did once watch a [Youtube video where a genetic algorithm beat Mario with ease](https://www.youtube.com/watch?v=qv6UVOQ0F44 "Genetically superior Mario video")), so I tried it. In short, it works reasonably well. Better than the simulated annealing implementation, in general.

   This implementation was also made in Python, using a numpy-centric data structure.

## In Depth
### DutySA Class
Below is the pseudocode (note that in this case, we are trying to minimize our evaluation score):
```
let best = best schedule
let current = current working state

let temp = temperature
let alpha = cooling factor

for number_of_cycles: 
	for number_of_trials_per_cycle:
		change current state
		if evaluation(current) > evaluation(best):
			if random_number(0,1) < exp(-|evaluation(current) - evaluation(best)|/temp): 
				best = current
			else: 
				reject current state
		else: 
			best = current
	temp = alpha * temp

return best schedule

```
As shown above, several things are needed: 

1. Schedule data structure: contains schedule, and schedule generation methods
2. Evaluation function: scores state
3. Alpha: controls the cooling of the temperature

#### Schedule Data Structure
The data structure contains an employee list, and a schedule as a pandas data frame. Below is the pandas data frame, visualized: 

![](https://github.com/ajeon66/scheduling/blob/master/images/datastructure.jpg "Pandas Schedule")

I experimented with two methods of changing state. The first method was simply a randomized schedule generator; it slotted a random selection of people into random slots. The second method involved swapping two slots; two random slots A and B were chosen, and the person in slot A is switched with the person in slot B. (something about why I chose both methods, and which method is better)

The evaluation function is simply the standard deviation of the total number of hours worked by each worker in the inputted schedule. Under this evaluation function, the best schedule is one that has every worker working for a similar number of hours. Of course, the ideal schedule has each person working a similar number of hours in addition to not having a single worker working for multiple shifts in a row, but to understand the simulated annealing algorithm better, I decided to simplify the problem question. 

#### Curiosities
I was curious as to how trial number per cycle affected overall performance - I suspected that there would not be a significant upgrade. Indeed, as shown in the table below, because the algorithm simply runs through a set number of trials to generate enough states to "work with", the trial number shouldn't make a huge difference. 

![](https://github.com/ajeon66/scheduling/blob/master/images/results/combined.png "Performance Based on Trials Per Cycle")

In general, the simulated annealing algorithm worked quite well. More interesting comparisons between simulated annealing and the genetic algorithm below.

### DutyGEN Class
Below is the pseudocode. 
```
population = generate_population()

for i in number_of_generations:
	parents = best_individuals(population)
	offspring = mutation(crossover(parents))

	population = parents + offspring
	
```
Similar to the DutySA class, we need a couple things:
1. Chromosome encoding: representation of a schedule
2. Population generation method
3. Parent selection method: to determine best individuals in population
4. Offspring generation method: involves crossover and point mutation

#### Genes, Jeans, and Chromosomes
The main problem to address in the chromosome encoding is the flattening of the information in a schedule into a one-dimensional list. The schedule has a total of 16 slots, so I created an array of length 16, with each entry being the worker on duty during that time slot and day. See below: 
![](https://github.com/ajeon66/scheduling/blob/master/images/gendatastructure.jpg "Chromosome")


