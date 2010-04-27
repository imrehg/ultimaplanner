#!/usr/bin/env python


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
        self.legend = {'X' : Wall(),
                       'F' : Field(),
                       'W' : Forrest(),
                       }
        self.reverselegend = dict([(v, k) for (k, v) in self.legend.iteritems()])
        self.setmap(data)
        self.printmap()

    def setmap(self, data):
        self.mapped = []
        for y in xrange(self.getysize()):
            temp = []
            for x in xrange(self.getxsize()):
                temp.append(self.legend[data[y][x]])
            self.mapped.append(temp)

    def printmap(self):
        for line in xrange(self.getysize()):
            marks = []
            for point in xrange(self.getxsize()):
                marks.append(self.reverselegend[self.mapped[line][point]])
#                print marks
            print "".join(marks)
        pass

    def buildsites(self):
        for y in xrange(self.getysize()):
            for y in xrange(self.getxsize()):
                pass

    def getxsize(self):
        return self.size[0]

    def getysize(self):
        return self.size[1]


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
        self.name = name
        self.produce = {WOOD : 0, STONE : 0, IRON : 0, FOOD : 0}
        self.improve = {WOOD : 0, STONE : 0, IRON : 0, FOOD : 0}
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
        self.improve[WOOD] = 100
        self.limited = 1


data = loadfile('sample.map')
map = Map(data)
