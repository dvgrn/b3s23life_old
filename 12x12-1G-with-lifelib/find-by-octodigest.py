import golly as g
import sys
sys.path.append('/PATH/TO/FOLDER/CONTAINING/LIFELIB/FOLDER/') # e.g., 'C:/repos/", not "C:/repos/lifelib/"
import lifelib

# test pattern is 2b2o$b2obo$ob3o$o2bo$2bo$bo!, one answer is 3o4$12b2o$11b2o$8b2o3bo$7bobo$7b2o! at T=36

fingerprintfile = "/PATH/TO/FOLDER/CONTAINING/TEN/FILES/NAMED/hashseq12x12"

chardict = {}
for i in range(37, 127):
  chardict[i-37] = chr(i)

chardict[92-37] = "!"  # backslash
chardict[39-37] = "#"  # apostrophe
chardict[44-37] = "$"  # comma

sess = lifelib.load_rules("b3s23")
lt = sess.lifetree()
  
# Python function to convert a cell list to RLE
# Author: Nathaniel Johnston (nathaniel@nathanieljohnston.com), June 2009.
#           DMG: Refactored slightly so that the function input is a simple cell list.
#                No error checking added.
#                TBD:  check for multistate rule, show appropriate warning.
#           AJP: Replace g.evolve(clist,0) with Python sort
# --------------------------------------------------------------------
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def giveRLE(clist):
    # clist_chunks = list (chunks (g.evolve(clist,0), 2))
    clist_chunks = list(chunks(clist, 2))
    clist_chunks.sort(key=lambda l:(l[1], l[0]))
    mcc = min(clist_chunks)
    rl_list = [[x[0]-mcc[0],x[1]-mcc[1]] for x in clist_chunks]
    rle_res = ""
    rle_len = 1
    rl_y = rl_list[0][1] - 1
    rl_x = 0
    for rl_i in rl_list:
        if rl_i[1] == rl_y:
            if rl_i[0] == rl_x + 1:
                rle_len += 1
            else:
                if rle_len == 1: rle_strA = ""
                else: rle_strA = str (rle_len)
                if rl_i[0] - rl_x - 1 == 1: rle_strB = ""
                else: rle_strB = str (rl_i[0] - rl_x - 1)
                
                rle_res = rle_res + rle_strA + "o" + rle_strB + "b"
                rle_len = 1
        else:
            if rle_len == 1: rle_strA = ""
            else: rle_strA = str (rle_len)
            if rl_i[1] - rl_y == 1: rle_strB = ""
            else: rle_strB = str (rl_i[1] - rl_y)
            if rl_i[0] == 1: rle_strC = "b"
            elif rl_i[0] == 0: rle_strC = ""
            else: rle_strC = str (rl_i[0]) + "b"
            
            rle_res = rle_res + rle_strA + "o" + rle_strB + "$" + rle_strC
            rle_len = 1
            
        rl_x = rl_i[0]
        rl_y = rl_i[1]
    
    if rle_len == 1: rle_strA = ""
    else: rle_strA = str (rle_len)
    rle_res = rle_res[2:] + rle_strA + "o"
    
    return rle_res+"!"
# --------------------------------------------------------------------

def get10char(hashval):
  s = ""
  numchars = 0
  while numchars<10:
    d = hashval/90
    r = hashval - d*90
    s = chardict[r] + s
    hashval = (hashval - r) / 90
    numchars += 1
  return s

def getoctodigest(rect):
  testpat = lt.pattern(giveRLE(g.getcells(rect)))
  return get10char(testpat.octodigest())

g.fitsel()
r = g.getselrect()
if r == []:
  g.exit("No selection.  Select something to find by fingerprint.")
hstr = getoctodigest(r)

count = 0
ptr = 0
pat = g.getcells(r)
g.addlayer()
g.new("Output")
g.putcells(pat,-32-r[0],-r[1])

for i in range(10):
  g.show("Scanning " + fingerprintfile + "_" + str(i) + ".txt")
  with open(fingerprintfile + "_" + str(i) + ".txt", "r") as f:
    for line in f:
      count += 1
      if hstr in line:
        matchingpat = line[:line.index(" ")]
        g.putcells(g.parse(matchingpat),ptr*32,0)
        ptr+=1
  g.fit()
plural = "" if ptr==1 else "s"
g.show("Found " + str(ptr) + " line" + plural + " matching '" + hstr + "' in " + str(count) + " lines of " + fingerprintfile + ".")
