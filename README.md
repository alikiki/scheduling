# Duty Scheduling
I was a soldier in the past year, and something my superiors and my fellow soldiers always got worked up about was how to schedule watch duty. As always, in trying to make my life easier, this is my attempt at making a sufficiently fair watch duty schedule. 

## Overview
I used two methods: simulated annealing and a genetic algorithm. 

1. Simulated Annealing

   My high school math teacher used simulated annealing to make schedules for the entire school. I thought I'd try my hand at it. I actually started making this version when I was deployed, but it was made in Excel VBA; it actually didn't perform that badly though.

   This implementation was made in Python, using a pandas-centric data structure.

2. (Genetic Implementation)

   While looking for papers that would improve my simulated annealing implementation, I stumbled on using genetic algorithms for block scheduling. I've always been excited by biology (and yes, I did once watch a [Youtube video where a genetic algorithm beat Mario with ease](https://www.youtube.com/watch?v=qv6UVOQ0F44 "Genetically superior Mario video")), so I tried it. In short, it works really, **really** well.

   This implementation was also made in Python, using a numpy-centric data structure.

## In Depth
### DutySA Class
### DutyGEN Class

