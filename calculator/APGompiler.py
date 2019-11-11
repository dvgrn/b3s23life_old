# APGompiler.py, version 0.4 (Osqrtlogt test)

import golly as g

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

ZNZstopper = g.parse("2o126b2o$o127bo$b3o125b3o$3bo127bo!")

startpat = g.parse("bo$2bo$3o4$22bo$20b3o$19bo$19b2o$25bo$23b3o$22bo$15bo6b2o$14bobo$14b2o!",-5,33)

APGsembly = """INITIAL; Z; A1; READ SQ
INITIAL; NZ; A1; READ SQ
A1; Z; B1; SET SQ, NOP
A1; NZ; C1; NOP
B1; Z; B2; DEC SQX
B1; NZ; B2; DEC SQX
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
C1; Z; C2; TDEC R0
C1; NZ; C2; TDEC R0
C2; Z; C4; DEC SQX
C2; NZ; C3; INC SQX, NOP
C3; Z; A1; READ SQ
C3; NZ; A1; READ SQ
C4; Z; C5; INC SQY, INC R1, NOP
C4; NZ; C4; DEC SQX
C5; Z; C6; TDEC R1
C5; NZ; C6; TDEC R1
C6; Z; C7; TDEC R2
C6; NZ; C6; INC R2, TDEC R1
C7; Z; A1; READ SQ
C7; NZ; C7; INC R0, INC R1, TDEC R2"""
progname = "Osqrtlogt"

proglines = APGsembly.split('\n')
numstates = len(proglines)
statedict = {}
for i in range(0,numstates,2):
  parts = proglines[i].split("; ")
  statedict[parts[0]]=i

g.new("Compiled " +  progname)
g.putcells(startpat)

for k in range(0,numstates,2):
  g.putcells(Snark_N, 184+k*72, -20+k*56)
  g.putcells(Snark_E, 27323 - 24400 + numstates*64, 21147 - 24400 +5984 -k*16 + numstates*64)
  g.putcells(Snark_S, 14235 - 832 +8976 -24400 -k*24 - len(outputdict)*32 + numstates*64, 34227 + 832 -2992 - 24400 +k*8 + len(outputdict)*32 + numstates*64)
for i in range(numstates):
  if i%2==0:
    g.putcells(ZNZ,i*64,i*64)
  parts = proglines[i].split("; ")
  actions = parts[3].split(", ")
  for j in actions:
    g.putcells(splitter,-182 - outputdict[j]*64+i*64, 167 + outputdict[j]*64 + i*64)
  nextstate = parts[2]
  offset = statedict[nextstate]
  
  g.putcells(transrefl,-150 - len(outputlist)*64 + i*64 - offset*16, 165 + len(outputlist)*64 + i*64 + offset*16)

g.putcells(ZNZstopper,-9 + numstates*64,29 + numstates*64)
g.fit()
