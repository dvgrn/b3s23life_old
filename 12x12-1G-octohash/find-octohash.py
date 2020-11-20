import golly as g
import hashlib

fingerprintfile = "/YOUR/PATH/HERE/octohashes2obj2x12b"

NUMLINES = 455380
GRIDSIZE = 40

chardict = {}
for i in range(37, 127):
  chardict[i-37] = chr(i)

chardict[92-37] = "!"  # backslash
chardict[39-37] = "#"  # apostrophe
chardict[44-37] = "$"  # comma
  
def get9char(inputstr):
  h = hashlib.sha1()
  h.update(inputstr)
  i = 0  # convert first seven bytes of SHA1 digest to an integer
  for char in h.digest()[:7]:
    i = i*256 + ord(char)
  s = ""
  while len(s)<9:
    d = i/90
    r = i - d*90
    s = chardict[r] + s
    i = (i - r) / 90   
  return s

def getoctohash(clist):
  ptr = 0
  g.new("Octotest"+str(count))
  for orientation in [[1,0,0,1],[0,-1,1,0],[-1,0,0,-1],[0,1,-1,0],[-1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,-1,-1,0]]:
    g.putcells(clist,ptr*2048,0,*orientation)
    ptr += 1
  for j in range(8):
    g.select([2048*j-1024,-1024,2048,2048])
    g.shrink()
    r = g.getselrect()
    if r == []: r = [0,0,1,1]
    pat = g.getcells(r)
    deltax, deltay = 0, 0
    if pat != []:
      deltax, deltay = -pat[0], -pat[1]
    if j==0:
      minstr = str(g.transform(pat, deltax, deltay))
    else:
      strpat = str(g.transform(pat, deltax, deltay))
      if  strpat < minstr:
        minstr = strpat
  return " " + get9char(minstr)

r = g.getselrect()
if r == []:
  g.exit("No selection.  Select something to find by fingerprint.")
g.fitsel()
r = g.getselrect()
if r == []:
  g.exit("No selection.  Select something to find by fingerprint.")

count = NUMLINES
outptrx, outptry, matches = 0,0,0
pat = g.getcells(r)

g.addlayer()  # do tests in a new layer, then put results there
hash = getoctohash(pat)
g.new("Output")
if pat != []:
  g.putcells(pat,-pat[0]-GRIDSIZE,-pat[1])

for i in range(10):
  s = "Scanning " + fingerprintfile + "_" + str(i) + ".txt"
  with open(fingerprintfile + "_" + str(i) + ".txt", "r") as f:
    for line in f:
      count -= 1
      if hash in line:
        matches += 1
        matchingpat = line[:line.index(" ")]
        g.putcells(g.parse(matchingpat),outptrx*GRIDSIZE,outptry*GRIDSIZE)        
        outptrx+=1
        if outptrx % 50 == 0:
          outptrx, outptry = 0, outptry + 1
          g.fit()
          g.update()
      if count % 1000 == 0:
        g.show(s + " Lines remaining: " + str(count/1000) + "K lines.")
plural = "" if matches==1 else "s"
g.show("Found " + str(matches) + " line" + plural + " matching" + hash + " in " + str(NUMLINES) + " lines of " + fingerprintfile + ".")