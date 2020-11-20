# APGsembly code emulator, version 0.5 (beta)
#   Version 0.314159+: remove phi calculator and other test programs, activate pi calculator
#   Version 0.5: add support for "ZZ" and "*" preprocessor formats, mostly copied from APGompiler.py

import golly as g
from glife.text import make_text
import types

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
program = {}
registers = {}
memory = {}
progname = "Osqrtlogt"

mullookup = {"MUL0 00000":["Z", "00000"],"MUL1 00000":["Z", "00101"],"MUL0 00001":["NZ", "00000"],"MUL1 00001":["NZ", "00101"],
	     "MUL0 00010":["Z", "00001"],"MUL1 00010":["Z", "00110"],"MUL0 00011":["NZ", "00001"],"MUL1 00011":["NZ", "00110"],
	     "MUL0 00100":["Z", "00010"],"MUL1 00100":["Z", "00111"],"MUL0 00101":["NZ", "00010"],"MUL1 00101":["NZ", "00111"],
	     "MUL0 00110":["Z", "00011"],"MUL1 00110":["Z", "01000"],"MUL0 00111":["NZ", "00011"],"MUL1 00111":["NZ", "01000"],
	     "MUL0 01000":["Z", "00100"],"MUL1 01000":["Z", "01001"],"MUL0 01001":["NZ", "00100"],"MUL1 01001":["NZ", "01001"],
	     "MUL0 01010":["Z", "00101"],"MUL1 01010":["Z", "01010"],"MUL0 01011":["NZ", "00101"],"MUL1 01011":["NZ", "01010"],
	     "MUL0 01100":["Z", "00110"],"MUL1 01100":["Z", "01011"],"MUL0 01101":["NZ", "00110"],"MUL1 01101":["NZ", "01011"],
	     "MUL0 01110":["Z", "00111"],"MUL1 01110":["Z", "01100"],"MUL0 01111":["NZ", "00111"],"MUL1 01111":["NZ", "01100"],
	     "MUL0 10000":["Z", "01000"],"MUL1 10000":["Z", "01101"],"MUL0 10001":["NZ", "01000"],"MUL1 10001":["NZ", "01101"],
	     "MUL0 10010":["Z", "01001"],"MUL1 10010":["Z", "01110"],"MUL0 10011":["NZ", "01001"],"MUL1 10011":["NZ", "01110"],
	     "MUL0 10100":["Z", "01010"],"MUL1 10100":["Z", "01111"],"MUL0 10101":["NZ", "01010"],"MUL1 10101":["NZ", "01111"],
	     "MUL0 10110":["Z", "01011"],"MUL1 10110":["Z", "00000"],"MUL0 10111":["NZ", "01011"],"MUL1 10111":["NZ", "00000"],
	     "MUL0 11000":["Z", "01100"],"MUL1 11000":["Z", "00001"],"MUL0 11001":["NZ", "01100"],"MUL1 11001":["NZ", "00001"],
	     "MUL0 11010":["Z", "01101"],"MUL1 11010":["Z", "00010"],"MUL0 11011":["NZ", "01101"],"MUL1 11011":["NZ", "00010"],
	     "MUL0 11100":["Z", "01110"],"MUL1 11100":["Z", "00011"],"MUL0 11101":["NZ", "01110"],"MUL1 11101":["NZ", "00011"],
	     "MUL0 11110":["Z", "01111"],"MUL1 11110":["Z", "00100"],"MUL0 11111":["NZ", "01111"],"MUL1 11111":["NZ", "00100"]}

