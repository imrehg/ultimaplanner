#!/usr/bin/env python



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
        self.printmap()
        self.nobuild = ['X', 'F', 'R', 'I', 'L', 'T']

    def setmap(self, data):
        pass

    def printmap(self):
        for line in xrange(self.getysize()):
            print "".join(self.data[line])
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

    def __init__(self, name, buildable):
        self.name = name
        self.buildable = buildable

    def improve(self, other):
        return 0
        

class Wall(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="Wall", buildable=False)


class Forrest(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="Forrest", buildable=True)


class Lake(MapItem):
    
    def __init__(self):
        MapItem.__init__(self, name="Lake", buildable=False)


class Rock(MapItem):
    
    def __init__(self):
        MapItem.__init__(self, name="Rock", buildable=False)

class Iron(MapItem):
    
    def __init__(self):
        MapItem.__init__(self, name="Iron", buildable=False)

class TownHall(MapItem):
    
    def __init__(self):
        MapItem.__init__(self, name="TownHall", buildable=False)

class Woodcutter(MapItem):

    def __init__(self):
        MapItem.__init__(self, name="WoodCutter", buildable=True)

class Cottage:
    
    def __init__(self):
        MapItem.__init__(self, name="Cottage", buildable=True)



data = loadfile('sample.map')
map = Map(data)
