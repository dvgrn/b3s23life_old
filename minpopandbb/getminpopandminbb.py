# getminpopandminbb.py
import golly as g

maxticks = g.getstring ("Enter maximum number of ticks to search: ", "1024")
r = g.getrect()
count, minT, minpop, minbbx, minbby, minbbt = 0, 0, int(g.getpop()), r[2], r[3], 0
while count<=int(maxticks):
  g.run(1)
  count+=1
  newpop = int(g.getpop())
  if newpop<minpop:
    minpop = newpop
    minT = count
  r = g.getrect()
  if r[2]*r[3]<minbbx*minbby:
    minbbx, minbby, minbbt = r[2], r[3], count
  if count%256==0:
   g.show("T: " + str(count) + "    Current pop: "+str(newpop)+"    Current minimum pop: " + str(minpop) + " at T = " + str(minT) + ". Min box = "+str([minbbx, minbby]) + " at T = " + str(minbbt))
   g.fit()
   g.update()
g.note("Finished scan of " + maxticks + " ticks.  Minimum population: " +str(minpop) + " at T = " + str(minT) + ". Min box = "+str([minbbx, minbby]) + " at T = " + str(minbbt))