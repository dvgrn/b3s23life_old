# APGompiler.py, version 0.8 (Osqrtlogt test)
# Version 0.5:  If GPC pattern is open, create compiled program on new layer, copy into GPC
#               -- this is a quick temporary fix until the modularized compiler is complete
#               The copy/paste math assumes that the first INITIAL state will jump to the second state (!)
# Version 0.6:  Add some error-checking related to paired Z/NZ options, and * syntax
# Version 0.7:  Fix problem with ZZ and * syntax appearing on very last line of program
# Version 0.8:  Added "ZNZbackstop" to prevent gliders leaking out of the computer when Z and NZ are both returned

import golly as g

APGsembly = """# Time to support comments and blank lines in APGsembly
# A 'ZZ' means only Z input is possible for this state
INITIAL; ZZ; A1; READ SQ
A1; Z; B1; SET SQ, NOP
A1; NZ; C1; NOP
B1; ZZ; B2; DEC SQX
B2; Z; B3; DEC SQY
B2; NZ; B2; DEC SQX
B3; Z; B4; TDEC R0
B3; NZ; B3; DEC SQY
B4; Z; B5; TDEC R1
B4; NZ; B4; TDEC R0
B5; Z; B6; TDEC R2
B5; NZ; B5; TDEC R1
B6; Z; A1; READ SQ
B6; NZ; B6; TDEC R2
# No possibility of an NZ input here
C1; ZZ; C2; TDEC R0
C2; Z; C4; DEC SQX
C2; NZ; C3; INC SQX, NOP
# removed another NZ line here
C3; ZZ; A1; READ SQ
C4; Z; C5; INC SQY, INC R1, NOP
C4; NZ; C4; DEC SQX
# use * format here, because DEC SQX can return either Z or NZ
C5; *; C6; TDEC R1
C6; Z; C7; TDEC R2
C6; NZ; C6; INC R2, TDEC R1
C7; Z; A1; READ SQ
C7; NZ; C7; INC R0, INC R1, TDEC R2

# unreachable program states for compiler testing
C8; ZZ; C8; NOP
C9; *; C9; NOP"""
progname = "Osqrtlogt-plus-test"

outputlist = ["NOP", "OUTPUT 0", "OUTPUT 1", "OUTPUT 2", "OUTPUT 3", "OUTPUT 4", "OUTPUT 5", "OUTPUT 6", "OUTPUT 7", "OUTPUT 8", "OUTPUT 9", "OUTPUT .", \
             "DEC SQX", "INC SQX", "READ SQ", "SET SQ", "DEC SQY", "INC SQY", \
             "RESET T0", "SET T0", "READ T0", "DEC T0", "INC T0", "RESET T1", "SET T1", "READ T1", "DEC T1", "INC T1", \
             "RESET T2", "SET T2", "READ T2", "DEC T2", "INC T2", "RESET T3", "SET T3", "READ T3", "DEC T3", "INC T3", \
             "RESET T4", "SET T4", "READ T4", "DEC T4", "INC T4", "RESET T5", "SET T5", "READ T5", "DEC T5", "INC T5", \
             "RESET T6", "SET T6", "READ T6", "DEC T6", "INC T6", "RESET T7", "SET T7", "READ T7", "DEC T7", "INC T7", \
             "RESET T8", "SET T8", "READ T8", "DEC T8", "INC T8", "RESET T9", "SET T9", "READ T9", "DEC T9", "INC T9", \
             "RESET T10", "SET T10", "READ T10", "DEC T10", "INC T10", "RESET T11", "SET T11", "READ T11", "DEC T11", "INC T11", \
             "RESET T12", "SET T12", "READ T12", "DEC T12", "INC T12", "RESET T13", "SET T13", "READ T13", "DEC T13", "INC T13", \
             "RESET T14", "SET T14", "READ T14", "DEC T14", "INC T14", "RESET T15", "SET T15", "READ T15", "DEC T15", "INC T15", \
             "RESET T16", "SET T16", "READ T16", "DEC T16", "INC T16", "RESET T17", "SET T17", "READ T17", "DEC T17", "INC T17", \
             "RESET T18", "SET T18", "READ T18", "DEC T18", "INC T18", "RESET T19", "SET T19", "READ T19", "DEC T19", "INC T19", \
             "TDEC R0", "INC R0", "TDEC R1", "INC R1", "TDEC R2", "INC R2", "TDEC R3", "INC R3", "TDEC R4", "INC R4", \
             "TDEC R5", "INC R5", "TDEC R6", "INC R6", "TDEC R7", "INC R7", "TDEC R8", "INC R8", "TDEC R9", "INC R9", \
             "ADD B0", "ADD B1", "ADD A1", "SUB B0", "SUB B1", "SUB A1", "MUL 1", "MUL 0"]