addlookup = {"000 bit0 A1":["NONE","010 bit1"],"000 bit0 B1":["NZ","000 bit0"],"000 bit0 B0":["Z","000 bit0"],
	     "000 bit1 A1":["NONE","010 bit0"],"000 bit1 B1":["Z","000 bit0"],"000 bit1 B0":["NZ","000 bit0"],
	     "001 bit0 A1":["NONE","011 bit1"],"001 bit0 B1":["NZ","000 bit0"],"001 bit0 B0":["Z","000 bit0"],
	     "001 bit1 A1":["NONE","011 bit0"],"001 bit1 B1":["Z","000 bit0"],"001 bit1 B0":["NZ","000 bit0"],
	     "010 bit0 A1":["NONE","000 bit1"],"010 bit0 B1":["NZ","100 bit1"],"010 bit0 B0":["Z","000 bit0"],
	     "010 bit1 A1":["NONE","000 bit0"],"010 bit1 B1":["Z","100 bit1"],"010 bit1 B0":["NZ","000 bit0"],
	     "011 bit0 A1":["NONE","001 bit1"],"011 bit0 B1":["NZ","000 bit0"],"011 bit0 B0":["Z","100 bit1"],
	     "011 bit1 A1":["NONE","001 bit0"],"011 bit1 B1":["Z","000 bit0"],"011 bit1 B0":["NZ","100 bit1"],
	     "100 bit0 A1":["NONE","110 bit1"],"100 bit0 B1":["NZ","100 bit1"],"100 bit0 B0":["Z","000 bit0"],
	     "100 bit1 A1":["NONE","110 bit0"],"100 bit1 B1":["Z","100 bit1"],"100 bit1 B0":["NZ","000 bit0"],
	     "101 bit0 A1":["NONE","111 bit1"],"101 bit0 B1":["NZ","000 bit0"],"101 bit0 B0":["Z","100 bit1"],
	     "101 bit1 A1":["NONE","111 bit0"],"101 bit1 B1":["Z","000 bit0"],"101 bit1 B0":["NZ","100 bit1"],
	     "110 bit0 A1":["NONE","100 bit1"],"110 bit0 B1":["NZ","100 bit1"],"110 bit0 B0":["Z","100 bit1"],
	     "110 bit1 A1":["NONE","100 bit0"],"110 bit1 B1":["Z","100 bit1"],"110 bit1 B0":["NZ","100 bit1"],
	     "111 bit0 A1":["NONE","101 bit1"],"111 bit0 B1":["NZ","100 bit1"],"111 bit0 B0":["Z","100 bit1"],
	     "111 bit1 A1":["NONE","101 bit0"],"111 bit1 B1":["Z","100 bit1"],"111 bit1 B0":["NZ","100 bit1"]}

