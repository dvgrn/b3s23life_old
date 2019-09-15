# slow-salvo-minimizer.py (was recipe-minimizer-binary-good.py)
# Expects a block in the northwest corner to define the 0 lane.
#   gliders should be moving northwest, pointed at the block.

import golly as g

def getbackground(clist):
   g.setrule("B12345678/S")
   background = g.evolve(clist, 1)
   g.setrule("B3/S23")
   return background

class Glider:
  def __init__(self, rlestr, timeoffset, laneoffset):
    self.dt = timeoffset
    self.dx = laneoffset
    cells = g.parse(rlestr)
    self.clist = g.transform(cells,-cells[0],0)
    self.background = getbackground(self.clist)

def matches(glider, x, y):
  for i in range(0, len(glider.clist), 2):
    if g.getcell(glider.clist[i]+x, glider.clist[i+1]+y) == 0: return 0
  bkg = glider.background
  for i in range(0, len(bkg), 2):
    if g.getcell(bkg[i]+x, bkg[i+1]+y) == 1:  return 0
  return 1

def makerecipe(background, gliderlist):
  g.new("Recipe")
  g.putcells(background)
  offset = max(background[1::2])+4
  for glider, delta in gliderlist:
    clist, lane = glider
    g.putcells(clist, (lane+1)/2+offset, offset)
    offset += delta

g.setalgo("HashLife")

glist = [ Glider("3o$o$bo!",0,0), Glider("bo$2o$obo!",1,-2), \
          Glider("2o$obo$o!",2,-1), Glider("b2o$2o$2bo!",3,-1) ]
gliderE, gliderO = g.transform(glist[0].clist,-glist[0].dx,0), g.transform(glist[1].clist,-glist[1].dx,0)   # glist[0].clist, glist[1].clist

if g.numstates()>2: g.exit("Please use a two-state rule.")

r=g.getrect()
if len(r)==0: g.exit("No pattern found.")

nongliderpat, ngp3, recipelist, recipe, remainder, count = [], [], [], "", g.getcells(r), 0
all = remainder

while len(remainder):
  matchflag = 0
  for index in range(len(glist)):
    glider = glist[index]
    if g.getkey() == "q": g.exit()
    TLx, TLy = remainder[0],remainder[1]
    matchflag = matches(glider, TLx, TLy)
    if matchflag:
      # remove the matched pattern from the universe
      count+=1
      g.putcells(glider.clist, TLx, TLy, 1, 0, 0, 1, "xor")
      g.update()
      g.show("Found glider #" + str(glider.dt) + " at " + str([TLx,TLy]))
      if recipe!="": recipe+=" "
      recipe+="E" if  glider.dt%2==0 else "O"
      lane = (TLx-TLy+glider.dx)*2-1
      recipe+=str(lane)
      recipelist+=[[(gliderE if glider.dt%2==0 else gliderO),lane]]
      nomatch = 0
      break
  if matchflag==0:
    nongliderpat+=[TLx, TLy]
    ngp3 +=[TLx, TLy, 3]
    g.setcell(TLx, TLy, 0)
  remainder = g.getcells(g.getrect())

if len(ngp3)%2 == 0: ngp3+=[0] # mark as three-state pattern

LONG_ENOUGH = 1024*(len(recipelist)+1) # extra time for the unknown non-glider pattern

g.show("Running pattern...")
g.putcells(all)
g.run(LONG_ENOUGH)
output = g.getrect()
if len(output)==0: g.exit("This script wasn't designed to build a big pile of nothing.  Need a hashable output.")
hash = g.hash(output)
g.show("Restoring pattern...")
g.select(output)
g.clear(0)
g.putcells(all)

# g.note(str([len(recipelist),recipelist]))
g.addlayer()

# first find the shortest fixed-width separation between gliders
minsep, sep=3, 256

while 1:
  midpoint = int(minsep + (sep-minsep)/2)
  offset=max(nongliderpat[1::2])+4
  g.show("Regenerating pattern at midpoint = " +str(midpoint) + ", minsep = " + str(minsep) + ", sep = "+ str(sep))
  g.new("Results")
  g.putcells(nongliderpat)
  for clist, lane in recipelist:
    g.putcells(clist, (lane+1)/2+offset, offset)
    offset += midpoint
  g.run(LONG_ENOUGH)
  g.fit()
  g.update()
  output = g.getrect()
  if len(output)==0: g.exit("Weird magic vanish reaction happened.  Need a hashable output.")
  newhash = g.hash(output)
  if newhash == hash:
    # g.show("Hashes matched at midpoint = " +str(midpoint) + ", minsep = " + str(minsep) + ", sep = " + str(sep))
    sep = midpoint
  else:
    # g.show("Hashes did not match at midpoint = " +str(midpoint) + ", minsep = " + str(minsep) + ", sep = "+ str(sep))
    if minsep == midpoint: break  # binary search has found a minimum
    minsep = midpoint
if sep != minsep+1: g.exit("Assertion failed -- sep vs. minsep," + str([sep, minsep]))

# g.note(str(len(recipelist))+" gliders to place.")

deltalist = [sep]*len(recipelist)
# deltalist[0] = max(nongliderpat[1::2])+4
makerecipe(nongliderpat, zip(recipelist, deltalist))
g.run(LONG_ENOUGH)
output = g.getrect()
if len(output)==0: g.exit("This script wasn't designed to build a big pile of nothing.  Need a hashable output.")
hash = g.hash(output)

LONG_ENOUGH = 2**12
while LONG_ENOUGH<len(deltalist)*4*sep+4000: LONG_ENOUGH*=2

ptr=0
while ptr<len(deltalist):
  mindelta, maxdelta = -100, sep
  newlist = deltalist[:]
  while 1:
    midpoint = int(mindelta + (maxdelta-mindelta)/2)
    newlist[ptr] = midpoint
    g.show(str(newlist).replace(" ",""))
    makerecipe(nongliderpat, zip(recipelist, newlist))
    g.run(LONG_ENOUGH)
    output = g.getrect()
    if len(output)==0: g.exit("Need a hashable output.")
    newhash = g.hash(output)
    if hash == newhash:
      if maxdelta == midpoint: break
      maxdelta = midpoint
    else:
      if mindelta == midpoint: break
      mindelta = midpoint
  deltalist[ptr]=mindelta+1  # take the last good one and continue
  makerecipe(nongliderpat, zip(recipelist, deltalist))
  g.fit()
  g.update()
  ptr+=1


g.setclipstr(recipe+"\n\n"+str(deltalist))
g.show("Done.")
