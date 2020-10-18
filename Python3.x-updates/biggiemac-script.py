# Golly selection directly to catagolue page
# stolen shamelessly from apgsearch.  Thanks Adam!
# biggiemac, 4 February 2016
# http://www.conwaylife.com/forums/viewtopic.php?f=9&t=2032#p27202
# Updated to work correctly with Golly 4.0+ and Python 3.x, 18 October 2020

import golly as g
import webbrowser

def bijoscar(maxsteps):

    initpop = int(g.getpop())
    initrect = g.getrect()
    if (len(initrect) == 0):
        return 0
    inithash = g.hash(initrect)

    for i in range(maxsteps):

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

    p = bijoscar(1000)

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

    rule = str.replace(g.getrule(),"/","").lower()
    
    webbrowser.open_new("http://catagolue.appspot.com/object?apgcode=x"+prefix+"_"+representation+"&rule="+rule)

# A subroutine used by canonise:
def canonise_orientation(length, breadth, ox, oy, a, b, c, d):

    representation = ""

    chars = "0123456789abcdefghijklmnopqrstuvwxyz"

    for v in range(int((breadth-1)/5)+1):
        zeroes = 0
        if (v != 0):
            representation += "z"
        for u in range(length):
            baudot = 0
            for w in range(5):
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

g.duplicate()
g.clear(1)
canonise()
