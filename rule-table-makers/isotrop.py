# HenselNotation->Ruletable(1.3).py
#  by Eric Goldstein, July 20, 2012.
# a.k.a. isotrop.py

import golly

dialog_box_message =  '''This script will allow you to enter the non-totalistic rule notation 
used by Johan Bontes' Life32 program, based on work by Alan Hensel.
Please look in the script file to see how the notation works.
Newly created rules will be placed in Golly's Rules directory (set in Golly"s preferences). 

Note:  Alan Hensel's notation for r and y are swapped in Life32.   Life32's rule dialog box
shows the correct arrangements, but they are swapped in the implementation.
What should work as 3r, 4r, and 5r, actually work as 3y, 4y, and 5y, and vice versa.
This script swaps the definition of r and y just like Life32 does, so that rules will
run the same way using either Golly or Life32.

An example rule is given below as a default.  Rules are case-insensitive.
B2a/S12, S12/B2a, and 12/2a are valid and equivalent.  

Inverse specifications are allowed.  For example, David Bell's Just Friends rule can be 
expressed B2-a/S12 indicating that all B2 arrangements are included except 2a.


There are two ways to use this script.  Both ways will create a new ruletable, and 
set the active layer of Golly to use the new rule. 
1) You can enter a rule below.
2) You can copy the contents of a life32 file starting with "#r" and then click
on this script, after which you'll be able to paste the pattern into Golly's active layer.

Enter a rule here:
   '''



# Golly"s ruletable format use the following notation:  
#  C,N,NE,E,SE,S,SW,W,NW,C' 
# where C is the current state, and C' is the new state, and
# where the eight neighbors in the Moore neighborhood are as shown below.

#     NW  N  NE 
#     W   C  E  
#     SW  S  SE 

# The lookup table below for Life32"s non-totalistic notation uses the eight neighbor values:
#   N,NE,E,SE,S,SW,W,NW

# The following code shows how the non-totalistic notation works:

notationdict = {  
                 "1e" : "1,0,0,0,0,0,0,0",  #   N 
                 "1c" : "0,1,0,0,0,0,0,0",  #   NE
                 "2a" : "1,1,0,0,0,0,0,0",  #   N,  NE
                 "2e" : "1,0,1,0,0,0,0,0",  #   N,  E 
                 "2k" : "1,0,0,1,0,0,0,0",  #   N,  SE
                 "2i" : "1,0,0,0,1,0,0,0",  #   N,  S 
                 "2c" : "0,1,0,1,0,0,0,0",  #   NE, SE
                 "2v" : "0,1,0,0,0,1,0,0",  #   NE, SW
                 "3a" : "1,1,1,0,0,0,0,0",  #   N,  NE, E
                 "3v" : "1,1,0,1,0,0,0,0",  #   N,  NE, SE 
                 "3y" : "1,1,0,0,1,0,0,0",  #   N,  NE, S      (3r in non-swapped notation)
                 "3q" : "1,1,0,0,0,1,0,0",  #   N,  NE, SW
                 "3j" : "1,1,0,0,0,0,1,0",  #   N,  NE, W
                 "3i" : "1,1,0,0,0,0,0,1",  #   N,  NE, NW
                 "3e" : "1,0,1,0,1,0,0,0",  #   N,  E,  S
                 "3k" : "1,0,1,0,0,1,0,0",  #   N,  E,  SW
                 "3r" : "1,0,0,1,0,1,0,0",  #   N,  SE, SW     (3y in non-swapped notation)
                 "3c" : "0,1,0,1,0,1,0,0",  #   NE, SE, SW 
                 "4a" : "1,1,1,1,0,0,0,0",  #   N,  NE, E,  SE
                 "4y" : "1,1,1,0,1,0,0,0",  #   N,  NE, E,  S  (4r in non-swapped notation)
                 "4q" : "1,1,1,0,0,1,0,0",  #   N,  NE, E,  SW
                 "4i" : "1,1,0,1,1,0,0,0",  #   N,  NE, SE, S
                 "4r" : "1,1,0,1,0,1,0,0",  #   N,  NE, SE, SW (4y in non-swapped notation)
                 "4k" : "1,1,0,1,0,0,1,0",  #   N,  NE, SE, W
                 "4v" : "1,1,0,1,0,0,0,1",  #   N,  NE, SE, NW 
                 "4z" : "1,1,0,0,1,1,0,0",  #   N,  NE, S,  SW
                 "4j" : "1,1,0,0,1,0,1,0",  #   N,  NE, S,  W
                 "4t" : "1,1,0,0,1,0,0,1",  #   N,  NE, S,  NW
                 "4w" : "1,1,0,0,0,1,1,0",  #   N,  NE, SW, W
                 "4e" : "1,0,1,0,1,0,1,0",  #   N,  E,  S,  W
                 "4c" : "0,1,0,1,0,1,0,1",  #   NE, SE, SW, NW
                 "5a" : "0,0,0,1,1,1,1,1",  #   SE, S,  SW, W,  NW
                 "5v" : "0,0,1,0,1,1,1,1",  #   E,  S,  SW, W,  NW
                 "5y" : "0,0,1,1,0,1,1,1",  #   E,  SE, SW, W,  NW (5r in non-swapped notation)
                 "5q" : "0,0,1,1,1,0,1,1",  #   E,  SE, S,  W,  NW
                 "5j" : "0,0,1,1,1,1,0,1",  #   E,  SE, S,  SW, NW 
                 "5i" : "0,0,1,1,1,1,1,0",  #   E,  SE, S,  SW, W 
                 "5e" : "0,1,0,1,0,1,1,1",  #   NE, SE, SW, W,  NW, 
                 "5k" : "0,1,0,1,1,0,1,1",  #   NE, SE, S,  W,  NW
                 "5r" : "0,1,1,0,1,0,1,1",  #   NE, E,  S,  W, NW  (5y in non-swapped notation)
                 "5c" : "1,0,1,0,1,0,1,1",  #   N,  E,  S,  W,  NW
                 "6a" : "0,0,1,1,1,1,1,1",  #   E,  SE, S,  SW, W,  NW
                 "6e" : "0,1,0,1,1,1,1,1",  #   NE, SE, S,  SW, W,  NW
                 "6k" : "0,1,1,0,1,1,1,1",  #   NE, E,  S,  SW, W,  NW
                 "6i" : "0,1,1,1,0,1,1,1",  #   NE, E,  SE, SW, W,  NW
                 "6c" : "1,0,1,0,1,1,1,1",  #   N,  E,  S,  SW, W,  NW
                 "6v" : "1,0,1,1,1,0,1,1",  #   N,  E,  SE, S,  W,  NW
                 "7e" : "0,1,1,1,1,1,1,1",  #   NE, E,  SE, S,  SW, W,  NW 
                 "7c" : "1,0,1,1,1,1,1,1"   #   N,  E,  SE, S,  SW, W,  NW
                }