outputdict = {}
for i in range(len(outputlist)):
  outputdict[outputlist[i]]=i

ZNZ = g.parse("""135bo$133b3o$132bo$132b2o7bo$139b3o$138bo24bo$138b2o23b3o$166bo$165b2o
$180b2o$180bo$177b2obo$176bo2bo$177b2o$147b2o13b2o$147b2o13b2o7$149b2o
6bob2o$126b2o21bobo3b3ob2o$125bobo23bo2bo$125bo25b2o2b3ob2o$124b2o31bo
bo$157bobo10b2o$158bo11b2o11$17bo127bo$15b3o125b3o$14bo127bo$14b2o126b
2o$20bo127bo$18b3o125b3o$17bo127bo$17b2o126b2o14$7b2o126b2o$8bo127bo$
5b3o125b3o$5bo127bo$191bo$189b3o$188bo$188b2o$23b2o126b2o$23bo127bo$
24b3o125b3o41b2o$26bo127bo42bo$197bob2o$189b2o4b3o2bo$189b2o3bo3b2o$
194b4o$180b2o15bo$15b2o126b2o34bobo12b3o$6b2o7b2o117b2o7b2o34bo13bo$7b
o127bo42b2o14b5o$7bobo125bobo60bo$8b2o126b2o58bo$24b2o126b2o42b2o$24bo
127bo$22bobo125bobo$22b2o126b2o3$3b2o126b2o$4bo127bo$4bobo18bo106bobo
18bo$5b2o17bobo106b2o17bobo$25bo127bo$32bo127bo$32b3o125b3o$35bo127bo$
34b2o126b2o$49b2o126b2o$49bo127bo$46b2obo124b2obo$2b2o41bo2bo81b2o41bo
2bo$bobo42b2o81bobo42b2o$bo5b2o22b2o96bo5b2o22b2o$2o4bo2bo21b2o95b2o4b
o2bo21b2o$7b2o126b2o3$9b2o7b2o3bo113b2o7b2o3bo$9b2o7bo3bobo112b2o7bo3b
obo$19bo3bobo121bo3bobo$20bo3bobob2o118bo3bobob2o$18bob4o2bob2o116bob
4o2bob2o$17bobo3bobo119bobo3bobo$17bobo2bo2b2ob2o115bobo2bo2b2ob2o$18b
o3b2o2bobo117bo3b2o2bobo$26bobo10b2o113bobo10b2o$27bo11b2o114bo11b2o!""")

onlyZ = g.parse("""135bo$133b3o$132bo$132b2o7bo$139b3o$138bo24bo$138b2o23b3o$166bo$165b2o
$180b2o$180bo$177b2obo$176bo2bo$177b2o$147b2o13b2o$147b2o13b2o7$149b2o
6bob2o$126b2o21bobo3b3ob2o$125bobo23bo2bo$125bo25b2o2b3ob2o$124b2o31bo
bo$138b2o17bobo10b2o$138bo19bo11b2o$139b3o$141bo9$17bo$15b3o$14bo$14b
2o$20bo$18b3o$17bo$17b2o14$7b2o$8bo$5b3o$5bo5$23b2o$23bo$24b3o$26bo6$
15b2o$6b2o7b2o$7bo$7bobo$8b2o$24b2o$24bo$22bobo$22b2o3$3b2o$4bo$4bobo
18bo$5b2o17bobo$25bo$32bo$32b3o$35bo$34b2o$49b2o$49bo$46b2obo$2b2o41bo
2bo$bobo42b2o$bo5b2o22b2o$2o4bo2bo21b2o$7b2o3$9b2o7b2o3bo$9b2o7bo3bobo
$19bo3bobo$20bo3bobob2o$18bob4o2bob2o$17bobo3bobo$17bobo2bo2b2ob2o$18b
o3b2o2bobo$26bobo10b2o$27bo11b2o!""")