sublookup = {"000 stopper0 bit0 A1":["NONE","000 stopper1 bit1"],"000 stopper0 bit0 B0":["Z","000 stopper0 bit0"],
	     "000 stopper0 bit0 B1":["NZ","100 stopper0 bit1"],"000 stopper0 bit1 A1":["NONE","000 stopper1 bit0"],
	     "000 stopper0 bit1 B0":["NZ","000 stopper0 bit0"],"000 stopper0 bit1 B1":["Z","100 stopper0 bit1"],
	     "000 stopper1 bit0 A1":["NONE","FAILURE"],"000 stopper1 bit0 B0":["Z","000 stopper0 bit0"],
	     "000 stopper1 bit0 B1":["NZ","000 stopper0 bit0"],"000 stopper1 bit1 A1":["NONE","FAILURE"],
	     "000 stopper1 bit1 B0":["NZ","000 stopper0 bit0"],"000 stopper1 bit1 B1":["Z","000 stopper0 bit0"],
	     "001 stopper0 bit0 A1":["NONE","001 stopper1 bit1"],"001 stopper0 bit0 B0":["Z","100 stopper0 bit1"],
	     "001 stopper0 bit0 B1":["NZ","000 stopper0 bit0"],"001 stopper0 bit1 A1":["NONE","001 stopper1 bit0"],
	     "001 stopper0 bit1 B0":["NZ","100 stopper0 bit1"],"001 stopper0 bit1 B1":["Z","000 stopper0 bit0"],
	     "001 stopper1 bit0 A1":["NONE","FAILURE"],"001 stopper1 bit0 B0":["Z","000 stopper0 bit0"],
	     "001 stopper1 bit0 B1":["NZ","000 stopper0 bit0"],"001 stopper1 bit1 A1":["NONE","FAILURE"],
	     "001 stopper1 bit1 B0":["NZ","000 stopper0 bit0"],"001 stopper1 bit1 B1":["Z","000 stopper0 bit0"],
	     "010 stopper0 bit0 A1":["NONE","010 stopper1 bit1"],"010 stopper0 bit0 B0":["Z","000 stopper0 bit0"],
	     "010 stopper0 bit0 B1":["NZ","000 stopper0 bit0"],"010 stopper0 bit1 A1":["NONE","010 stopper1 bit0"],
	     "010 stopper0 bit1 B0":["NZ","000 stopper0 bit0"],"010 stopper0 bit1 B1":["Z","000 stopper0 bit0"],
	     "010 stopper1 bit0 A1":["NONE","FAILURE"],"010 stopper1 bit0 B0":["Z","000 stopper0 bit0"],
	     "010 stopper1 bit0 B1":["NZ","100 stopper0 bit1"],"010 stopper1 bit1 A1":["NONE","FAILURE"],
	     "010 stopper1 bit1 B0":["NZ","000 stopper0 bit0"],"010 stopper1 bit1 B1":["Z","100 stopper0 bit1"],
	     "011 stopper0 bit0 A1":["NONE","011 stopper1 bit1"],"011 stopper0 bit0 B0":["Z","000 stopper0 bit0"],
	     "011 stopper0 bit0 B1":["NZ","000 stopper0 bit0"],"011 stopper0 bit1 A1":["NONE","011 stopper1 bit0"],
	     "011 stopper0 bit1 B0":["NZ","000 stopper0 bit0"],"011 stopper0 bit1 B1":["Z","000 stopper0 bit0"],
	     "011 stopper1 bit0 A1":["NONE","FAILURE"],"011 stopper1 bit0 B0":["Z","100 stopper0 bit1"],
	     "011 stopper1 bit0 B1":["NZ","000 stopper0 bit0"],"011 stopper1 bit1 A1":["NONE","FAILURE"],
	     "011 stopper1 bit1 B0":["NZ","100 stopper0 bit1"],"011 stopper1 bit1 B1":["Z","000 stopper0 bit0"],
	     "100 stopper0 bit0 A1":["NONE","100 stopper1 bit1"],"100 stopper0 bit0 B0":["Z","100 stopper0 bit1"],
	     "100 stopper0 bit0 B1":["NZ","100 stopper0 bit1"],"100 stopper0 bit1 A1":["NONE","100 stopper1 bit0"],
	     "100 stopper0 bit1 B0":["NZ","100 stopper0 bit1"],"100 stopper0 bit1 B1":["Z","100 stopper0 bit1"],
	     "100 stopper1 bit0 A1":["NONE","FAILURE"],"100 stopper1 bit0 B0":["Z","000 stopper0 bit0"],
	     "100 stopper1 bit0 B1":["NZ","100 stopper0 bit1"],"100 stopper1 bit1 A1":["NONE","FAILURE"],
	     "100 stopper1 bit1 B0":["NZ","000 stopper0 bit0"],"100 stopper1 bit1 B1":["Z","100 stopper0 bit1"],
	     "101 stopper0 bit0 A1":["NONE","101 stopper1 bit1"],"101 stopper0 bit0 B0":["Z","100 stopper0 bit1"],
             "101 stopper0 bit0 B1":["NZ","100 stopper0 bit1"],"101 stopper0 bit1 A1":["NONE","101 stopper1 bit0"],
	     "101 stopper0 bit1 B0":["NZ","100 stopper0 bit1"],"101 stopper0 bit1 B1":["Z","100 stopper0 bit1"],
	     "101 stopper1 bit0 A1":["NONE","FAILURE"],"101 stopper1 bit0 B0":["Z","100 stopper0 bit1"],
	     "101 stopper1 bit0 B1":["NZ","000 stopper0 bit0"],"101 stopper1 bit1 A1":["NONE","FAILURE"],
	     "101 stopper1 bit1 B0":["NZ","100 stopper0 bit1"],"101 stopper1 bit1 B1":["Z","000 stopper0 bit0"],
	     "110 stopper0 bit0 A1":["NONE","110 stopper1 bit1"],"110 stopper0 bit0 B0":["Z","000 stopper0 bit0"],
	     "110 stopper0 bit0 B1":["NZ","100 stopper0 bit1"],"110 stopper0 bit1 A1":["NONE","110 stopper1 bit0"],
	     "110 stopper0 bit1 B0":["NZ","000 stopper0 bit0"],"110 stopper0 bit1 B1":["Z","100 stopper0 bit1"],
	     "110 stopper1 bit0 A1":["NONE","FAILURE"],"110 stopper1 bit0 B0":["Z","100 stopper0 bit1"],
	     "110 stopper1 bit0 B1":["NZ","100 stopper0 bit1"],"110 stopper1 bit1 A1":["NONE","FAILURE"],
	     "110 stopper1 bit1 B0":["NZ","100 stopper0 bit1"],"110 stopper1 bit1 B1":["Z","100 stopper0 bit1"],
	     "111 stopper0 bit0 A1":["NONE","111 stopper1 bit1"],"111 stopper0 bit0 B0":["Z","100 stopper0 bit1"],
	     "111 stopper0 bit0 B1":["NZ","000 stopper0 bit0"],"111 stopper0 bit1 A1":["NONE","111 stopper1 bit0"],
	     "111 stopper0 bit1 B0":["NZ","100 stopper0 bit1"],"111 stopper0 bit1 B1":["Z","000 stopper0 bit0"],
	     "111 stopper1 bit0 A1":["NONE","FAILURE"],"111 stopper1 bit0 B0":["Z","100 stopper0 bit1"],
	     "111 stopper1 bit0 B1":["NZ","100 stopper0 bit1"],"111 stopper1 bit1 A1":["NONE","FAILURE"],
             "111 stopper1 bit1 B0":["NZ","100 stopper0 bit1"],"111 stopper1 bit1 B1":["Z","100 stopper0 bit1"]}


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
          # in the line below, there's no .replace("; ZZ;","; Z;") in the compiler version,
          #    because we need to know whether to use ZNZ or onlyZ component...
          progonly += [Zline.replace("; ZZ;","; Z;"), Zparts[0]+"; NZ"]  
          Zline = line
          NZflag = 1
        else:
          g.note("Pre-processing failed on lines:\n" + Zline + "\n" + line + "\nNeed a Z and NZ line for each state, or * / ZZ syntax.")
          g.exit()

