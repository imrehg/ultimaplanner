Lord of Ultima city planner
===========================

City planning is not an easy task in Lord of Ultima [1], as there are many
competing designs that have to be balanced. The different resources have
very different priorities, and some of the planning advice one could give
can be quite counter-intuitive.

The aim of this software is to help your city to achieve her full potential,
whether you want to have large number of resources, troops, gold, or a good
balance...


Idea
====

The optimal city layout is found through a method called "simulated
annealing" [2], borrowed from physics simulations.

The simulations repeats for a number of turns. In every turn:
* A random site is selected
* The type of building on that site is changed randomly
* If the resulting layout is more benefitial (has a higher weighted score
as defined later) then it is adopted.
* If it has lower score, than it is adopted or discared with a certain
probability that is based on a virtual "temperature" parameter. Higher
temperature means more variations.

The wighted score comes from weighing the final achiveable amount of
resources and other "counted" items:
* Wood
* Stone
* Iron
* Gold
* Army unit numbers
* Different types of army units
* Storage space
(maybe other measures as well later)

E.g. one can have larger than average weight assigned to "wood" to potentially 
achive higher output of that in the end.

Progress
========

Idea and path layed down, now getting to work, yeah! :)

License
=======

See Licence.txt

[1]: http://lordofultima.com/ "Lord of Ultima"
[2]: http://en.wikipedia.org/wiki/Simulated_annealing "Wikipedia: Simulated annealing"