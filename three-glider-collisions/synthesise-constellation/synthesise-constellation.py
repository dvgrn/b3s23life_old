#C synthesise-constellation-v1.0.py
# This is Goldtiger997's original version from
#   http://www.conwaylife.com/forums/viewtopic.php?p=68370#p68370

import golly as g
g.setrule("B3/S23")

offset = 0
with open("consts.txt","r") as fl:
    consts = (fl.read()[1:-1]).split(", ")
with open("cols.txt","r") as fl:
    cols = (fl.read()[2:-2]).split("], [")
#g.note(str(cols[:20]))
i = 0
for i in range(0,len(cols)):
	cols[i] = cols[i].split(", ")

def bijoscar(maxsteps):

    initpop = int(g.getpop())
    initrect = g.getrect()
    if (len(initrect) == 0):
        return 0
    inithash = g.hash(initrect)

    for i in xrange(maxsteps):

        g.run(1)

        if (int(g.getpop()) == initpop): 

            prect = g.getrect()
            phash = g.hash(prect)

            if (phash == inithash):

                period = i + 1

                if (prect == initrect):
                    return period
                else:
                    return -period 
    return -1


def canonise():
    
    p = bijoscar(4)
    
    representation = "#"
    for i in range(abs(p)):
        rect = g.getrect()
        representation = compare_representations(representation, canonise_orientation(rect[2], rect[3], rect[0], rect[1], 1, 0, 0, 1))
        representation = compare_representations(representation, canonise_orientation(rect[2], rect[3], rect[0]+rect[2]-1, rect[1], -1, 0, 0, 1))
        representation = compare_representations(representation, canonise_orientation(rect[2], rect[3], rect[0], rect[1]+rect[3]-1, 1, 0, 0, -1))
        representation = compare_representations(representation, canonise_orientation(rect[2], rect[3], rect[0]+rect[2]-1, rect[1]+rect[3]-1, -1, 0, 0, -1))
        representation = compare_representations(representation, canonise_orientation(rect[3], rect[2], rect[0], rect[1], 0, 1, 1, 0))
        representation = compare_representations(representation, canonise_orientation(rect[3], rect[2], rect[0]+rect[2]-1, rect[1], 0, -1, 1, 0))
        representation = compare_representations(representation, canonise_orientation(rect[3], rect[2], rect[0], rect[1]+rect[3]-1, 0, 1, -1, 0))
        representation = compare_representations(representation, canonise_orientation(rect[3], rect[2], rect[0]+rect[2]-1, rect[1]+rect[3]-1, 0, -1, -1, 0))
        g.run(1)
    
    if (p<0):
        prefix = "q"+str(abs(p))
    elif (p==1):
        prefix = "s"+str(g.getpop())
    else:
        prefix = "p"+str(p)

    return "x"+prefix+"_"+representation

# A subroutine used by canonise:
def canonise_orientation(length, breadth, ox, oy, a, b, c, d):

    representation = ""

    chars = "0123456789abcdefghijklmnopqrstuvwxyz"

    for v in xrange(int((breadth-1)/5)+1):
        zeroes = 0
        if (v != 0):
            representation += "z"
        for u in xrange(length):
            baudot = 0
            for w in xrange(5):
                x = ox + a*u + b*(5*v + w)
                y = oy + c*u + d*(5*v + w)
                baudot = (baudot >> 1) + 16*g.getcell(x, y)
            if (baudot == 0):
                zeroes += 1
            else:
                if (zeroes > 0):
                    if (zeroes == 1):
                        representation += "0"
                    elif (zeroes == 2):
                        representation += "w"
                    elif (zeroes == 3):
                        representation += "x"
                    else:
                        representation += "y"
                        representation += chars[zeroes - 4]
                zeroes = 0     
                representation += chars[baudot]
    return representation

# Compares strings first by length, then by lexicographical ordering.
# A hash character is worse than anything else.
def compare_representations(a, b):

    if (a == "#"):
        return b
    elif (b == "#"):
        return a
    elif (len(a) < len(b)):
        return a
    elif (len(b) < len(a)):
        return b
    elif (a < b):
        return a
    else:
        return b

pattern = canonise()
if pattern in consts:
    g.new("solutions")
    loc = consts.index(pattern)
    g.show(str(len(cols[loc])) + " collisions found")
    g.setname(pattern)
    for e in cols[loc]:
	    g.putcells(g.parse(e),offset,0)
	    offset += 50
else:
    g.note("No 3 glider collision found for that constellation. Better luck next time")
