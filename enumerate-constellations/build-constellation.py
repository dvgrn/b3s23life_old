# build-constellation-v13b.py
# Still a work in progress -- it should really work with more than two blinkers,
#    and write to a file instead of messing with the clipboard for output,
#    and probably output RLE instead of cell lists

import golly as g
from time import sleep
from glife.text import make_text

MAXOBJ=2
xsize,ysize=6,9

def getinp(s):
###########################
  temp=g.getcell(x,y)
  g.setcell(x,y,5)
  g.show(s+"Ptr:"+str(ptr)+" x:" +str(x)+" y:"+str(y))
  g.fit()
  g.update()
  g.setcell(x,y,temp)
  # return
  k=g.getevent()
  count=0
  while k=="":
    sleep(.01)
    k=g.getevent()
    count+=1
  if k=="key q none": g.exit()
  return
###########################

patdict={}
# for i in range(2,xsize+1):
#   for j in range(2,ysize+1):
#     patdict[str([i,j])]=[]
objs=["2o$2o!","2o$obo$bo!","b2o$obo$bo!","bo$obo$b2o!","bo$obo$2o!", # block and boat
      "b2o$o2bo$b2o!","bo$obo$obo$bo!","bo$obo$bo!","b2o$o2bo$o2bo$b2o!", # beehive, tub, pond
      "2o$obo$b2o!", "b2o$obo$2o!", "b2o$o2bo$obo$bo!", # ship, loaf1
      "b2o$o2bo$bobo$2bo!","2bo$bobo$o2bo$b2o!","bo$obo$o2bo$b2o!", # other loaves
      "2o$bo$bobo$2b2o!","3bo$b3o$o$2o!","2o$obo$2bo$2b2o!","2b2o$3bo$3o$o!", # one chirality of eater
      "2o$o$b3o$3bo!","2b2o$bobo$bo$2o!","o$3o$3bo$2b2o!","2b2o$2bo$obo$2o!", # the other chirality of eater
      "2o$obo$bobo$2bo!","2b2o$bobo$obo$bo!","bo$obo$bobo$2b2o!","2bo$bobo$obo$2o!", # longboats
      "bo$3o$bo!"]  # and last but not least, the weird case -- blinkers
objlist=[]
for i in range(len(objs)):
  # normalize so that the first ON cell in the list is always (0,0)
  templist=g.parse(objs[i])
  objlist+=[g.transform(templist,-templist[0],-templist[1])]
numobjs=len(objlist)
zonelist=[]
for item in objlist:
  g.setrule("B12345678/S012345678")
  neighbors=g.evolve(item,1)
  g.setrule("B2345678/S012345678")
  zone=g.evolve(neighbors,1)
  zonelist+=[zone]    # includes cells for object also

g.setrule("LifeHistory")
nearlist=[[i,j] for i in range(-1,xsize+1) for j in range(-1,ysize+1) if i<0 or i>=xsize or j<0 or j>=ysize]
count,x,y,ptr,filledlist,searchlist=0,0,0,0,[],[]
while y==0 or len(searchlist)>0:
  overlap=([x,y] in nearlist)
  # place current object
  #############################################
  # TODO:  if there's an overlap, set ptr to max value, then handle all cases with same code at the bottom
  if overlap==0:
    # g.show(str(ptr))
    obj=g.transform(objlist[ptr],x,y)
    objpairs=[[obj[i],obj[i+1]] for i in range(0,len(obj),2)]
    for item in objpairs:
      if item in nearlist:
        overlap=1
        break
    if overlap==0:
      zone=g.transform(zonelist[ptr],x,y)
      zonepairs=[[zone[i],zone[i+1]] for i in range(0,len(zone),2)]
      for item in zonepairs:
        if item in filledlist:
          overlap=2
          break
      if overlap==0:
        g.new("TestPage")
        newptr,newx,newy=ptr+1,x,y
        if newptr>=len(objlist): newptr,newx=0,newx+1
        if newx>=xsize-1: newptr,newx,newy=0,0,y+1
        searchlist.append([newx,newy,newptr,nearlist[:],filledlist[:]]) # add next state to search to the stack
        nearlist+=zonepairs
        filledlist+=objpairs
        for i,j in nearlist: g.setcell(i,j,2)
        minx, maxx, miny, maxy = 999,-999,999,-999
        for i,j in filledlist:
          g.setcell(i,j,1)
          if i<minx:minx=i
          elif i>maxx:maxx=i
          if j<miny: miny=j
          elif j>maxy: maxy=j          
        # Take a snapshot of the current successful placement
        # [e.g., successful if two objects placed, etc.]
        if minx==0 and miny==0:
          keystr=str(maxx+1)+"x"+str(maxy+1)
          if keystr not in patdict: patdict[keystr]=[]
          if filledlist not in patdict[keystr]: patdict[keystr]+=[filledlist[:]]
        # Now continue searching from where we are
        count+=1
        if count%100==0:
          g.show(str(count))
          g.update()        
        ptr,x=0,x+4
      else:  # the neighbor zone for this object overlaps some already placed object
        ptr+=1
        if ptr>=len(objlist): ptr,x=0,x+1
    else: # the object itself overlaps some already placed object's neighborhood
      ptr+=1
      if ptr>=len(objlist): ptr,x=0,x+1
  else:
    ptr,x=0,x+1
  # getinp("Overlap type " + str(overlap) + ".  Lenlist="+str(len(searchlist))+".")
  if x>=xsize-1: ptr,x,y=0,0,y+1
  if y>=ysize-1 or len(searchlist)>=MAXOBJ:
    # we've reached the end of the frame.
    # Time to clear the last placed object, go back to that x,y
    if searchlist==[]:
      g.new("TestPage")
      g.exit("Search is complete.")
    x,y,ptr,nearlist,filledlist=searchlist.pop()

