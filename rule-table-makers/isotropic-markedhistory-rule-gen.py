# isotropic-markedhistory-rule-gen.py, version 1.0
#   Minimal changes made to isotropic-rule-gen.py version 1.1
#     ( https://github.com/dvgrn/b3s23life/blob/master/rule-table-makers/isotropic-rule-gen.py )
#     to produce an equivalent seven-state rule with state-2 History cells,
#     state-3 and state-5 marked ON cells, state-4 marked OFF cells,
#     and state-6 impervious boundary cells, all equivalent to B3/S23 LifeHistory.
#
# Most of the code is unchanged from isotropic-rule.py / isotropicRulegen.py,
# an auxillary rule generator from wildmyron's non-totalistic version of apgsearch.
# The rulespace is the set of isotropic non-totalistic rules on the Moore
# neighbourhood, using Alan Hensel's notation.
# See http://www.ibiblio.org/lifepatterns/neighbors2.html
# Generate a History rule table for an isotropic rule using Alan Hensel's
# isotropic, non-totalistic rule format for CA on the Moore neighbourhood

import golly as g
import os

# Generates the helper rules for apgsearch-isotropic, given a base isotropic 
# rule in Hensel's notation.
class RuleGenerator:

    # notationdict adapted from Eric Goldstein's HenselNotation->Ruletable(1.3).py
    # ( http://conwaylife.com/forums/viewtopic.php?p=6815#p6815 )
    # Modified for neighbourhood2 version of Hensel's notation
    notationdict = {
        "0"  : [0,0,0,0,0,0,0,0],   #    
        "1e" : [1,0,0,0,0,0,0,0],   #   N
        "1c" : [0,1,0,0,0,0,0,0],   #   NE
        "2a" : [1,1,0,0,0,0,0,0],   #   N,  NE
        "2e" : [1,0,1,0,0,0,0,0],   #   N,  E
        "2k" : [1,0,0,1,0,0,0,0],   #   N,  SE
        "2i" : [1,0,0,0,1,0,0,0],   #   N,  S
        "2c" : [0,1,0,1,0,0,0,0],   #   NE, SE
        "2n" : [0,1,0,0,0,1,0,0],   #   NE, SW
        "3a" : [1,1,1,0,0,0,0,0],   #   N,  NE, E
        "3n" : [1,1,0,1,0,0,0,0],   #   N,  NE, SE
        "3r" : [1,1,0,0,1,0,0,0],   #   N,  NE, S
        "3q" : [1,1,0,0,0,1,0,0],   #   N,  NE, SW
        "3j" : [1,1,0,0,0,0,1,0],   #   N,  NE, W
        "3i" : [1,1,0,0,0,0,0,1],   #   N,  NE, NW
        "3e" : [1,0,1,0,1,0,0,0],   #   N,  E,  S
        "3k" : [1,0,1,0,0,1,0,0],   #   N,  E,  SW
        "3y" : [1,0,0,1,0,1,0,0],   #   N,  SE, SW
        "3c" : [0,1,0,1,0,1,0,0],   #   NE, SE, SW
        "4a" : [1,1,1,1,0,0,0,0],   #   N,  NE, E,  SE
        "4r" : [1,1,1,0,1,0,0,0],   #   N,  NE, E,  S
        "4q" : [1,1,1,0,0,1,0,0],   #   N,  NE, E,  SW
        "4i" : [1,1,0,1,1,0,0,0],   #   N,  NE, SE, S
        "4y" : [1,1,0,1,0,1,0,0],   #   N,  NE, SE, SW
        "4k" : [1,1,0,1,0,0,1,0],   #   N,  NE, SE, W
        "4n" : [1,1,0,1,0,0,0,1],   #   N,  NE, SE, NW
        "4z" : [1,1,0,0,1,1,0,0],   #   N,  NE, S,  SW
        "4j" : [1,1,0,0,1,0,1,0],   #   N,  NE, S,  W
        "4t" : [1,1,0,0,1,0,0,1],   #   N,  NE, S,  NW
        "4w" : [1,1,0,0,0,1,1,0],   #   N,  NE, SW, W
        "4e" : [1,0,1,0,1,0,1,0],   #   N,  E,  S,  W
        "4c" : [0,1,0,1,0,1,0,1],   #   NE, SE, SW, NW
        "5i" : [1,1,1,1,1,0,0,0],   #   N,  NE, E,  SE, S
        "5j" : [1,1,1,1,0,1,0,0],   #   N,  NE, E,  SE, SW
        "5n" : [1,1,1,1,0,0,1,0],   #   N,  NE, E,  SE, W
        "5a" : [1,1,1,1,0,0,0,1],   #   N,  NE, E,  SE, NW
        "5q" : [1,1,1,0,1,1,0,0],   #   N,  NE, E,  S,  SW
        "5c" : [1,1,1,0,1,0,1,0],   #   N,  NE, E,  S,  W
        "5r" : [1,1,0,1,1,1,0,0],   #   N,  NE, SE, S,  SW
        "5y" : [1,1,0,1,1,0,1,0],   #   N,  NE, SE, S,  W
        "5k" : [1,1,0,1,0,1,1,0],   #   N,  NE, SE, SW, W
        "5e" : [1,1,0,1,0,1,0,1],   #   N,  NE, SE, SW, NW
        "6a" : [1,1,1,1,1,1,0,0],   #   N,  NE, E,  SE, S,  SW
        "6c" : [1,1,1,1,1,0,1,0],   #   N,  NE, E,  SE, S,  W
        "6k" : [1,1,1,1,0,1,1,0],   #   N,  NE, E,  SE, SW, W
        "6e" : [1,1,1,1,0,1,0,1],   #   N,  NE, E,  SE, SW, NW
        "6n" : [1,1,1,0,1,1,1,0],   #   N,  NE, E,  S,  SW, W
        "6i" : [1,1,0,1,1,1,0,1],   #   N,  NE, SE, S,  SW, NW
        "7c" : [1,1,1,1,1,1,1,0],   #   N,  NE, E,  SE, S,  SW, W
        "7e" : [1,1,1,1,1,1,0,1],   #   N,  NE, E,  SE, S,  SW, NW
        "8"  : [1,1,1,1,1,1,1,1],   #   N,  NE, E,  SE, S,  SW, W,  NW
        }

    notationdict2 = {
        "0"  : "off1,off2,off3,off4,off5,off6,off7,off8",   #    
        "1e" : "on01,off2,off3,off4,off5,off6,off7,off8",   #   N
        "1c" : "off1,on02,off3,off4,off5,off6,off7,off8",   #   NE
        "2a" : "on01,on02,off3,off4,off5,off6,off7,off8",   #   N,  NE
        "2e" : "on01,off2,on03,off4,off5,off6,off7,off8",   #   N,  E
        "2k" : "on01,off2,off3,on04,off5,off6,off7,off8",   #   N,  SE
        "2i" : "on01,off2,off3,off4,on05,off6,off7,off8",   #   N,  S
        "2c" : "off1,on02,off3,on04,off5,off6,off7,off8",   #   NE, SE
        "2n" : "off1,on02,off3,off4,off5,on06,off7,off8",   #   NE, SW
        "3a" : "on01,on02,on03,off4,off5,off6,off7,off8",   #   N,  NE, E
        "3n" : "on01,on02,off3,on04,off5,off6,off7,off8",   #   N,  NE, SE
        "3r" : "on01,on02,off3,off4,on05,off6,off7,off8",   #   N,  NE, S
        "3q" : "on01,on02,off3,off4,off5,on06,off7,off8",   #   N,  NE, SW
        "3j" : "on01,on02,off3,off4,off5,off6,on07,off8",   #   N,  NE, W
        "3i" : "on01,on02,off3,off4,off5,off6,off7,on08",   #   N,  NE, NW
        "3e" : "on01,off2,on03,off4,on05,off6,off7,off8",   #   N,  E,  S
        "3k" : "on01,off2,on03,off4,off5,on06,off7,off8",   #   N,  E,  SW
        "3y" : "on01,off2,off3,on04,off5,on06,off7,off8",   #   N,  SE, SW
        "3c" : "off1,on02,off3,on04,off5,on06,off7,off8",   #   NE, SE, SW
        "4a" : "on01,on02,on03,on04,off5,off6,off7,off8",   #   N,  NE, E,  SE
        "4r" : "on01,on02,on03,off4,on05,off6,off7,off8",   #   N,  NE, E,  S
        "4q" : "on01,on02,on03,off4,off5,on06,off7,off8",   #   N,  NE, E,  SW
        "4i" : "on01,on02,off3,on04,on05,off6,off7,off8",   #   N,  NE, SE, S
        "4y" : "on01,on02,off3,on04,off5,on06,off7,off8",   #   N,  NE, SE, SW
        "4k" : "on01,on02,off3,on04,off5,off6,on07,off8",   #   N,  NE, SE, W
        "4n" : "on01,on02,off3,on04,off5,off6,off7,on08",   #   N,  NE, SE, NW
        "4z" : "on01,on02,off3,off4,on05,on06,off7,off8",   #   N,  NE, S,  SW
        "4j" : "on01,on02,off3,off4,on05,off6,on07,off8",   #   N,  NE, S,  W
        "4t" : "on01,on02,off3,off4,on05,off6,off7,on08",   #   N,  NE, S,  NW
        "4w" : "on01,on02,off3,off4,off5,on06,on07,off8",   #   N,  NE, SW, W
        "4e" : "on01,off2,on03,off4,on05,off6,on07,off8",   #   N,  E,  S,  W
        "4c" : "off1,on02,off3,on04,off5,on06,off7,on08",   #   NE, SE, SW, NW
        "5i" : "on01,on02,on03,on04,on05,off6,off7,off8",   #   N,  NE, E,  SE, S
        "5j" : "on01,on02,on03,on04,off5,on06,off7,off8",   #   N,  NE, E,  SE, SW
        "5n" : "on01,on02,on03,on04,off5,off6,on07,off8",   #   N,  NE, E,  SE, W
        "5a" : "on01,on02,on03,on04,off5,off6,off7,on08",   #   N,  NE, E,  SE, NW
        "5q" : "on01,on02,on03,off4,on05,on06,off7,off8",   #   N,  NE, E,  S,  SW
        "5c" : "on01,on02,on03,off4,on05,off6,on07,off8",   #   N,  NE, E,  S,  W
        "5r" : "on01,on02,off3,on04,on05,on06,off7,off8",   #   N,  NE, SE, S,  SW
        "5y" : "on01,on02,off3,on04,on05,off6,on07,off8",   #   N,  NE, SE, S,  W
        "5k" : "on01,on02,off3,on04,off5,on06,on07,off8",   #   N,  NE, SE, SW, W
        "5e" : "on01,on02,off3,on04,off5,on06,off7,on08",   #   N,  NE, SE, SW, NW
        "6a" : "on01,on02,on03,on04,on05,on06,off7,off8",   #   N,  NE, E,  SE, S,  SW
        "6c" : "on01,on02,on03,on04,on05,off6,on07,off8",   #   N,  NE, E,  SE, S,  W
        "6k" : "on01,on02,on03,on04,off5,on06,on07,off8",   #   N,  NE, E,  SE, SW, W
        "6e" : "on01,on02,on03,on04,off5,on06,off7,on08",   #   N,  NE, E,  SE, SW, NW
        "6n" : "on01,on02,on03,off4,on05,on06,on07,off8",   #   N,  NE, E,  S,  SW, W
        "6i" : "on01,on02,off3,on04,on05,on06,off7,on08",   #   N,  NE, SE, S,  SW, NW
        "7c" : "on01,on02,on03,on04,on05,on06,on07,off8",   #   N,  NE, E,  SE, S,  SW, W
        "7e" : "on01,on02,on03,on04,on05,on06,off7,on08",   #   N,  NE, E,  SE, S,  SW, NW
        "8"  : "on01,on02,on03,on04,on05,on06,on07,on08",   #   N,  NE, E,  SE, S,  SW, W,  NW
        }    
    allneighbours = [  
        ["0"],
        ["1e", "1c"],
        ["2a", "2e", "2k", "2i", "2c", "2n"],
        ["3a", "3n", "3r", "3q", "3j", "3i", "3e", "3k", "3y", "3c"],
        ["4a", "4r", "4q", "4i", "4y", "4k", "4n", "4z", "4j", "4t", "4w", "4e", "4c"],
        ["5i", "5j", "5n", "5a", "5q", "5c", "5r", "5y", "5k", "5e"],
        ["6a", "6c", "6k", "6e", "6n", "6i"],
        ["7c", "7e"],
        ["8"],
        ]
        
    allneighbours_flat = [n for x in allneighbours for n in x]
    
    numneighbours = len(notationdict)
    
    # Use dict to store rule elements, initialised by setrule():
    bee = {}
    ess = {}
    alphanumeric = ""
    rulename = ""
    
    # Save the isotropic rule
    def saveAllRules(self):    
        self.saveIsotropicRule()
    
    # Interpret birth or survival string
    def ruleparts(self, part):

        inverse = False
        nlist = []
        totalistic = True
        rule = { k: False for k, v in self.notationdict.iteritems() }
        
        # Reverse the rule string to simplify processing
        part = part[::-1]
        
        for c in part:
            if c.isdigit():
                d = int(c)
                if totalistic:
                    # Add all the neighbourhoods for this value
                    for neighbour in self.allneighbours[d]:
                        rule[neighbour] = True
                elif inverse:
                    # Add all the neighbourhoods not in nlist for this value
                    for neighbour in self.allneighbours[d]:
                        if neighbour[1] not in nlist:
                            rule[neighbour] = True
                else:
                    # Add all the neighbourhoods in nlist for this value
                    for n in nlist:
                        neighbour = c + n
                        if neighbour in rule:
                            rule[neighbour] = True
                        else:
                            # Error
                            return {}
                    
                inverse = False
                nlist = []
                totalistic = True

            elif (c == '-'):
                inverse = True

            else:
                totalistic = False
                nlist.append(c)
        
        return rule

    # Set isotropic, non-totalistic rule
    # Adapted from Eric Goldstein's HenselNotation->Ruletable(1.3).py
    def setrule(self, rulestring):
    
        # neighbours_flat = [n for x in neighbours for n in x]
        b = {}
        s = {}
        sep = ''
        birth = ''
        survive = ''
        
        rulestring = rulestring.lower()
        
        if '/' in rulestring:
            sep = '/'
        elif '_' in rulestring:
            sep = '_'
        elif (rulestring[0] == 'b'):
            sep = 's'
        else:
            sep = 'b'
        
        survive, birth = rulestring.split(sep)
        if (survive[0] == 'b'):
            survive, birth = birth, survive
        survive = survive.replace('s', '')
        birth = birth.replace('b', '')
        
        b = self.ruleparts(birth)
        s = self.ruleparts(survive)

        if b and s:
            self.alphanumeric = 'B' + birth + 'S' + survive
            self.rulename = 'B' + birth + '_S' + survive + "History"
            self.bee = b
            self.ess = s
        else:
            # Error
            g.note("Unable to process rule definition.\n" +
                    "b = " + str(b) + "\ns = " + str(s))
            g.exit()
            

    # Save a rule file:
    def saverule(self, name, comments, table, colours, icons):
        
        ruledir = g.getdir("rules")
        filename = ruledir + name + ".rule"

        results = "@RULE " + name + "\n\n"
        results += "*** File autogenerated by saverule. ***\n\n"
        results += comments
        results += "\n\n@TABLE\n\n"
        results += table
        results += "\n\n@COLORS\n\n"
        results += colours
        results += "\n\n@ICONS\n\n"
        results += icons

        # Change in behavior:  always create rule table,
        #   silently overwriting any file with the same name
        try:
            f = open(filename, 'w')
            f.write(results)
            f.close()
        except:
            g.warn("Unable to create rule table:\n" + filename)

    # Defines a variable:
    def newvar(self, name, vallist):

        line = "var "+name+"={"
        for i in xrange(len(vallist)):
            if (i > 0):
                line += ','
            line += str(vallist[i])
        line += "}\n"

        return line

    # Defines a block of equivalent variables:
    def newvars(self, namelist, vallist):

        block = "\n"

        for name in namelist:
            block += self.newvar(name, vallist)

        return block

    def scoline(self, chara, charb, left, right, amount):

        line = str(left) + ","

        for i in xrange(8):
            if (i < amount):
                line += chara
            else:
                line += charb
            line += chr(97 + i)
            line += ","

        line += str(right) + "\n"

        return line

    def isotropicline(self, chara, charb, left, right, n):

        line = str(left) + ","
        neighbours = self.notationdict[n]
        
        for i in xrange(8):
            if neighbours[i]:
                line += chara
            else:
                line += charb
            line += chr(97 + i)
            line += ","

        line += str(right) + "\n"

        return line
        
    def saveIsotropicRule(self):
    
        comments = """
This is a two state, isotropic, non-totalistic rule on the Moore neighbourhood.
The notation used to define the rule was originally proposed by Alan Hensel.
See http://www.ibiblio.org/lifepatterns/neighbors2.html for details
"""

        table = """
n_states:7
neighborhood:Moore
symmetries:rotate4reflect
"""
        # a through h become "any"
        # i,j,k,m,n,p,q,r become "off"
        # new "on" options needed, up to 8 of them (for b8 rules)
        table += self.newvars(["any1","any2","any3","any4","any5","any6","any7","any8"], [0, 1, 2, 3, 4, 5, 6])
        table += self.newvars(["off","off1","off2","off3","off4","off5","off6","off7","off8","off9"], [0, 2, 4, 6])
        table += self.newvars(["on","on01","on02","on03","on04","on05","on06","on07","on08"], [1, 3, 5])
        table += self.newvars(["markedon"],[3, 5])
        
        table += "\n# boundary cell always stays a boundary cell\n"
        table += "6,any1,any2,any3,any4,any5,any6,any7,any8,6\n"

        table += "\n# anything else that touches a boundary cell dies\n"	
        table += "markedon,6,any1,any2,any3,any4,any5,any6,any7,4\n"
	table += "on,6,any1,any2,any3,any4,any5,any6,any7,2\n"
	table += "on,any1,6,any2,any3,any4,any5,any6,any7,2\n"

        table += "\n# Marked birth\n"
        for n in self.allneighbours_flat:
            if self.bee[n]:
                table += "4,"
                table += self.notationdict2[n]
                table += ",3\n"
        
        table += "\n# Marked survival state 3\n"
        for n in self.allneighbours_flat:
            if self.ess[n]:
                table += "3,"
                table += self.notationdict2[n]
                table += ",3\n"

        table += "\n# Marked survival state 5\n"
        for n in self.allneighbours_flat:
            if self.ess[n]:
                table += "5,"
                table += self.notationdict2[n]
                table += ",5\n"
	
        table += "\n# Birth\n"
        for n in self.allneighbours_flat:
            if self.bee[n]:
                table += "off,"
                table += self.notationdict2[n]
                table += ",1\n"
        
        table += "\n# Survival\n"
        for n in self.allneighbours_flat:
            if self.ess[n]:
                table += "1,"
                table += self.notationdict2[n]
                table += ",1\n"

        table += "\n# Death for marked cells\n"
        table += "markedon,any1,any2,any3,any4,any5,any6,any7,any8,4"

        table += "\n# Death for unmarked cells\n"
        table += "1,any1,any2,any3,any4,any5,any6,any7,any8,2"
        
        colours = """1    0  255    0
2    0    0  128
3  216  255  216
4  255    0    0
5  255  255    0
6   96   96   96
"""
        icons = """XPM
/* width height num_colors chars_per_pixel */
"31 186 5 1"
/* colors */
". c #000000"
"B c #404040"
"C c #808080"
"D c #C0C0C0"
"E c #FFFFFF"
/* icon for state 1 */
"..............................."
"..............................."
"..........BCDEEEEEDCB.........."
".........CEEEEEEEEEEEC........."
".......BEEEEEEEEEEEEEEEB......."
"......DEEEEEEEEEEEEEEEEED......"
".....DEEEEEEEEEEEEEEEEEEED....."
"....BEEEEEEEEEEEEEEEEEEEEEB...."
"....EEEEEEEEEEEEEEEEEEEEEEE...."
"...CEEEEEEEEEEEEEEEEEEEEEEEC..."
"..BEEEEEEEEEEEEEEEEEEEEEEEEEB.."
"..CEEEEEEEEEEEEEEEEEEEEEEEEEC.."
"..DEEEEEEEEEEEEEEEEEEEEEEEEED.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..DEEEEEEEEEEEEEEEEEEEEEEEEED.."
"..CEEEEEEEEEEEEEEEEEEEEEEEEEC.."
"..BEEEEEEEEEEEEEEEEEEEEEEEEEB.."
"...CEEEEEEEEEEEEEEEEEEEEEEEC..."
"....EEEEEEEEEEEEEEEEEEEEEEE...."
"....BEEEEEEEEEEEEEEEEEEEEEB...."
".....DEEEEEEEEEEEEEEEEEEED....."
"......DEEEEEEEEEEEEEEEEED......"
".......BEEEEEEEEEEEEEEEB......."
".........CEEEEEEEEEEEC........."
"..........BCDEEEEEDCB.........."
"..............................."
"..............................."
/* icon for state 2 */
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
/* icon for state 3 */
"..............................."
"..............................."
"..........BCDEEEEEDCB.........."
".........CEEEEEEEEEEEC........."
".......BEEEEEEEEEEEEEEEB......."
"......DEEEEEEEEEEEEEEEEED......"
".....DEEEEEEEEEEEEEEEEEEED....."
"....BEEEEEEEEEEEEEEEEEEEEEB...."
"....EEEEEEEEEEEEEEEEEEEEEEE...."
"...CEEEEEEEEEEEEEEEEEEEEEEEC..."
"..BEEEEEEEEEEEEEEEEEEEEEEEEEB.."
"..CEEEEEEEEEEEEEEEEEEEEEEEEEC.."
"..DEEEEEEEEEEEEEEEEEEEEEEEEED.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..DEEEEEEEEEEEEEEEEEEEEEEEEED.."
"..CEEEEEEEEEEEEEEEEEEEEEEEEEC.."
"..BEEEEEEEEEEEEEEEEEEEEEEEEEB.."
"...CEEEEEEEEEEEEEEEEEEEEEEEC..."
"....EEEEEEEEEEEEEEEEEEEEEEE...."
"....BEEEEEEEEEEEEEEEEEEEEEB...."
".....DEEEEEEEEEEEEEEEEEEED....."
"......DEEEEEEEEEEEEEEEEED......"
".......BEEEEEEEEEEEEEEEB......."
".........CEEEEEEEEEEEC........."
"..........BCDEEEEEDCB.........."
"..............................."
"..............................."
/* icon for state 4 */
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
/* icon for state 5 */
"..............................."
"..............................."
"..........BCDEEEEEDCB.........."
".........CEEEEEEEEEEEC........."
".......BEEEEEEEEEEEEEEEB......."
"......DEEEEEEEEEEEEEEEEED......"
".....DEEEEEEEEEEEEEEEEEEED....."
"....BEEEEEEEEEEEEEEEEEEEEEB...."
"....EEEEEEEEEEEEEEEEEEEEEEE...."
"...CEEEEEEEEEEEEEEEEEEEEEEEC..."
"..BEEEEEEEEEEEEEEEEEEEEEEEEEB.."
"..CEEEEEEEEEEEEEEEEEEEEEEEEEC.."
"..DEEEEEEEEEEEEEEEEEEEEEEEEED.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..EEEEEEEEEEEEEEEEEEEEEEEEEEE.."
"..DEEEEEEEEEEEEEEEEEEEEEEEEED.."
"..CEEEEEEEEEEEEEEEEEEEEEEEEEC.."
"..BEEEEEEEEEEEEEEEEEEEEEEEEEB.."
"...CEEEEEEEEEEEEEEEEEEEEEEEC..."
"....EEEEEEEEEEEEEEEEEEEEEEE...."
"....BEEEEEEEEEEEEEEEEEEEEEB...."
".....DEEEEEEEEEEEEEEEEEEED....."
"......DEEEEEEEEEEEEEEEEED......"
".......BEEEEEEEEEEEEEEEB......."
".........CEEEEEEEEEEEC........."
"..........BCDEEEEEDCB.........."
"..............................."
"..............................."
/* icon for state 6 */
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E.E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E.E.E.E.E.E.E.E.E."

XPM
/* width height num_colors chars_per_pixel */
"15 90 5 1"
/* colors */
". c #000000"
"B c #404040"
"C c #808080"
"D c #C0C0C0"
"E c #FFFFFF"
/* icon for state 1 */
"..............."
"....BDEEEDB...."
"...DEEEEEEED..."
"..DEEEEEEEEED.."
".BEEEEEEEEEEEB."
".DEEEEEEEEEEED."
".EEEEEEEEEEEEE."
".EEEEEEEEEEEEE."
".EEEEEEEEEEEEE."
".DEEEEEEEEEEED."
".BEEEEEEEEEEEB."
"..DEEEEEEEEED.."
"...DEEEEEEED..."
"....BDEEEDB...."
"..............."
/* icon for state 2 */
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
/* icon for state 3 */
"..............."
"....BDEEEDB...."
"...DEEEEEEED..."
"..DEEEEEEEEED.."
".BEEEEEEEEEEEB."
".DEEEEEEEEEEED."
".EEEEEEEEEEEEE."
".EEEEEEEEEEEEE."
".EEEEEEEEEEEEE."
".DEEEEEEEEEEED."
".BEEEEEEEEEEEB."
"..DEEEEEEEEED.."
"...DEEEEEEED..."
"....BDEEEDB...."
"..............."
/* icon for state 4 */
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
/* icon for state 5 */
"..............."
"....BDEEEDB...."
"...DEEEEEEED..."
"..DEEEEEEEEED.."
".BEEEEEEEEEEEB."
".DEEEEEEEEEEED."
".EEEEEEEEEEEEE."
".EEEEEEEEEEEEE."
".EEEEEEEEEEEEE."
".DEEEEEEEEEEED."
".BEEEEEEEEEEEB."
"..DEEEEEEEEED.."
"...DEEEEEEED..."
"....BDEEEDB...."
"..............."
/* icon for state 6 */
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"
".E.E.E.E.E.E.E."
"E.E.E.E.E.E.E.E"

XPM
/* width height num_colors chars_per_pixel */
"7 42 6 1"
/* colors */
". c #000000"
"B c #404040"
"C c #808080"
"D c #C0C0C0"
"E c #FFFFFF"
"F c #E0E0E0"
/* icon for state 1 */
".BFEFB."
"BEEEEEB"
"FEEEEEF"
"EEEEEEE"
"FEEEEEF"
"BEEEEEB"
".BFEFB."
/* icon for state 2 */
".E.E.E."
"E.E.E.E"
".E.E.E."
"E.E.E.E"
".E.E.E."
"E.E.E.E"
".E.E.E."
/* icon for state 3 */
".BFEFB."
"BEEEEEB"
"FEEEEEF"
"EEEEEEE"
"FEEEEEF"
"BEEEEEB"
".BFEFB."
/* icon for state 4 */
"E.E.E.E"
".E.E.E."
"E.E.E.E"
".E.E.E."
"E.E.E.E"
".E.E.E."
"E.E.E.E"
/* icon for state 5 */
".BFEFB."
"BEEEEEB"
"FEEEEEF"
"EEEEEEE"
"FEEEEEF"
"BEEEEEB"
".BFEFB."
/* icon for state 6 */
"E.E.E.E"
".E.E.E."
"E.E.E.E"
".E.E.E."
"E.E.E.E"
".E.E.E."
"E.E.E.E"
"""
        self.saverule(self.rulename, comments, table, colours, icons)

rulestring = g.getstring("To make a marked History rule, enter rule string in Alan Hensel's isotropic rule notation", 
                         "B2-a/S12")

rg = RuleGenerator()

rg.setrule(rulestring)
rg.saveIsotropicRule()
g.setrule(rg.rulename)

g.show("Created rule in file: " + rg.rulename + ".rule")