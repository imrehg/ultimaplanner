#!/usr/bin/env python

from __future__ import division
import random
from copy import copy
from math import exp, sqrt
from pylab import plot, show

WOOD, STONE, IRON, FOOD, GOLD = range(5)
Resources = [WOOD, STONE, IRON, FOOD, GOLD]
Terraforming = True

def addlists(a, b):
    return map(sum, zip(*[a, b]))

def negate(a):
    return [-1 * x for x in a]

class Map(object):
    """ Map layout
    """

    def __init__(self, data):
        self.size = (len(data[0]), len(data))
        self.setmap(data)
        self.score = self.getoutput()

    def setmap(self, data):
        self.mapped = []
        for y in xrange(self.getysize()):
            temp = []
            for x in xrange(self.getxsize()):
                temp.append(legend[data[y][x]]())
            self.mapped.append(temp)

    def printmap(self):
        for line in xrange(self.getysize()):
            marks = []
            for point in xrange(self.getxsize()):
                marks.append(reverselegend[type(self.mapped[line][point])])
            print "".join(marks)
        pass

    def buildsites(self):
        for y in xrange(self.getysize()):
            for x in xrange(self.getxsize()):
                pass

    def getxsize(self):
        return self.size[0]

    def getysize(self):
        return self.size[1]

    def getoutput(self):
        out = [0] * len(Resources)
        for y in xrange(self.getysize()):
            for x in xrange(self.getxsize()):
                building = self.mapped[y][x]
                if sum(building.produce) > 0:
                    out = addlists(out, self.getscore((x, y)))
        return out

    def getscore(self, pos):
        effect = [0] * len(Resources)
        out = [0] * len(Resources)
        x, y = pos
        building = self.mapped[y][x]
        affectedby = self.updateaffected(pos)
        for i, aff in enumerate(affectedby):
            for res in Resources:
                effect[res] += aff.improve[res]
        for i in xrange(len(Resources)):
            out[i] += int(building.produce[i]*(1 + effect[i]/100.0))
        return out

    def updateaffected(self, pos):
        x, y = pos
        building = self.mapped[y][x]
        affectedby = []
        for neighpos in self.neighbours(pos):
            neigh = self.mapped[neighpos[1]][neighpos[0]]
            affected = False
            for r in Resources:
                if (neigh.improve[r] > 0) and (building.produce[r] > 0):
                    affected = True
                if affected and neigh.limited == 0 and \
                        (neigh not in affectedby):
                    affectedby.append(neigh)
                elif affected and neigh.limited > 0:
                    num = 0
                    for aff in affectedby:
                        if isinstance(aff, type(neigh)):
                            num += 1
                    if num < neigh.limited:
                        affectedby.append(neigh)
        return affectedby

    def updatemap(self, pos, building):
        x, y = pos
        # scoremodify = [0] * len(Resources)
        # # Before
        # scoremodify = addlists(negate(self.getscore(pos)),
        #                        scoremodify)
        # for neigh in self.neighbours(pos):
        #     scoremodify = addlists(negate(self.getscore(neigh)),
        #                            scoremodify)
        # # After
        self.mapped[y][x] = building
        # scoremodify = addlists(self.getscore(pos),
        #                        scoremodify)
        # for neigh in self.neighbours(pos):
        #     scoremodify = addlists(self.getscore(neigh),
        #                            scoremodify)
        # self.score = addlists(self.score, scoremodify)
        self.score = self.getoutput()

    def neighbours(self, pos):
        x, y = pos
        minx = (x - 1) if (x > 0) else 0
        maxx = (x + 1) if (x < (self.getxsize()-1)) else self.getxsize()-1
        miny = (y - 1) if (y > 0) else 0
        maxy = (y + 1) if (y < (self.getysize()-1)) else self.getysize()-1
        ns = []
        for i in xrange(minx, maxx+1):
            for j in xrange(miny, maxy+1):
                if not ((i == x) and (j == y)):
                    ns.append((i, j))
        return ns


def loadfile(filename):
    datafile = open(filename, "r")
    alldata = []
    for line in datafile.readlines():
        line = line.strip()
        temp = []
        for i in xrange(len(line)):
            temp.append(line[i])
        alldata.append(temp)
    datafile.close()
    return alldata


class MapItem(object):

    def __init__(self):
        self.produce = [0] * len(Resources)
        self.improve = [0] * len(Resources)
        self.limited = 0
        self.buildable = False
        self.removable = False


class Wall(MapItem):

    def __init__(self):
        MapItem.__init__(self)

class Field(MapItem):

    def __init__(self):
        MapItem.__init__(self)
        self.buildable = True
        self.removable = True
        self.improve[FOOD] = 25

class Forrest(MapItem):

    def __init__(self):
        MapItem.__init__(self)
        self.removable = Terraforming
        self.improve[WOOD] = 25

class Lake(MapItem):
    
    def __init__(self):
        MapItem.__init__(self)
        self.removable = Terraforming
        self.improve[FOOD] = 50
        self.limited = 2