# no point in looking at configurations with no object on the first line
g.new("TestPage")
outstr="Total count = " + str(count)
t=make_text(outstr,"mono")
g.putcells(t,0,-20)
s=""
for item in sorted(patdict):
  y=0
  t = make_text(item + " ("+str(len(patdict[item]))+")","mono")
  outstr+="\n" + item + " ("+str(len(patdict[item]))+")"
  g.putcells(t,x-6,y)
  y+=30
  for pat in patdict[item]:
    blinkercenters = []
    for i,j in pat:
      if [i-1,j] in pat and [i+1,j] in pat and [i,j-1] in pat and [i,j+1] in pat:
        blinkercenters+=[[i,j]]
    if len(blinkercenters)>0:
      if len(blinkercenters)==1:
        i,j = blinkercenters[0]
        patphase1=[coord for coord in pat if coord not in [[i-1,j],[i+1,j]]]
        patphase2=[coord for coord in pat if coord not in [[i,j-1],[i,j+1]]]
        s+=str(patphase1)+"\n"+str(patphase2)+"\n"
        for cell in patphase1:
          g.setcell(cell[0]+x,cell[1]+y,1)
        y+=20
        for cell in patphase2:
          g.setcell(cell[0]+x,cell[1]+y,1)
        y+=20
      elif len(blinkercenters)==2:
        i,j = blinkercenters[0]
        m,n = blinkercenters[1]
        patphase1=[coord for coord in pat if coord not in [[i-1,j],[i+1,j],[m-1,n],[m+1,n]]]
        patphase2=[coord for coord in pat if coord not in [[i,j-1],[i,j+1],[m-1,n],[m+1,n]]]
        patphase3=[coord for coord in pat if coord not in [[i-1,j],[i+1,j],[m,n-1],[m,n+1]]]
        patphase4=[coord for coord in pat if coord not in [[i,j-1],[i,j+1],[m,n-1],[m,n+1]]]
        s+=str(patphase1)+"\n"+str(patphase2)+"\n"+str(patphase3)+"\n"+str(patphase4)+"\n"
        for cell in patphase1:
          g.setcell(cell[0]+x,cell[1]+y,1)
        y+=20
        for cell in patphase2:
          g.setcell(cell[0]+x,cell[1]+y,1)
        y+=20
        for cell in patphase3:
          g.setcell(cell[0]+x,cell[1]+y,1)
        y+=20
        for cell in patphase4:
          g.setcell(cell[0]+x,cell[1]+y,1)
        y+=20
      else:
        g.note("The general case with more than two blinkers is not yet handled in this code.  Skipping this configuration.")
    else:
      s+=str(pat)+"\n"
      for cell in pat:
        g.setcell(cell[0]+x,cell[1]+y,1)
      y+=20
  x+=100
g.note("Search is complete.")
g.setclipstr(s)
