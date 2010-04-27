#!/usr/bin/env python

from __future__ import division
import random
from copy import deepcopy 
from math import exp, sqrt
from pylab import plot, show

WOOD, STONE, IRON, FOOD, GOLD = range(5)
Resources = [WOOD, STONE, IRON, FOOD, GOLD]
Terraforming = True

class Map(object):
    """ Map layout
    """

    def __init__(self, data):
        self.size = (len(data[0]), len(data))
        self.data = data
        self.legend = {'#' : Wall,
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
        self.reverselegend = dict([(v, k) for (k, v) in self.legend.iteritems()])
        self.setmap(data)

    def setmap(self, data):
        self.mapped = []
        for y in xrange(self.getysize()):
            temp = []
            for x in xrange(self.getxsize()):
                temp.append(self.legend[data[y][x]]())
            self.mapped.append(temp)

    def printmap(self):
        for line in xrange(self.getysize()):
            marks = []
            for point in xrange(self.getxsize()):
                marks.append(self.reverselegend[type(self.mapped[line][point])])
#                print marks
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
                building.affectedby = []
        for y in xrange(self.getysize()):
            for x in xrange(self.getxsize()):
                building = self.mapped[y][x]
                if (sum(building.improve) > 0):
                    neigh = self.neighbours((x,y))
                    for i in neigh:
                        n = self.mapped[i[1]][i[0]]
                        affected = False
                        for r in Resources:
                            if (building.improve[r] > 0) and (n.produce[r] >0):
                                affected = True
                        if affected and building.limited == 0 and (building not in n.affectedby):
                            n.affectedby.append(building)
                        elif affected and building.limited > 0:
                            num = 0
                            for aff in n.affectedby:
                                if isinstance(aff, type(building)):
                                    num += 1
                            if num < building.limited:
                                n.affectedby.append(building)
        for y in xrange(self.getysize()):
            for x in xrange(self.getxsize()):
                building = self.mapped[y][x]
                effect = [0] * len(Resources)
                if sum(building.produce) > 0:
                    for i, aff in enumerate(building.affectedby):
                        for res in Resources:
                            effect[res] += aff.improve[res]
                for i in xrange(len(Resources)):
                    out[i] += int(building.produce[i]*(1 + effect[i]/100.0))
        return out

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

    def __init__(self, name):
#        self._creator = creator
        self.name = name
        self.produce = [0] * len(Resources)
        self.improve = [0] * len(Resources)
        self.affectedby = []
        self.limited = 0
        self.buildable = False
        self.removable = False


class Wall(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="Wall")

class Field(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="Field")
        self.buildable = True
        self.removable = True
        self.improve[FOOD] = 25

class Forrest(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="Forrest")
        self.removable = Terraforming
        self.improve[WOOD] = 25

class Lake(MapItem):
    
    def __init__(self):
        MapItem.__init__(self, name="Lake")
        self.removable = Terraforming
        self.improve[FOOD] = 50
        self.limited = 2

class Rock(MapItem):
    
    def __init__(self):
        MapItem.__init__(self, name="Rock")
        self.removable = Terraforming
        self.improve[STONE] = 25

class Iron(MapItem):
    
    def __init__(self):
        MapItem.__init__(self, name="Iron")
        self.removable = Terraforming
        self.improve[IRON] = 25

class Townhall(MapItem):
    
    def __init__(self):
        MapItem.__init__(self, name="Townhall")

class Woodcutter(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="WoodCutter")
        self.buildable = True
        self.removable = True
        self.produce[WOOD] = 300

class Cottage(MapItem):
    
    def __init__(self):
        MapItem.__init__(self, name="Cottage")
        self.buildable = True
        self.removable = True
        self.improve[WOOD] = 50
        self.improve[STONE] = 50
        self.improve[IRON] = 50
        self.improve[FOOD] = 50

class Sawmill(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="Sawmill")
        self.buildable = True
        self.removable = True
        self.improve[WOOD] = 75
        self.limited = 1

class Mine(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="Mine")
        self.buildable = True
        self.removable = True
        self.produce[IRON] = 300

class Foundry(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="Foundry")
        self.buildable = True
        self.removable = True
        self.improve[IRON] = 75
        self.limited = 1

class Quarry(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="Quarry")
        self.buildable = True
        self.removable = True
        self.produce[STONE] = 300

class Stonemason(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="Stonemason")
        self.buildable = True
        self.removable = True
        self.improve[STONE] = 75
        self.limited = 1

class Farm(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="Farm")
        self.buildable = True
        self.removable = True
        self.produce[FOOD] = 400

class Mill(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="Mill")
        self.buildable = True
        self.removable = True
        self.improve[FOOD] = 75
        self.limited = 1

class Townhouse(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="Townhouse")
        self.buildable = True
        self.removable = True
        self.produce[GOLD] = 400

class Marketplace(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="Marketplace")
        self.buildable = True
        self.removable = True
        self.improve[GOLD] = 20
        self.limited = 1

Buildings = [Woodcutter, Cottage, Sawmill, Mine, Foundry, Quarry, Stonemason,
             Farm, Mill, Townhouse, Marketplace]

def scoring(value, weights):
    score = sum(i*j for i, j in zip(value, weights))
    sumw = sum(weights)
    multi = 0
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
    startmap = deepcopy(mymap)
    currmap = deepcopy(mymap)
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
    value = currmap.getoutput()
    score = scoring(value, weights)
    scorehist = [score]
    for n in xrange(nsim):
        pos = random.randint(0, naltpos-1)
        newmap = deepcopy(currmap)
        x,y = (altpos[pos][0], altpos[pos][1])
        possible = Buildings[:]
#        possible.append(startmap[y][x])
        newbuild = random.randint(0, len(possible)-1)
        newmap.mapped[y][x] = possible[newbuild]()
        newvalue = newmap.getoutput()
        newscore = scoring(newvalue, weights)
        if newscore > score or badbutgood(score, newscore, T(n, nsim)):
            value = newvalue
            score = newscore
            currmap = deepcopy(newmap)
        scorehist.append(score)
    currmap.printmap()
    print value, score
    plot(scorehist)
    show()

data = loadfile('sample.map')
mymap = Map(data)
weights = [1,1,1,1,1]
params = (weights)
simulation(mymap, params)