splitter = g.parse("""48bo$48b3o$51bo$50b2o3$42b2o$42bo$39b2obo$39bo2b3o4b2o$40b2o3bo3b2o$
42b4o$42bo15b2o3b2o$43b3o12bobobobo$46bo13bobo$41b5o14bo2bo$41bo19bobo
$43bo18bo$42b2o4$77b2o$77b2o4$57b2o$56bobo$56bo18b2o$55b2o7b2o9bo$64b
2o10bo$75b2o$72b2o$9bo62b2ob2o$9b3o63bo$12bo59b2o3bo$11b2o10bo47bo2b4o
$22bobo45bobobo$22bobo27bo18bo2bob2o$o20b2ob3o25b3o19bobo$3o24bo27bo
17b2o2bo$3bo17b2ob3o6bo20b2o14bobo2bobo$2b2o17b2obo6b3o15bo20b2o2bobo$
30bo18b3o23bo$30b2o20bo$5b2o44b2o$4bo2bo$5b2o4$48b2o$48b2o17b2o$67b2o$
17b2o$18bo$15b3o50b2o$15bo52bo$55b2o12b3o$38b2o16bo14bo$38bo14b3o$39b
3o11bo$41bo!""")

transrefl = g.parse("""24bo$22b3o$21bo$20bobo$20bobo$21bo5$5b2o$5b2o4$25b2o$25bobo$27bo$18b2o
7b2o$18b2o2$8bob2o$6b3ob2o$5bo$6b3ob2o$8bobo$8bobo$9bo6$18b2o$18b2o16$
3bob2o$b3ob2o$o$b3ob2o$3bobo2bo$6b3o$11bo5b2o$8b4o5b2o$8bo$9bo$8b2o!""")

Snark_S = g.parse("""15bo$13b3o$12bo$12b2o7$2b2o$bobo5b2o$bo7b2o$2o2$14bo$10b2obobo$9bobobo
bo$6bo2bobobobob2o$6b4ob2o2bo2bo$10bo4b2o$8bobo$8b2o!""")

Snark_E = g.parse("""18b2o$18bo$20bo$2o14b5o$bo13bo$bobo12b3o$2b2o15bo$16b4o$11b2o3bo3b2o$
11b2o4b3o2bo$19bob2o$19bo$18b2o3$10b2o$10bo$11b3o$13bo!""")

Snark_N = g.parse("""9b2o$8bobo$2b2o4bo$o2bo2b2ob4o$2obobobobo2bo$3bobobobo$3bobob2o$4bo2$
17b2o$8b2o7bo$8b2o5bobo$15b2o7$5b2o$6bo$3b3o$3bo!""")

# ZNZstopper = g.parse("2o126b2o$o127bo$b3o125b3o$3bo127bo!")

ZNZbackstop = g.parse("""2o126b2o$o127bo$b3o125b3o$3bo127bo7$10b2obo124b2obo$10b2ob3o122b2ob3o$
16bo127bo$10b2ob3o122b2ob3o$11bobo125bobo$11bobo125bobo$12bo127bo!""")

startpat = g.parse("3o$o$bo!", 255, 58)

proglines = (APGsembly + "\nEND OF PROGRAM; Z\nEND OF PROGRAM; NZ").split('\n')

