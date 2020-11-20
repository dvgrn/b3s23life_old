# extract-single-channel-recipe.py
# glider stream should be pointed northwest.  First glider should be in 3o$o$bo! phase, point at (0,0).
# no selection needed -- script works on entire pattern in current universe
#
# For very large single-channel streams, a variant of recognizer.py would be enormously more efficient

import golly as g
count = 0
recipe = []
while int(g.getpop())>0:
  if g.getcell(0,0)==1 and g.getcell(1,0)==1 and g.getcell(2,0)==1 and g.getcell(0,1)==1 and g.getcell(1,2)==1:
    g.setcell(0,0,0)
    g.setcell(1,0,0)
    g.setcell(2,0,0)
    g.setcell(0,1,0)
    g.setcell(1,2,0)
    recipe+=[count]
    count=0
    if len(recipe)%10 == 0:
      g.show(str(len(recipe)))
      g.fit()
      g.update()
  else:
    count+=1
    g.run(1)
g.note("Done.  Click OK to copy results to clipboard.")
g.setclipstr(str(recipe))
g.show(str(len(recipe)))