g.new(progname)
g.setcell(0,0,1)
g.fit()
g.setcell(0,0,0)
g.update()
runflag = 0

def check_keyboard():
  global runflag
  while 1:
    evt = g.getevent()
    if evt !="":
      g.show(state + " -- " + nextstate + " :: " + instr + "; regs=" + str(registers)  + " -- 'r' to toggle run mode, any key to step")
    if evt == "key q none":
      g.setclipstr(s)
      g.exit()
    if evt == "key r none":
      runflag = 1-runflag
    elif evt=="key g none":
      break
    else:
      g.doevent(evt)
    if runflag == 1:
      break

# every state has a Z and NZ jump instruction to following states,
#   so the order of the program lines doesn't really matter.
#   Turn the program into a dictionary.
for item in progonly:
   fourparts = item.replace(", ",",").split("; ") 
   if len(fourparts) != 4:
      if len(fourparts) == 2:
         # this is probably an auto-generated line for a state+Z/NZ combination that will never be reached
         # ... so we'll try including it with empty jump and action values, and just see if it works.
         fourparts += ["none",""]
      else:
         g.note("Failed to parse: " + item)
         g.exit()
   label, bitval, nextstate, instr = fourparts
   program[label+";"+bitval]=[nextstate,instr]

state, nextstate, nextoutput, outputtext = "START","INITIAL","Z",""

g.show(state + " -- " + nextstate + " :: " + instr + "; regs=" + str(registers)  + " -- 'r' to toggle run mode, any key to step")

check_keyboard()

