# MAPper.py
# Changes a given MAP rule one state at a time, much faster than by hand.
# The way it works will switch the existing transition input.
# Solution is shown and copied to clipboard, prefixed with MAP.
# Author: Rhombic
# Updated to work with Python 3.x, 19 October 2020

import golly as g
rule = g.getstring("Initial MAP rule to modify (default is CGoL) without the MAP prefix. Leave blank to start from scratch (B/S)","ARYXfhZofugWaH7oaIDogBZofuhogOiAaIDogIAAgAAWaH7oaIDogGiA6ICAAIAAaIDogIAAgACAAIAAAAAAAA")
if rule == "":
    rule="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
changes = int(g.getstring("How many changes are you planning?","1"))
for i in range(changes):
    newcase = g.getstring("Binary code to implement:","000000000")
    defect = int(newcase,2)
    base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    rulepos = (defect-(defect%6))//6
    checkcase = int(base64.index(rule[rulepos]))
    bcheckcase = "{0:06b}".format(checkcase)
    if bcheckcase[defect%6] == "1":
        newdec = int(bin(base64.index(rule[rulepos]))[2:])-int(bin(2**(5-(defect%6)))[2:])
    elif bcheckcase[defect%6] == "0":
        newdec = int(bin(base64.index(rule[rulepos]))[2:])+int(bin(2**(5-(defect%6)))[2:])
    newdecnum = int(str(newdec), 2)
    pointdefect = base64[newdecnum]
    newrule = rule[0:rulepos]+pointdefect+rule[(rulepos+1):len(rule)]
    g.show("Last transition changed: "+str(pointdefect)+" replaced "+str(rule[rulepos])+" at position "+str(rulepos)+", new rule is MAP"+newrule)
    rule = newrule
    
g.setclipstr("MAP"+newrule)