#  Here's a graphical depiction of the notation.
dummyvariable = '''
x = 147, y = 97, rule = B/S012345678
21b3o6b5o5bo3bo6b3o6b5o5bo3bo5bo3bo6b3o10bo5b4o6b5o5bobobo5b5o$20bo3bo
5bo9bo2bo6bo3bo7bo7bo3bo5bo3bo5bo3bo9bo5bo3bo7bo7bobobo9bo$20bo9bo9bob
o7bo3bo7bo7bo3bo5bo3bo5bo3bo9bo5bo3bo7bo7bobobo8bo$20bo9b3o7b2o8b5o7bo
7bo3bo6bobo6bo3bo9bo5b4o8bo7bobobo7bo$20bo9bo9bobo7bo3bo7bo7bo3bo7bo7b
obobo5bo3bo5bo3bo7bo7bobobo6bo$20bo3bo5bo9bo2bo6bo3bo7bo8bobo8bo7bo2bo
6bo3bo5bo3bo7bo7bobobo5bo$21b3o6b5o5bo3bo5bo3bo5b5o7bo9bo8b2obo6b3o6bo
3bo7bo8bobo6b5o4$b3o6b7o$o3bo5bo5bo$o2b2o5bo5bo$obobo5bo2bo2bo$2o2bo5b
o5bo$o3bo5bo5bo$b3o6b7o4$b2o17b7o3b7o$obo17bo5bo3bo5bo$2bo17bobo3bo3bo
2bo2bo$2bo17bo2bo2bo3bo2bo2bo$2bo17bo5bo3bo5bo$2bo17bo5bo3bo5bo$5o15b
7o3b7o4$b3o16b7o3b7o3b7o3b7o3b7o3b7o$o3bo15bo5bo3bo5bo3bo5bo3bo5bo3bo
5bo3bo5bo$4bo15bobobobo3bo2bo2bo3bobo3bo3bobo3bo3bo2bo2bo3bo3bobo$3bo
16bo2bo2bo3bob2o2bo3bo2bo2bo3bob2o2bo3bo2bo2bo3bo2bo2bo$2bo17bo5bo3bo
5bo3bo2bo2bo3bo5bo3bo2bo2bo3bobo3bo$bo18bo5bo3bo5bo3bo5bo3bo5bo3bo5bo
3bo5bo$5o15b7o3b7o3b7o3b7o3b7o3b7o4$b3o16b7o3b7o3b7o3b7o3b7o3b7o3b7o3b
7o3b7o3b7o$o3bo15bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo
3bo5bo$4bo15bobobobo3bo2bo2bo3bobo3bo3bob2o2bo3bo3bobo3bobobobo3bo2b2o
bo3bo3bobo3bo3bobo3bobobobo$2b2o16bo2bo2bo3bob2o2bo3bo2b2obo3bob2o2bo
3bo2b2obo3bob2o2bo3bo2bo2bo3bo2bo2bo3bo2b2obo3bo2bo2bo$4bo15bobo3bo3bo
2bo2bo3bo2bo2bo3bo5bo3bo3bobo3bo5bo3bo2bo2bo3bob2o2bo3bo2bo2bo3bo2bo2b
o$o3bo15bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo$b
3o16b7o3b7o3b7o3b7o3b7o3b7o3b7o3b7o3b7o3b7o4$2b2o16b7o3b7o3b7o3b7o3b7o
3b7o3b7o3b7o3b7o3b7o3b7o3b7o3b7o$bobo16bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3b
o5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo$o2bo16bobobobo3bo2bo2bo
3bo2b2obo3bob3obo3bob2o2bo3bobobobo3bob2o2bo3bob2o2bo3bo3bobo3bobobobo
3bob3obo3bobo3bo3bob2o2bo$5o15bo2bo2bo3bob3obo3bob2o2bo3bob2o2bo3bo2bo
2bo3bob2o2bo3bob2o2bo3bob2o2bo3bob3obo3bo2bo2bo3bo2bo2bo3bob2o2bo3bo2b
o2bo$3bo16bobobobo3bo2bo2bo3bo3bobo3bo5bo3bob2o2bo3bobo3bo3bo2bo2bo3bo
3bobo3bo2bo2bo3bob2o2bo3bo2bo2bo3bo2b2obo3bo2b2obo$3bo16bo5bo3bo5bo3bo
5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo$3bo16b
7o3b7o3b7o3b7o3b7o3b7o3b7o3b7o3b7o3b7o3b7o3b7o3b7o4$5o15b7o3b7o3b7o3b
7o3b7o3b7o3b7o3b7o3b7o3b7o$o19bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5b
o3bo5bo3bo5bo3bo5bo$4o16bo2bo2bo3bobobobo3bo2b2obo3bo3bobo3bob2o2bo3bo
bo3bo3bobobobo3bob2o2bo3bob2o2bo3bobobobo$4bo15bob3obo3bo2b2obo3bob2o
2bo3bo2b2obo3bob2o2bo3bob3obo3bob3obo3bob2o2bo3bob2o2bo3bob3obo$4bo15b
o2b2obo3bobobobo3bobobobo3bob3obo3bob2o2bo3bob2o2bo3bobo3bo3bo2b2obo3b
obobobo3bo2bo2bo$o3bo15bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo
3bo5bo3bo5bo$b3o16b7o3b7o3b7o3b7o3b7o3b7o3b7o3b7o3b7o3b7o4$b3o16b7o3b
7o3b7o3b7o3b7o3b7o$o3bo15bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo$o19bo2bo
2bo3bobobobo3bo2b2obo3bo2b2obo3bobobobo3bob2o2bo$4o16bob3obo3bo2b2obo
3bob3obo3bo2b2obo3bob3obo3bob3obo$o3bo15bob3obo3bob3obo3bobobobo3bob3o
bo3bobobobo3bo2b2obo$o3bo15bo5bo3bo5bo3bo5bo3bo5bo3bo5bo3bo5bo$b3o16b
7o3b7o3b7o3b7o3b7o3b7o4$5o15b7o3b7o$4bo15bo5bo3bo5bo$3bo16bo2b2obo3bob
3obo$3bo16bob3obo3bo2b2obo$2bo17bob3obo3bob3obo$2bo17bo5bo3bo5bo$2bo
17b7o3b7o4$b3o6b7o$o3bo5bo5bo$o3bo5bob3obo$b3o6bob3obo$o3bo5bob3obo$o
3bo5bo5bo$b3o6b7o!
'''