# pre-processing to remove blank lines and comments, and deal with * / ZZ format
progonly = []
NZflag = 0
for line in proglines:
  if line.strip()!="" and line.strip()[:1]!="#":
    if NZflag == 0:
      Zline = line
      NZflag = 1
    else:
      NZflag = 0
      if line == "END OF PROGRAM; NZ":
        break
      
      # process the next pair of lines, make sure it's a matched Z + NZ set
      Zparts = Zline.split("; ")
      NZparts = line.split("; ")
      if Zparts[0]==NZparts[0]:
        if Zparts[1]=="Z" and NZparts[1]=="NZ":
          progonly += [Zline,line]
        else:
          g.note("Pre-processing failed on lines:\n" + Zline + "\n" + line + "\nNeed Z line followed by NZ line, or * / ZZ syntax.")
          g.exit()
      else:
        if Zparts[1]=="*":
          progonly += [Zline.replace("*","Z"),Zline.replace("*","NZ")]
          Zline = line
          NZflag = 1
        elif Zparts[1]=="ZZ":
          progonly += [Zline, Zparts[0]+"; NZ"]  # .replace("; ZZ;","; Z;")
          Zline = line
          NZflag = 1
        else:
          g.note("Pre-processing failed on lines:\n" + Zline + "\n" + line + "\nNeed a Z and NZ line for each state, or * / ZZ syntax.")
          g.exit()

numstates = len(progonly)

statedict = {}
for i in range(0,numstates,2):
  parts = progonly[i].split("; ")
  statedict[parts[0]]=i

if g.getname()[:3]!="GPC":
  g.new("Compiled " +  progname)
  GPClayer = -1
else:
  GPClayer = g.getlayer()
  g.addlayer()
  g.setname("Compiled " + progname)

g.putcells(startpat)

firstreflx, firstrefly = -1, -1
for k in range(0,numstates,2):
  g.putcells(Snark_N, 184+k*72, -20+k*56)
  g.putcells(Snark_E, -2177 + numstates*72 + len(outputdict)*16, -2369 -k*16 + numstates*72 + len(outputdict)*16)
  g.putcells(Snark_S, -7121 -k*24 - len(outputdict)*32 + len(outputdict)*16 + numstates*72, 2567 +k*8 + len(outputdict)*32 +len(outputdict)*16 + numstates*72)
  # The '72' above is mostly 64 per Z/NZ program row, but also 16 more cells diagonally for each state
  #   (there are only half as many states as rows) to leave enough space for all the reflectors at the bottom.
for i in range(numstates):
  parts = progonly[i].split("; ")
  if i%2==0:
    if parts[1]=="ZZ":
      g.putcells(onlyZ,i*64,i*64)
    else:
      g.putcells(ZNZ,i*64,i*64)
  if len(parts)==2:
    parts+=["",""]
  if parts[1]=="ZZ":
    parts = [parts[0],"Z",parts[2],parts[3]]
  actions = parts[3].split(", ")
  for j in actions:
    if j != "":
      g.putcells(splitter,-182 - outputdict[j]*64+i*64, 167 + outputdict[j]*64 + i*64)
  nextstate = parts[2]
  if nextstate != "":
    offset = statedict[nextstate]
    g.putcells(transrefl,-150 - len(outputlist)*64 + i*64 - offset*16, 165 + len(outputlist)*64 + i*64 + offset*16)

  # keep track of the placement of the first reflector, needed to place pattern correctly relative to GPC
  if firstreflx ==-1:
    firstreflx = -150 - len(outputlist)*64 + i*64 - offset*16
    firstrefly = 165 + len(outputlist)*64 + i*64 + offset*16

g.putcells(ZNZbackstop,-49 + numstates*64,-11 + numstates*64)
g.fit()

if GPClayer != -1:
  calcpat = g.getcells(g.getrect())
  g.setlayer(GPClayer)
  g.putcells(calcpat, 77924 - firstreflx, 38284 - firstrefly)  # this is the location of the key first reflector in calculator, in the GPC
  if g.getname()[:6]=="GPC-2^":
    g.setstep(int(g.getname()[6:8]))