while 1:

   if nextoutput == "":
      g.show(state + " -- " + nextstate + " :: " + instr + "; regs=" + str(registers)  + "; mem=" + str(memory))
      g.note("Program reached halt state (because no bit value was returned by any instruction).")
      g.setclipstr(s)
      g.exit()
   
   state = nextstate + ";" + nextoutput
   # get info from program dictionary, move to next state
   nextstate, instr = program[state]

   # process instructions for current state
   # -- there may be just one instruction,
   #    or several comma-separated instructions
   nextoutput = ""  # if some instruction doesn't set this variable, the program will halt
   for i in instr.split(","):
     # allow stepping or full-speed run from keyboard (toggle "r")
     check_keyboard()

     if i == "NOP":
       nextoutput = "Z"

     elif i == "READ SQ":
       if "SQX" not in registers: registers["SQX"], registers["SQY"]=0,0  # initialize if necessary
       coord = str(registers["SQX"]) +","+str(registers["SQY"])
       if coord not in memory:
         memory[coord]=0
       if memory[coord]==0:
         nextoutput = "Z"
       else:
         nextoutput = "NZ"
         memory[coord] = 0  # this is a destructive read operation
         g.setcell(registers["SQX"]-registers["SQY"],-registers["SQX"]-registers["SQY"],memory[coord])
         g.update()

     elif i == "SET SQ":
       if coord not in memory:
         memory[coord]=0
       if memory[coord]==0:
         memory[coord] = 1
         g.setcell(registers["SQX"]-registers["SQY"],-registers["SQX"]-registers["SQY"],memory[coord])
         g.update()
       else:
         g.note("PROGRAM ERROR:\nTried to set memory coordinate " + coord + "to 1,\nwhen it was already 1.")
         g.exit()

     elif i[:4]=="INC ":
       reg = i.split(" ")[1]
       if reg not in registers:
         if reg[:1]=="T": # binary register
           registers[reg]=[0,"0"]
         else:
           registers[reg]=0 # simple register
       if isinstance(registers[reg], types.ListType): # binary register
         ptr,bits = registers[reg]
         if ptr == len(bits)-1:
           bits+="0"         # the mechanism automatically adds a zero when INCing past current end of tape
           nextoutput = "Z"  # ... and it returns a zero output in that case
         else:
           nextoutput = "NZ" # if it's not creating a new bit, it returns an NZ output.  TODO: what does the program use this for?
         registers[reg] = [ptr+1,bits]
       else:
         registers[reg] += 1  # simple register

     elif i[:5]=="TDEC " or i[:6]=="DEC SQ": # simple register
       reg = i.split(" ")[1]
       if reg not in registers:
         registers[reg]=0
       if registers[reg] == 0:
         nextoutput = "Z" # don't update register, it's already zero
       else:
         registers[reg] -= 1
         nextoutput = "NZ"

     elif i[:4]=="DEC ": # binary register
       reg = i.split(" ")[1]
       ptr,bits = registers[reg]
       if ptr == 0:
         nextoutput = "Z" # don't update register, it's already zero
       else:
         registers[reg] = [ptr-1,bits]
         nextoutput = "NZ"    

     elif i=="HALT":
       g.note("Program reached halt state.")
       g.setclipstr(s)
       g.exit()

     elif i[:4]=="MUL ":
       bit = str(i[4:])
       if "MUL" not in registers:
         registers["MUL"]="00000"
       nextoutput, registers["MUL"] = mullookup["MUL" + bit + " " + registers["MUL"]]

     elif i[:7] == "OUTPUT ":
       outputtext += i[7:]
       outpat = make_text(outputtext)
       g.putcells(outpat, 0, 10)
       g.update()

     elif i[:4]=="SUB ":
       if "SUB" not in registers:
         registers["SUB"]="000 stopper0 bit0"
       whichinput = i[4:]
       out, registers["SUB"] = sublookup[registers["SUB"] + " " + whichinput]
       if registers["SUB"] == "FAILURE":
         g.note("Program crashed at line '" + i + "'.  SUB A1 must have been run twice (?).")
         g.exit()
       if out != "NONE":
         nextoutput = out

     elif i[:4]=="ADD ":
       if "ADD" not in registers:
         registers["ADD"]="000 bit0"
       whichinput = i[4:]
       temp = registers["ADD"] + " " + whichinput
       out, registers["ADD"] = addlookup[temp]
       if out != "NONE":
         nextoutput = out

     elif i[:5]=="READ ":
       binregname = i[5:] # TODO: maybe be consistent and use .split()?
       if binregname not in registers:
         registers[binregname]=[0,"0"]
       ptr, bits = registers[binregname]
       if bits[ptr]=="x":
         g.note("Program crashed on instruction '" + i + "':\n attempt to read an empty position in a binary register.")
         g.exit()
       elif bits[ptr]=="0":
         nextoutput = "Z"
       elif bits[ptr]=="1":
         nextoutput = "NZ"
       else:
         g.note("Emulator error. Found value '" + bits[ptr] + "' on READ, in " + binregname + " bitstring -- " + str(registers[binregname]) + ".")
         g.exit()
       registers[binregname] = [ptr, bits[:ptr]+"x"+bits[ptr+1:]]

     elif i[:4]=="SET ":
       binregname = i[4:]
       if binregname not in registers:
         registers[binregname]=[0,"0"]
       ptr, bits = registers[binregname]
       if bits[ptr]!="x":
         g.note("Crash. Found value '" + bits[ptr] + "' on SET, in " + binregname + " bitstring -- " + str(registers[binregname]) + ".")
         g.exit()
       registers[binregname] = [ptr, bits[:ptr]+"1"+bits[ptr+1:]]

     elif i[:6]=="RESET ":
       binregname = i[6:]
       if binregname not in registers:
         registers[binregname]=[0,"0"]
       else:
         ptr, bits = registers[binregname]
       if bits[ptr]!="x":
         g.note("Crash. Found value '" + bits[ptr] + "' on READ, in " + binregname + " bitstring -- " + str(registers[binregname]) + ".")
         g.exit()
       registers[binregname] = [ptr, bits[:ptr]+"0"+bits[ptr+1:]]

     else:
       g.note("Unknown instruction: " + instr + " -- ~" + i + "~")
       g.exit()

