# code for enumerating all 3Disotropic bits -- 3D isotropic range-1 Moore neighborhood
#   (creation of dictionary is commented out at the end of the code,
#    because it slowed down the counting process unnecessarily --
#    but it appeared to work okay.)
# This is proof-of-concept IFFO code [Incredibly Far From Optimized]

import golly as g
from itertools import permutations 
perm = list(permutations(range(1, 4)))
affinelist=[]
d={}

for a in [1,-1]:
  for b in [1,-1]:
    for c in [1,-1]:
      d[1], d[2], d[3] = [a,0,0], [0,b,0], [0,0,c]
      for p in perm:
        affine = d[p[0]]+d[p[1]]+d[p[2]]
        affinelist+=[affine]

neighbors = [(0,0,1),
             (0,1, 1),(1,1, 1),(1,0, 1),(1,-1, 1),(0,-1, 1),(-1,-1, 1),(-1,0, 1),(-1,1, 1),
             (0,1, 0),(1,1, 0),(1,0, 0),(1,-1, 0),(0,-1, 0),(-1,-1, 0),(-1,0, 0),(-1,1, 0),
             (0,1,-1),(1,1,-1),(1,0,-1),(1,-1,-1),(0,-1,-1),(-1,-1,-1),(-1,0,-1),(-1,1,-1),
             (0,0,-1)
            ]
ndict = {(0, 0, 1):"a",
         (0, 1, 1):"b",(1, 1, 1):"c",(1,0, 1):"d",(1, -1, 1):"e",(0, -1, 1):"f",(-1, -1, 1):"g",(-1, 0, 1):"h",(-1, 1, 1):"i",
         (0, 1, 0):"j",(1, 1, 0):"k",(1,0, 0):"l",(1, -1, 0):"m",(0, -1, 0):"n",(-1, -1, 0):"o",(-1, 0, 0):"p",(-1, 1, 0):"q",
         (0, 1, -1):"r",(1, 1, -1):"s",(1,0, -1):"t",(1, -1, -1):"u",(0, -1, -1):"v",(-1, -1, -1):"w",(-1, 0, -1):"x",(-1, 1, -1):"y",
         (0, 0, -1):"z"
        }

def getletters(neighborlist):
  ltrs = []
  for item in neighborlist:
    ltrs += [ndict[item]]
  return "".join(sorted(ltrs))

# g.note(str(affinelist))
# g.note(str(len(affinelist)))
# g.note(getletters(neighbors))
# g.exit()

isodict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0}

for i in xrange(2**27-1, 2**26-1,-1): # 2**26,2**27):
   arrangement = bin(i)[3:]
   nlist = []
   for j in range(26):
     if arrangement[j]=="1":
       nlist += [neighbors[j]]
   numneighbors = len(nlist)
   if numneighbors > 13:
     continue # for simple counts, skip processing for things that are more than half 1's

   letters = getletters(nlist)
   bestletters = letters
   
   for affine in affinelist:
     altlist = []
     for k in nlist:
       a, b, c = k
       m,n,o,p,q,r,s,t,u = affine
       d = m*a + n*b + o*c
       e = p*a + q*b + r*c
       f = s*a + t*b + u*c
       altlist += [(d,e,f)]
     altletters = getletters(altlist)
     if altletters<bestletters: bestletters = altletters
     # g.note(str(i) + ": " + str(nlist)+ " -- " + bestletters + " // " + str(affine) + " = " + str(altlist) + " :: " + altletters)
   # if bestletters not in isodict:
   #   isodict[bestletters]=1
   # else:
   #   isodict[bestletters]+=1
   # if i%1024==0:
   #   g.show(str(i) + ": " + str(len(isodict)) )
   #   if i>67200000:
   #     g.setclipstr(str(isodict))
   #     g.exit()
   if bestletters == letters:
     isodict[numneighbors]+=1
   if i%1024==0:
     g.show(str(i) + ": " + str(isodict))
g.setclipstr(str(isodict))