# The following function takes a rule element like B2a or B2-a and creates the appropriate ruletable row.
# Parameters:
# bs is a string with one of two values "0," to indicate birth, and "1," to indicates survival.
# totalistic_num is one character string "0" ... "8"
# notation_letter is a one character string indicating Hensel's notation "a", 
# inverse_list is a list of notation letters for inverse notation 

def create_table_row(bs,totalistic_num, notation_letter, inverse_list):
   result = ""
   if totalistic_num == "0":
     result = bs + "0,0,0,0,0,0,0,0" + ",1"+"\n"  
   elif totalistic_num == "8":
     result = bs + "1,1,1,1,1,1,1,1" + ",1" +"\n"  
   elif notation_letter != "none":
      result = bs + notationdict[totalistic_num+notation_letter] + ",1" +"\n"
   elif inverse_list != []:
      for i in notationdict: 
         if not (i[1] in inverse_list) and i.startswith(totalistic_num):
            result = result +  bs + notationdict[i] + ",1" +"\n"
   else: 
      for i in notationdict:
         if i.startswith(totalistic_num):
            result = result +  bs + notationdict[i] + ",1" + "\n"
   return result


CR = chr(13)
LF = chr(10)
pastepattern = "none"

yourclipboard = golly.getclipstr()
yourclipboard = yourclipboard.replace(CR+LF,LF)
yourclipboard = yourclipboard.replace(CR,LF)

