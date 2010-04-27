#!/usr/bin/env python

from __future__ import division
import random
from copy import deepcopy 
from math import exp

WOOD, STONE, IRON, FOOD = range(4)
Resources = [WOOD, STONE, IRON, FOOD]

class Map(object):
    """ Map layout

    Legend:
    Set pieces:
    F : farmland (empty space, can build)
    X : wall
    W : forrest
    R : rocks
    I : iron
    L : lake
    T : town hall
    Buildings
    C : castle
    H : woodcutter's hut
    O : cottage
    Q : quarry
    A : farm
    M : iron mine
    S : townhouse
    ...
    """

    def __init__(self, data):
        self.size = (len(data[0]), len(data))
        self.data = data
        self.legend = {'X' : Wall,
                       'F' : Field,
                       'W' : Forrest,
                       'H' : Woodcutter,
                       'S' : Sawmill,
                       'C' : Cottage
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
        self.produce = [0, 0, 0, 0]
        self.improve = [0, 0, 0, 0]
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
        self.removable = True
        self.improve[WOOD] = 25
        

class Lake(MapItem):
    
    def __init__(self):
        MapItem.__init__(self, name="Lake")
        self.removable = True
        self.improve[FOOD] = 50
        self.limited = 2

class Rock(MapItem):
    
    def __init__(self):
        MapItem.__init__(self, name="Rock")
        self.removable = True
        self.improve[STONE] = 25

class Iron(MapItem):
    
    def __init__(self):
        MapItem.__init__(self, name="Iron")
        self.removable = True
        self.improve[IRON] = 25

class TownHall(MapItem):
    
    def __init__(self):
        MapItem.__init__(self, name="TownHall")

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


Buildings = [Woodcutter, Cottage, Sawmill]

def scoring(value, weights):
    score = sum(i*j for i, j in zip(value, weights))
    return score

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
           
    currmap.printmap()
    print value, score

data = loadfile('sample.map')
mymap = Map(data)
weights = [1,1,1,1]

params = (weights)
simulation(mymap, params)
