# glider-rewinder.py
# http://conwaylife.com/forums/viewtopic.php?f=9&t=1107
# 29 May 2013: Version 0.81
#  - fixed a bug in getenvelope() that prevented recognition of closely-spaced gliders or *WSSes
# 18 October 2020: Version 1.0
#  - updated to work correctly with Golly 4.0+ and Python 3.x, 

import golly as g
import os
import itertools
from glife import *

lib=[["NW","bo$2o$obo!"],["NE","2o$b2o$o!"],["SE","obo$b2o$bo!"],["SW","2bo$2o$b2o!"],
     ["NL","bo$3o$ob2o$b3o$b2o!"],["EL","2b2o$2ob2o$4o$b2o!"],["SL","b2o$3o$2obo$b3o$2bo!"],["WL","2b2o$b4o$2ob2o$b2o!"],
     ["NM","bo$3o$ob2o$b3o$b3o$b2o!"],["EM","3b2o$3ob2o$5o$b3o!"],["SM","b2o$3o$3o$2obo$b3o$2bo!"],["WM","2b3o$b5o$2ob3o$b2o!"],
     ["NH","bo$3o$ob2o$b3o$b3o$b3o$b2o!"],["EH","4b2o$4ob2o$6o$b4o!"],["SH","b2o$3o$3o$3o$2obo$b3o$2bo!"],["WH","2b4o$b6o$2ob4o$b2o!"],
     ["B3","3o!"],["B8a","2o$o$3bo$2b2o!"],["B8b","2b2o$3bo$o$2o!"],["loaferWa","b2o4b2o$o2b2ob3o$bobo$2bo$8bo$6b3o$5bo$6b2o$7bo!"]]

def getenvelope(pat):
  env=[]
  if len(pat)%2:
    g.exit("Must be a 2-state list.")
  for i in range(0,len(pat)-1,2):
    for x in range(-1,2):
      for y in range(-1,2):
        if abs(x)!=0 or abs(y)!=0: # add eight neighbors of each ON cell to the mask
          if [pat[i]+x,pat[i+1]+y] not in env:
            env.append([pat[i]+x,pat[i+1]+y])
  for i in range(0,len(pat),2):
    if [pat[i],pat[i+1]] in env:
      env.remove([pat[i],pat[i+1]]) # take original pattern back out of mask
    # else: # with the reduced envelope, this will now happen, e.g. with *WSS singleton sparks
    #  g.note("Technical error: " + str([pat[i],pat[i+1]])+ " not in envelope:" + str(env) + " \n\n" + str(pat)) 
  return list(itertools.chain.from_iterable(env))

r=g.getselrect()
if len(r)==0:
  r=g.getrect()
  if len(r)==0: g.exit("No pattern, nothing to do.")
sel = g.getcells(r)
if len(sel)==0: g.exit("Nothing in selection.")
if len(sel)%2: g.exit("Can't do the rewinding trick on multistate rules.")
all = g.getcells(g.getrect())
allcoords=[]
for i in range(0,len(all),2):
  allcoords.append([all[i],all[i+1]])

# g.show("Processing object library...")
odict=dict()
for i in range(len(lib)):
  # g.show("Processing object " + lib[i][0])
  # run and normalize each library object until a duplicate of the original pattern appears
  # The number of ticks to duplication, and the offset, give all the information needed to rewind...
  obj = g.parse(lib[i][1])
  basex, basey,ticks,newobj=obj[0],obj[1],0,[]
  baseobj = g.transform(obj,-basex,-basey)
  basepat = pattern(baseobj) # use glife to avoid having to add a layer in Golly
  
  # TODO: figure out the actual right way to compare in Python 3.x... baseobj>newobj or baseobj<newobj, maybe?
  while str(baseobj) != str(newobj):
    ticks+=1
    newpat=basepat[ticks]
    newlist = list(newpat)
    newobj=g.transform(newpat,-newlist[0],-newlist[1])
    if ticks>999:
      g.exit(obj[0] + " in library has no reasonable repeat time.")
  stridex,stridey=newlist[0],newlist[1]
  
  # odict key is name+phase, and there's an entry for each phase of each object
  # Contains list of repeat, stridex, stridey, dx, dy, clist, envclist.
  # By convention, the first ON cell in phase 0 is at (0,0) and dx and dy are also 0,0.
  # The first ON cell in other phases is also 0,0 but dx and dy will be altered appropriately.
  
  odict[lib[i][0]+"_0"]=[ticks, stridex, stridey, 0, 0, baseobj, getenvelope(baseobj)]
  for t in range(1,ticks):
    newlist=list(basepat[t])
    normalized=g.transform(newlist,-newlist[0],-newlist[1])
    odict[lib[i][0]+"_"+str(t)]=[ticks,stridex,stridey,newlist[0],newlist[1],normalized,getenvelope(normalized)]
g.show("")

# make a list of coordinate pairs that might be Objects of Interest (gliders or LWSSes)
coords=[]
for i in range(0,len(sel),2):
  coords.append([sel[i],sel[i+1]])

rewindable=[]
# now go through the selection and find all the recognizable patterns
i=0
while i<len(coords):
  x0,y0=coords[i][0], coords[i][1]
  for k, v in list(odict.items()):
    clist = v[5] # object cell list
    match=1
    for j in range(0,len(clist),2):
      if [x0+clist[j],y0+clist[j+1]] not in coords:
        match=0
        break # a cell in this object is not in the selected pattern
    if match:
      envclist=v[6] # object envelope cell list
      for j in range(0,len(envclist),2):
        if [x0+envclist[j],y0+envclist[j+1]] in allcoords: # could use coords instead, but selection should be increased 2 cells all around
          match=0
          break # a cell in the surrounding must-be-OFF area is ON
    if match:
      # remove all recognized cells from coords
      for j in range(0,len(clist),2):
        crd=[x0+clist[j],y0+clist[j+1]]
        if crd in coords:
          coords.remove(crd)
        else:
          g.exit("A coordinate that should have been there wasn't: " + str(crd) + "\n\n" + str(coords))
      rewindable.append([k,x0-v[3],y0-v[4]])
      break # no need to go through rest of items in dictionary
  if not match:
    i+=1 # only increment index if current coord has not been removed due to a match

# at the end of this process, coords should be flattenable to a cell list containing all unrecognized stuff

g.setgen("-1")

# remove all rewindable items
for item in rewindable:
  lookup=odict[item[0]]
  # odict[name+phase]=[ticks, stridex, stridey, dx, dy, clist, getenvelope(clist)]
  clist = lookup[5]
  for i in range(0,len(clist),2):
    g.setcell(clist[i]+item[1]+lookup[3],clist[i+1]+item[2]+lookup[4],0)

# now put them back one tick earlier...
for item in rewindable:
  namephase=item[0]
  ind=namephase.find("_")
  name=namephase[:ind]
  dx, dy=0,0
  phase=int(namephase[ind+1:])
  if phase==0:
    temp=odict[namephase]
    phase, dx, dy = temp[0], temp[1], temp[2] # number of ticks until repeat
  newobj=odict[name+"_"+str(phase-1)]
  offsetx,offsety,clist=newobj[3],newobj[4],newobj[5]
  for i in range(0,len(clist),2):
    # recorded location plus relative cell location plus offset minus stride-if-phase-has-cycled:
    g.setcell(item[1]+clist[i]+offsetx-dx,item[2]+clist[i+1]+offsety-dy,1)
    # could easily use the envelope, newobj[6], here to check for conflicts...
    # but what exactly should I do if there's a conflict?
