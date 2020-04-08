# Duty Scheduling
I was a soldier in the past year, and something my superiors and my fellow soldiers always got worked up about was how to schedule watch duty. As always, in trying to make my life easier, this is my attempt at making a sufficiently fair watch duty schedule. 

## Overview
I used two methods: simulated annealing and a genetic algorithm. 

1. Simulated Annealing

   My high school math teacher used simulated annealing to make schedules for the entire school. I thought I'd try my hand at it. I actually started making this version when I was deployed, but it was made in Excel VBA; it actually didn't perform that badly though.

   This implementation was made in Python, using a pandas-centric data structure.

2. (Genetic Implementation)

   While looking for papers that would improve my simulated annealing implementation, I stumbled on using genetic algorithms for block scheduling. I've always been excited by biology (and yes, I did once watch a [Youtube video where a genetic algorithm beat Mario with ease](https://www.youtube.com/watch?v=qv6UVOQ0F44 "Genetically superior Mario video")), so I tried it. In short, it works reasonably well. Better than the simulated annealing implementation, in general.

   This implementation was also made in Python, using a numpy-centric data structure.

## In Depth
### DutySA Class
#### Overview
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
			if random_number(0,1) < exp(-|evaluation(current) - evaluation(best)|/temp): accept current state
			else: reject current state
		else: accept current state
	temp = alpha * temp

return best schedule

```

I was curious as to how trial number per cycle affected overall performance - I suspected that there would not be a significant upgrade. Indeed, as shown in the table below, because the algorithm simply runs through a set number of trials to generate enough states to "work with", the trial number shouldn't make a huge difference. 

![](https://github.com/ajeon66/scheduling/blob/master/images/results/combined.png "Performance Based on Trials Per Cycle")

### DutyGEN Class