if yourclipboard.startswith("#r "):
  rulestring = yourclipboard.split(" ")[1].split("\n")[0]
  pastepattern = yourclipboard.split("#r "+rulestring)[1] 
else:
  rulestring = golly.getstring(dialog_box_message, "B2a/S12") 


# The following code cleans up the rulestring
# so that it makes a valid and somewhat readable file name - eg "B2-a_S12.table"

rulestring = rulestring.replace(" ", "")
rulestring = rulestring.lower()
rulestring = rulestring.replace("b", "B")
rulestring = rulestring.replace("s", "S")

# The variable named rulestring will be parsed.  
# The variable named rule_name will be the name of the new file.
# Valid rules contain a slash character but filenames can not include slashes.

rule_name = rulestring.replace("/", "_")  

# To do:  Allow the user to specify their own name for a rule.

#  The following code cleans up the rule string to 
#  make life easier for the parser.

if rulestring.startswith("B") or rulestring.startswith("S"):
    rulestring = rulestring.replace("/", "")
else:
    rulestring = rulestring.replace("/", "B")

rulestring = rulestring + "\n"  

# Lets make a new file

f = open(golly.getdir("rules")+rule_name+".table", "w")

# Now create the header for the rule table

neighborhood = "Moore"  
# Incorporate Paul Callahan's hexagonal non-totaistic notation next?
f.write("neighborhood:"+neighborhood+"\n")

# The next line is where the magic happens! 
f.write("symmetries:rotate4reflect\n") 


# Lets stick with 2 states for now, but it would be interesting 
# to add generations-style decay states, as MCell's Weighted Life does.

n_states = 2   
f.write("n_states:"+str(n_states)+"\n\n")

f.write("""
var a={0,1}
var b={0,1}
var c={0,1}
var d={0,1}
var e={0,1}
var f={0,1}
var g={0,1}
var h={0,1}

""")

# Now that the header for the rule table has been created, 
# parse the rulestring, and add rows to the ruletable as we go.

# Lets say rule strings contain "rule elements", such as B2i, or B2-a, which are composed of: 
# 1) a birth or survival flag 
# 2) a "totalistic context" consisting of an integer between zero and 8
# 3) a "notation_letter".   
# 4) a flag for "positive" or "inverse" notation

bs = "1,"                        # Use "1," for survival or "0," for birth
totalistic_context = "none"      # "none" will be replaced with "0" through
                                 # "8" by the parser.
last_totalistic_context = "none" # Lets the parser remember the previous  
                                 # integer it encountered.
notation_letter = "none"         # "none","a", "e", "i", etc.
positive_or_inverse = "positive" 
inverse_list = []

for x in rulestring:
  if x == "S" or x == "B" or x.isdigit() or x == "\n":
     last_totalistic_context = totalistic_context   
     totalistic_context = x                         
     if last_totalistic_context != "none"  and notation_letter == "none":
         f.write(create_table_row(bs, last_totalistic_context, "none",[]))             
     if last_totalistic_context != "none" and  positive_or_inverse == "inverse":
         f.write(create_table_row(bs, last_totalistic_context, "none", inverse_list))  
     # Now lets get ready to move on to the next character.
     notation_letter = "none"
     inverse_list = []
     positive_or_inverse = "positive"
     if x == "S" or x == "B":
         totalistic_context = "none"
     if x == "S":
         bs = "1,"
     if x == "B": 
         bs = "0,"
  elif x == "-":
    positive_or_inverse = "inverse"
  elif x in ["c", "a", "e", "k", "i", "v", "j", "y", "q", "r", "w", "t", "z"] and totalistic_context != "none":
     if positive_or_inverse == "positive":
        notation_letter = x
        f.write(create_table_row(bs, totalistic_context, notation_letter, []))    
     else:
        notation_letter = x
        inverse_list.append(x) 


f.write("# Death otherwise"+"\n")
f.write("1,a,b,c,d,e,f,g,h,0"+"\n\n")
f.flush()
f.close()
golly.setalgo("RuleTable")
golly.setrule(rule_name)
if pastepattern != "none":
  golly.setclipstr(pastepattern)
  golly.show("Paste the pattern when you are ready....")
else:
  golly.show("Created "+rule_name+".table in "+golly.getdir("rules"))
