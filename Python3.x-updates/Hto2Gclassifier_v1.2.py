# Hto2Gclassifier_v1.2.py
# -- given any two selected gliders,
#    display the class of Herschel-to-2-glider converter
#    that produces those two synchronized gliders,
#    with the help of some number of Snark reflectors
# v1.2: Updated to work with Python 3.x, 20 October 2020

import golly as g

equivdict={"NW":[0,0,0],"NE":[2,0,1],"SE":[0,1,1],"SW":[2,1,0]}
gliders=["NW0:3o$o$bo!","NW1:bo$2o$obo!","NW2:2o$obo$o!","NW3:b2o$2o$2bo!",
         "NE0:b2o$obo$2bo!","NE1:2o$b2o$o!","NE2:3o$2bo$bo!","NE3:bo$b2o$obo!",
         "SE0:bo$2bo$3o!","SE1:obo$b2o$bo!","SE2:2bo$obo$b2o!","SE3:o$b2o$2o!",
         "SW0:o$obo$2o!","SW1:2bo$2o$b2o!","SW2:bo$o$3o!","SW3:obo$2o$bo!"]
gdict={}
for item in gliders:
  name,rle = item.split(":")
  gdict[name]=g.parse(rle)

def findglider(clist):
  canonical = g.transform(clist,-clist[0],-clist[1])
  canoncoords = list(zip(canonical[0::2],canonical[1::2]))
  for key in gdict:
    glist = g.transform(gdict[key],-gdict[key][0],-gdict[key][1])
    gcoords = list(zip(glist[0::2],glist[1::2]))
    match=1
    for coord in gcoords:
      if coord not in canoncoords:
        match=0
        break
    if match==1:
      for coord in gcoords:  # remove the matching glider
        canoncoords.remove(coord)
      # return UL bounding box corner of matching glider
      x, y = min(glist[0::2])+clist[0],min(glist[1::2])+clist[1]
      dir,phase = key[:2],int(key[2])
      outlist=[]
      for a,b in canoncoords: outlist+=[a,b]
      return [dir,phase,x,y],g.transform(outlist,clist[0],clist[1])

def findgliders(clist):
  # check the top left cell in clist against the first cell in each gdict[key]
  stats1,remainder=findglider(clist)
  stats2,empty=findglider(remainder)
  if empty!=[]: g.exit("Could not recognize gliders in selection.")
  return stats1, stats2

# find an {outdir}-traveling glider equivalent to one with the statistics in statlist
def findcanonical(statslist,outdir):
  dir,phase,x,y = statslist
  dphase, dx, dy = equivdict[dir]
  dphaseout, dxout, dyout = equivdict[outdir]
  # this is really all two-state arithmetic, so + vs. - below doesn't actually matter
  return [outdir, (phase+dphase-dphaseout)%4, x+dx-dxout, y+dy-dyout]
  
if g.numstates()!=2: g.exit("Please convert to standard two-state Life before running this script.")
clist = g.getcells(g.getselrect())
if len(clist)!=20:  g.exit("Please select a rectangle containing the two gliders to be synchronized, and nothing else." \
                         + "\nThere should be at least a four-cell gap between the gliders horizontally and vertically.")
while 1:  # iterate until we find NW0
  stats1, stats2 = findgliders(clist)
  canonical1 = findcanonical(stats1,"NW")
  canonical2 = findcanonical(stats2,"SE")
  if canonical1[1]==0: break
  clist = g.evolve(clist,1)

dir1,phase1,x1,y1 = canonical1
dir2,phase2,x2,y2 = canonical2
charx = "E" if (x1-x2)%2 else "O"  # looks backwards -- the usual fencepost issue 
chary = "e" if (y1-y2)%2 else "o"  # (bounding box coords vs. # of cells in bounding box width)
rating = charx+chary+str(phase2)

clist = g.getcells(g.getselrect()) 
while 1:  # iterate until we find NW0
  stats1, stats2 = findgliders(clist)
  stats2mod = stats2[:]
  stats2mod[2]-=1024
  stats2mod[3]-=1024 # shouldn't matter, but it seems to!
  reversed1 = findcanonical(stats1,"SE")
  reversed2 = findcanonical(stats2mod,"NW")
  if reversed2[1]==0: break
  clist = g.evolve(clist,1)

dirr1,phaser1,xr1,yr1 = reversed1
dirr2,phaser2,xr2,yr2 = reversed2
charrx = "E" if (xr1-xr2)%2 else "O"
charry = "e" if (yr1-yr2)%2 else "o"
ratingr = charrx+charry+str(phaser1)

g.note(rating + " if the first glider in the selection (reading from top down and left to right) is the reference glider\n" \
     + ratingr + " if the second glider is the reference glider (i.e., it will be connected to the NW output in the stamp collection)")