class Rock(MapItem):
    
    def __init__(self):
        MapItem.__init__(self)
        self.removable = Terraforming
        self.improve[STONE] = 25

class Iron(MapItem):
    
    def __init__(self):
        MapItem.__init__(self)
        self.removable = Terraforming
        self.improve[IRON] = 25

class Townhall(MapItem):
    
    def __init__(self):
        MapItem.__init__(self)

class Woodcutter(MapItem):

    def __init__(self):
        MapItem.__init__(self)
        self.buildable = True
        self.removable = True
        self.produce[WOOD] = 300

class Cottage(MapItem):
    
    def __init__(self):
        MapItem.__init__(self)
        self.buildable = True
        self.removable = True
        self.improve[WOOD] = 50
        self.improve[STONE] = 50
        self.improve[IRON] = 50
        self.improve[FOOD] = 50

class Sawmill(MapItem):

    def __init__(self):
        MapItem.__init__(self)
        self.buildable = True
        self.removable = True
        self.improve[WOOD] = 75
        self.limited = 1

class Mine(MapItem):

    def __init__(self):
        MapItem.__init__(self)
        self.buildable = True
        self.removable = True
        self.produce[IRON] = 300

class Foundry(MapItem):

    def __init__(self):
        MapItem.__init__(self)
        self.buildable = True
        self.removable = True
        self.improve[IRON] = 75
        self.limited = 1

class Quarry(MapItem):

    def __init__(self):
        MapItem.__init__(self)
        self.buildable = True
        self.removable = True
        self.produce[STONE] = 300

class Stonemason(MapItem):

    def __init__(self):
        MapItem.__init__(self)
        self.buildable = True
        self.removable = True
        self.improve[STONE] = 75
        self.limited = 1

class Farm(MapItem):

    def __init__(self):
        MapItem.__init__(self)
        self.buildable = True
        self.removable = True
        self.produce[FOOD] = 400

class Mill(MapItem):

    def __init__(self):
        MapItem.__init__(self)
        self.buildable = True
        self.removable = True
        self.improve[FOOD] = 75
        self.limited = 1

class Townhouse(MapItem):

    def __init__(self):
        MapItem.__init__(self)
        self.buildable = True
        self.removable = True
        self.produce[GOLD] = 400

class Marketplace(MapItem):

    def __init__(self):
        MapItem.__init__(self)
        self.buildable = True
        self.removable = True
        self.improve[GOLD] = 20
        self.limited = 1

Buildings = [Woodcutter, Cottage, Sawmill, Mine, Foundry, Quarry, Stonemason,
             Farm, Mill, Townhouse, Marketplace]

legend = {'#' : Wall,
          '-' : Field,
          '.' : Forrest,
          ':' : Rock,
          ',' : Iron,
          ';' : Lake,
          'W' : Woodcutter,
          'L' : Sawmill,
          'C' : Cottage,
          'Q' : Quarry,
          'A' : Stonemason,
          'I' : Mine,
          'D' : Foundry,
          'F' : Farm,
          'M' : Mill,
          'U' : Townhouse,
          'P' : Marketplace,
          'T' : Townhall,
          }
reverselegend = dict([(v, k) for (k, v) in legend.iteritems()])

def scoring(value, weights):
    score = sum(i*j for i, j in zip(value, weights))
    sumw = sum(weights)
    multi = 0
    if score == 0:
        return 0
    for i, v in enumerate(value):
        b = weights[i] * v / score 
        bb = weights[i] / sumw
        multi += 1-sqrt(abs(b - bb))
    return score * multi / 5

def T(n, nmax):
    T0 = 500.0
    return (nmax-n+1)/nmax*T0

def badbutgood(e0, e1, temp):
    if random.random() < exp((e1-e0)/temp):
        return True
    else:
        return False
    

def simulation(mymap, params):
    startmap = copy(mymap)
    currmap = copy(mymap)
    weights = params
    maxx = mymap.getxsize()
    maxy = mymap.getysize()
    altpos = []
    for x in xrange(0, maxx):
        for y in xrange(0, maxy):
            if mymap.mapped[y][x].removable:
                altpos.append((x,y))
    naltpos = len(altpos)
    nsim = 1000
    value = currmap.score
    score = scoring(value, weights)
    scorehist = [score]
    for n in xrange(nsim):
        pos = random.randint(0, naltpos-1)
        newmap = copy(currmap)
        x,y = (altpos[pos][0], altpos[pos][1])
        possible = Buildings[:]
        newbuild = random.randint(0, len(possible)-1)
        newmap.updatemap((x,y), possible[newbuild]())
        newvalue = newmap.score
        newscore = scoring(newvalue, weights)
        if newscore > score or badbutgood(score, newscore, T(n, nsim)):
            value = newvalue
            score = newscore
            currmap = copy(newmap)
        scorehist.append(score)
    currmap.printmap()
    print value, score
    plot(scorehist)
    show()

def main():
    data = loadfile('sample.map')
    mymap = Map(data)
    weights = [1,1,1,1,1]
    params = (weights)
    simulation(mymap, params)

if __name__ == '__main__':
    main()
