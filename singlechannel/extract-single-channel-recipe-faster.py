# extract-single-channel-recipe-faster.py
# glider stream should be pointed northwest.  First glider should be in 3o$o$bo! phase, point at (0,0).
# no selection needed -- script works on entire pattern in current universe

# the setcell() calls are all optional, and make the process go slower --
#   just added as a way of debugging, and to show progress.
#   (If they're removed, change the exit condition to something about bounding box.)

import golly as g

gliders=["3o$o$bo!","b2o$2o$2bo!","b2o$bobo$bo!","2bo$b2o$bobo!"]

x, y = 0, 0
count, lastcount = 0, 0
recipe = []
while int(g.getpop())>0:
  if g.getcell(x+0,y+0)==1 and g.getcell(x+1,y+0)==1 and g.getcell(x+2,y+0)==1 and g.getcell(x+0,y+1)==1 and g.getcell(x+1,y+2)==1:
    g.setcell(x+0,y+0,0)
    g.setcell(x+1,y+0,0)
    g.setcell(x+2,y+0,0)
    g.setcell(x+0,y+1,0)
    g.setcell(x+1,y+2,0)
    recipe+=[count-lastcount]
    lastcount = count
  elif g.getcell(x+1,y+0)==1 and g.getcell(x+2,y+0)==1 and g.getcell(x+0,y+1)==1 and g.getcell(x+1,y+1)==1 and g.getcell(x+2,y+2)==1:
    g.setcell(x+1,y+0,0)
    g.setcell(x+2,y+0,0)
    g.setcell(x+0,y+1,0)
    g.setcell(x+1,y+1,0)
    g.setcell(x+2,y+2,0)
    recipe+=[count+1-lastcount]
    lastcount = count+1
  elif g.getcell(x+1,y+0)==1 and g.getcell(x+2,y+0)==1 and g.getcell(x+1,y+1)==1 and g.getcell(x+3,y+1)==1 and g.getcell(x+1,y+2)==1:
    g.setcell(x+1,y+0,0)
    g.setcell(x+2,y+0,0)
    g.setcell(x+1,y+1,0)
    g.setcell(x+3,y+1,0)
    g.setcell(x+1,y+2,0)
    recipe+=[count+2-lastcount]
    lastcount = count+2
  elif g.getcell(x+2,y+0)==1 and g.getcell(x+1,y+1)==1 and g.getcell(x+2,y+1)==1 and g.getcell(x+1,y+2)==1 and g.getcell(x+3,y+2)==1:
    g.setcell(x+2,y+0,0)
    g.setcell(x+1,y+1,0)
    g.setcell(x+2,y+1,0)
    g.setcell(x+1,y+2,0)
    g.setcell(x+3,y+2,0)
    recipe+=[count+3-lastcount]
    lastcount = count+3
  else:
    count += 4
    x += 1
    y += 1
  if count%1000 == 0:
    g.show(str(len(recipe)))
    g.fit()
    g.update()
g.note("Done.  Click OK to copy results to clipboard.")
g.setclipstr(str(recipe))
g.show(str(len(recipe)))
