# synthesise_patt_v1.2.py
# Changes:
#   v1.0:  Goldtiger997's original from http://www.conwaylife.com/forums/viewtopic.php?p=68316#p68316
#   v1.1:  use bz2 module to read directly from compressed files (10x slower than reading from .txt)
#   v1.2:  decompress archive files if .txt versions of files are not found

import golly as g
import bz2
import os.path

g.setrule("B3/S23")

MAX_GENS = 256
GEN_CHECK = 80

offset = 0

# decompress archive files if that hasn't been done yet
#   (reading directly from compressed files takes an order of magnitude longer)
if not os.path.isfile("rles.txt"):
  g.show("Decompressing rles.txt.bz2...")
  temp = bz2.BZ2File('rles.txt.bz2', 'rb')
  data = temp.read()
  with open ("rles.txt","w") as f: f.write(data)

if not os.path.isfile("colseqs.txt"):
  g.show("Decompressing colseqs.txt.bz2...")
  temp = bz2.BZ2File('colseqs.txt.bz2', 'rb')
  data = temp.read()
  with open ("colseqs.txt","w") as f: f.write(data)
  
patts = open("rles.txt","r")
cols = open("colseqs.txt","r")

sols = 0
count = 0
popseq = ""
for i in range(0,GEN_CHECK):
        popseq += str(chr(33+(int(g.getpop())%64)))
        g.run(1)
g.new("Solutions")
curr_patt = patts.readline()
while curr_patt != "":
        curr_col = cols.readline()
        g.show(str(sols) + " solutions found, " + str(count) + " collisions tried. Press <x> to copy current results to clipboard. Press <esc> to quit.")          
        if popseq in curr_col:
                g.putcells(g.parse(curr_patt),offset,0)
                offset += 75
                sols += 1
        event = g.getevent()
        if event.startswith("key x"):
                g.select(g.getrect())
                g.copy()
                g.select([])
        curr_patt = patts.readline()
        count += 1

patts.close()
cols.close()
