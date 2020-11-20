# isotropic-history-rule-gen.py, version 1.0
#   Minimal changes made to isotropic-rule-gen.py version 1.1
#     ( https://github.com/dvgrn/b3s23life/blob/master/rule-table-makers/isotropic-rule-gen.py )
#     to produce an equivalent three-state rule with state-2 History cells
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
        "0"  : "i,j,k,m,n,p,q,r",   #    
        "1e" : "1,j,k,m,n,p,q,r",   #   N
        "1c" : "i,1,k,m,n,p,q,r",   #   NE
        "2a" : "1,1,k,m,n,p,q,r",   #   N,  NE
        "2e" : "1,j,1,m,n,p,q,r",   #   N,  E
        "2k" : "1,j,k,1,n,p,q,r",   #   N,  SE
        "2i" : "1,j,k,m,1,p,q,r",   #   N,  S
        "2c" : "i,1,k,1,n,p,q,r",   #   NE, SE
        "2n" : "i,1,k,m,n,1,q,r",   #   NE, SW
        "3a" : "1,1,1,m,n,p,q,r",   #   N,  NE, E
        "3n" : "1,1,k,1,n,p,q,r",   #   N,  NE, SE
        "3r" : "1,1,k,m,1,p,q,r",   #   N,  NE, S
        "3q" : "1,1,k,m,n,1,q,r",   #   N,  NE, SW
        "3j" : "1,1,k,m,n,p,1,r",   #   N,  NE, W
        "3i" : "1,1,k,m,n,p,q,1",   #   N,  NE, NW
        "3e" : "1,j,1,m,1,p,q,r",   #   N,  E,  S
        "3k" : "1,j,1,m,n,1,q,r",   #   N,  E,  SW
        "3y" : "1,j,k,1,n,1,q,r",   #   N,  SE, SW
        "3c" : "i,1,k,1,n,1,q,r",   #   NE, SE, SW
        "4a" : "1,1,1,1,n,p,q,r",   #   N,  NE, E,  SE
        "4r" : "1,1,1,m,1,p,q,r",   #   N,  NE, E,  S
        "4q" : "1,1,1,m,n,1,q,r",   #   N,  NE, E,  SW
        "4i" : "1,1,k,1,1,p,q,r",   #   N,  NE, SE, S
        "4y" : "1,1,k,1,n,1,q,r",   #   N,  NE, SE, SW
        "4k" : "1,1,k,1,n,p,1,r",   #   N,  NE, SE, W
        "4n" : "1,1,k,1,n,p,q,1",   #   N,  NE, SE, NW
        "4z" : "1,1,k,m,1,1,q,r",   #   N,  NE, S,  SW
        "4j" : "1,1,k,m,1,p,1,r",   #   N,  NE, S,  W
        "4t" : "1,1,k,m,1,p,q,1",   #   N,  NE, S,  NW
        "4w" : "1,1,k,m,n,1,1,r",   #   N,  NE, SW, W
        "4e" : "1,j,1,m,1,p,1,r",   #   N,  E,  S,  W
        "4c" : "i,1,k,1,n,1,q,1",   #   NE, SE, SW, NW
        "5i" : "1,1,1,1,1,p,q,r",   #   N,  NE, E,  SE, S
        "5j" : "1,1,1,1,n,1,q,r",   #   N,  NE, E,  SE, SW
        "5n" : "1,1,1,1,n,p,1,r",   #   N,  NE, E,  SE, W
        "5a" : "1,1,1,1,n,p,q,1",   #   N,  NE, E,  SE, NW
        "5q" : "1,1,1,m,1,1,q,r",   #   N,  NE, E,  S,  SW
        "5c" : "1,1,1,m,1,p,1,r",   #   N,  NE, E,  S,  W
        "5r" : "1,1,k,1,1,1,q,r",   #   N,  NE, SE, S,  SW
        "5y" : "1,1,k,1,1,p,1,r",   #   N,  NE, SE, S,  W
        "5k" : "1,1,k,1,n,1,1,r",   #   N,  NE, SE, SW, W
        "5e" : "1,1,k,1,n,1,q,1",   #   N,  NE, SE, SW, NW
        "6a" : "1,1,1,1,1,1,q,r",   #   N,  NE, E,  SE, S,  SW
        "6c" : "1,1,1,1,1,p,1,r",   #   N,  NE, E,  SE, S,  W
        "6k" : "1,1,1,1,n,1,1,r",   #   N,  NE, E,  SE, SW, W
        "6e" : "1,1,1,1,n,1,q,1",   #   N,  NE, E,  SE, SW, NW
        "6n" : "1,1,1,m,1,1,1,r",   #   N,  NE, E,  S,  SW, W
        "6i" : "1,1,k,1,1,1,q,1",   #   N,  NE, SE, S,  SW, NW
        "7c" : "1,1,1,1,1,1,1,r",   #   N,  NE, E,  SE, S,  SW, W
        "7e" : "1,1,1,1,1,1,q,1",   #   N,  NE, E,  SE, S,  SW, NW
        "8"  : "1,1,1,1,1,1,1,1",   #   N,  NE, E,  SE, S,  SW, W,  NW
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
    def saverule(self, name, comments, table, colours):
        
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
        results += "circles\n"

        # Only create a rule file if it doesn't already exist; this avoids
        # concurrency issues when booting an instance of apgsearch whilst
        # one is already running.
        if not os.path.exists(filename):
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
n_states:3
neighborhood:Moore
symmetries:rotate4reflect
"""

        table += self.newvars(["a","b","c","d","e","f","g","h"], [0, 1, 2])
        table += self.newvars(["off","i","j","k","l","m","n","p","q","r"], [0, 2])
        
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

        table += "\n# Death\n"
        table += self.scoline("","",1,2,0)
        
        colours = ""
        self.saverule(self.rulename, comments, table, colours)

rulestring = g.getstring("To make a History rule, enter rule string in Alan Hensel's isotropic rule notation", 
                         "B2-a/S12")

rg = RuleGenerator()

rg.setrule(rulestring)
rg.saveIsotropicRule()
g.setrule(rg.rulename)

g.show("Created rule in file: " + rg.rulename + ".rule")