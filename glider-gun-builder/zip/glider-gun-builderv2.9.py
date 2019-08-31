# glider-gun-builderv2.9.py
#
# INSTRUCTIONS
#
# --- Quick Reference ---
# 1) Everything from https://github.com/ceebo/glider_guns goes in "glider_guns-master" folder
# 2) When a new template is needed, it goes in the "template" folder
# 3) If a specific adjustment needs a weld or other customization at adjustment N,
#       the custom-built gun also goes in the "template" folder with the suffix "altN".
# 4) If a gun of a specific subperiod requires a different shape (e.g., for glider crossings to work)
#       than the base period gun, then the adjusted gun should be placed in "template/specialcases".
#
# Note:  The g.setrule("LifeHistoryToLife") calls will fail unless ToLife.lua has been run
#        at least once on a LifeHistory pattern, to generate the rule table file.
#
# --- Longer Instructions --
# This script is intended for use with the pattern archive at https://github.com/ceebo/glider_guns .
# Based on the variable-period guns in the "variable" folder, it will build guns of specific periods,
#   following the information found in README.md.
# To make this possible, it is necessary to mark each variable gun to show
#   1) where input signals should be added (yellow state 5, often a Herschel or glider but not always)
#   2) what part of the gun should be adjusted (white state 3, marking all cells that should move)
#   3) where the output of the gun should be expected (red state 4, should be on a bounding box edge)
#   4) if there are temporary edge sparks in the fixed part of the gun, the row or column reached
#        (blue state 2, one cell, should be somewhere out of the way on the correct row or column)
#   5) if there are temporary edge sparks in the movable part of the gun, the row or column reached
#        (gray state 6, one cell, should be somewhere out of the way on the correct row or column)
#   The last two colors are only necessary when there are no permanent ON cells marking the
#      edge of the gun's LifeHistory bounding box.
#
# These template guns are saved in a folder named "template".
# The filenames of these template guns include some extra information:
#  -- the direction of adjustment for the movable part of the gun -- DX,DY;
#  -- the number of ticks to advance after placing input signals, to reach the output location
# This last is necessary because the input location is assumed to be in the stationary part
#   of the gun, along with the output.  In other words, input and output locations are not
#   changed when the gun is adjusted to a new period.  So in some cases, if the active signal
#   is in fact somewhere in the adjustable part of the gun when a glider escapes from the
#   bounding box, then it is necessary to "rewind" that signal by N ticks until it is in the
#   stationary part, then give OFFSET=N in the filename:
#
#   p{5-digit period with leading zeroes},DX,DY,OFFSET.rle
#
# In some situations, the early adjustments to a gun contain pieces that are too close to each other
#   that have to be custom-welded to avoid catastrophic explosions.  This must be done separately
#   for each individual situation, with the resulting gun saved as a separate template.  Filename:
#
#   p000{period}alt{adjustment_distance},0,0,OFFSET.rle
#
# Notice that no DX or DY is needed, because with welded components no adjustment is possible.
#
# The adjustability only works for simple linear displacements.  All guns with complex adjustability
#   must have an "alt" template pattern custom-adjusted for each required spacing.
#
# In rare cases, a gun with multiple signals in a loop will require a slightly different (larger)
#   shape than the base gun with only a single signal, to avoid conflicts between the signals.
#   Another situation that requires the use of the specialcase folder is when an adjustment causes
#   the gun bounding box to become taller than it is wide, as in p00590x3_7,0,0,0.rle.
#
#   In these cases, a pattern should be added to the "specialcases" subfolder of the template folder.
#   The filename should match the requested adjustment in the README.  For example, there's a
#   period 762+8*4 = p794 gun that does not work at period 397 because of signal collisions.  So
#   a custom-adjusted "p00762_4_p00397,0,0,0.rle" gun has been added to the "specialcases" folder.
#   The README line for this gun reads "397 (5762, 'p00762_4_p00397')", matching up to the comma.
#
#   Another special case is when a periodic period multiplier prevents a gun's signals from being
#   loaded correctly:  starting with an empty gun, loading a signal every p ticks would cause the
#   final pattern's period multiplier to be out of alignment with the phase of the multiplier
#   that actually uses the required spark.  In this case, append the suffix "_fixed_{period}"
#   to the pattern, and include the LifeHistory version of the full gun in the "specialcases" folder.
#
# TODO: Adjust specialcases guns so they don't need the ",0,0,0" suffix

import golly as g
import os, sys
from os import listdir
from os.path import isfile, join

def outputmatch(outputcells):
  outputmatchflag=1
  for outcell in range(0,len(outputcells),3):
    if g.getcell(outputcells[outcell],outputcells[outcell+1])!=1:
      outputmatchflag=0
      break
  return outputmatchflag

# __file__ not available in Golly?
# scriptpath = os.path.dirname(os.path.abspath( __file__ ))
scriptpath =  os.path.realpath(os.path.dirname(sys.argv[0]))
outfolder = os.path.join(scriptpath, "guns")
LHoutfolder = os.path.join(scriptpath, "LHguns")
infolder = os.path.join(scriptpath, "template")
specialfolder = os.path.join(scriptpath,"template", "specialcases")
fixedfolder = os.path.join(scriptpath,"glider_guns-master", "fixed")
vargunfolder = os.path.join(scriptpath,"glider_guns-master", "variable")
readmefolder = os.path.join(scriptpath,"glider_guns-master")

if not os.path.exists(outfolder): os.makedirs(outfolder)
if not os.path.exists(LHoutfolder): os.makedirs(LHoutfolder)

onlyfiles = [f for f in listdir(infolder) if isfile(os.path.join(infolder, f))]
baseguns=dict()
for file in onlyfiles:
  name, dx, dy, offset = file[:-4].split(",")  # remove '.rle'
  baseguns[name]=[g.load(os.path.join(infolder, file)),int(dx), int(dy), int(offset)]
specialguns=dict()
specialfiles = [f for f in listdir(specialfolder) if isfile(os.path.join(specialfolder, f))]
for file in specialfiles:  # these are not adjustable guns and are saved in final form,
                           # so no need for dx, dy, or offset
  name, dx, dy, offset = file[:-4].split(",")  # remove '.rle'
  specialguns[name]=[g.load(os.path.join(specialfolder, file)),int(dx), int(dy), int(offset)]
g.addlayer()

with open(os.path.join(readmefolder, "README"), "r") as f:
  readme = f.readlines()
  
gunlistbegin, gunlistend = 0,0
for i in range(len(readme)):
  if readme[i]=="Gun List\n":
    gunlistbegin=i+2
  elif readme[i]=="Stats\n":
    gunlistend = i-2
    break
readmelist = readme[gunlistbegin:gunlistend]
# readmelist = [] ############################# temporarily disable gun building
warnings = ""
countbuilt, countfixed, countspecial, countvar0, countconfirmed = 0, 0, 0, 0, 0
for item in readmelist:
  period, size, basegun = item.replace("\n","").split(" ")
  basegun=basegun.replace("'","").replace(")","")
  bb, usebb = [],0
  # g.note(str([basegun+"_special_p" + ("0000"+period)[-5:], (basegun+"_special_p" + ("0000"+period)[-5:] in specialguns)]))
  if basegun=="fixed" or basegun+"_special_p" + ("0000"+period)[-5:] in specialguns:
    if basegun=="fixed":
      fixedname="p"+("0000"+period)[-5:]
      folder = fixedfolder
    else:
      # g.note(basegun) #################
      fixedname = basegun+"_special_p" + ("0000"+period)[-5:]+",0,0,0"
      folder = specialfolder
    g.open(os.path.join(folder, fixedname+".rle"))
    bb=g.getrect()
    usebb=1
    g.setrule("LifeHistoryToLife")
    g.run(1)
    g.setrule("Life")
    if basegun=="fixed":
      g.save(os.path.join(outfolder,fixedname)+"_fixed.rle","rle")
      g.show("[fixed]")
      countfixed+=1
    else:
      g.save(os.path.join(outfolder,"p"+("0000"+period)[-5:]+"_custom")+".rle","rle")
      countspecial+=1
    r=g.getrect()
  else:
    datalist = basegun.split("_")
    if len(datalist)==2:
      baseperiod, adjustment = datalist
    else:
      baseperiod, adjustment, finalperiod = datalist
    subperiod = 1 # this should probably really be called the "period multiplier" or some such -- it's for when you add a semi-Snark, etc.
    temp = baseperiod.split('x')
    if len(temp)==2:
      subperiod = int(temp[1])
    iperiod,  iadjustment = int(period), int(adjustment)
    if baseperiod+"alt"+adjustment in baseguns:
      baseperiod+="alt"+adjustment
      iadjustment=0 # weld has already been done at specific adjustment
    if baseperiod not in baseguns:
      if iadjustment==0:
        # we have no template pattern, but presumably we have the one gun in the variable folder, anyway
        countvar0+=1
        g.open(os.path.join(vargunfolder, baseperiod+".rle"))
        bb=g.getrect()
        usebb=1
        g.setrule("LifeHistoryToLife")
        g.run(1)
        g.setrule("Life")
        variablegunname="p"+("0000"+period)[-5:]
        # we would still have to fill in multiple signals for cases where that's needed
        #        (i.e., where len(temp)==2, where there's an 'x' in the name)
        flag="_NEEDS_TEMPLATE_"+basegun if len(temp)==2 else "" # these all actually have templates now (5/20/2018)
        g.save(os.path.join(outfolder,variablegunname)+"_0"+flag+".rle","rle")
      continue
    else:  # there's a matching adjustable gun in the template folder.

      basepat, dx, dy, finaladjustment = specialguns[basegun] if basegun in specialguns else baseguns[baseperiod]
      fixedpat, movablepat, fixedbb, movablebb, output, signal=[],[],[],[],[],[]
      for i in range(0,len(basepat)-1,3):
        cellcolor = basepat[i+2]
        if cellcolor==1:
          fixedpat+=basepat[i:i+3]
        elif cellcolor==2:
          fixedbb+=basepat[i:i+2]+[1]
        elif cellcolor==3:
          movablepat+=basepat[i:i+2]+[1]
        elif cellcolor==4:
          output+=basepat[i:i+2]+[0]
        elif cellcolor==5:
          signal+=basepat[i:i+2]+[1]
        elif cellcolor==6:
          movablebb+=basepat[i:i+2]+[1]
        else:
          g.exit("Don't know that color: "+str(basepat[i+2]))
      errorstr = ""
      if len(fixedpat) == 0: errorstr += "fixed pattern (state 1, green) "
      if len(movablepat) == 0: errorstr += "movable pattern (state 3, white) "
      if len(output) == 0: errorstr += "output pattern (state 4, red) "
      if len(signal) == 0: errorstr += "signal pattern (state 5, yellow) "
      if errorstr != "":
        g.warn("Required cell states -- " +errorstr \
               + "-- not found in " + basegun + " template pattern:\n" + item)
      if len(fixedpat)%2 == 0: fixedpat+=[0]
      if len(movablepat)%2 == 0: movablepat+=[0]
      if len(fixedbb)%2 == 0 : fixedbb+=[0]
      if len(movablebb)%2 == 0 : movablebb+=[0]
      if len(output)%2 == 0: output+=[0]
      if len(signal)%2 == 0: signal+=[0]
      g.new(basegun)
      g.putcells(fixedpat)
      g.putcells(fixedbb)
      g.putcells(movablepat, iadjustment*dx, iadjustment*dy)
      g.putcells(movablebb, iadjustment*dx, iadjustment*dy)
      done = 0
      g.setrule("Life")
      r=g.getrect()
      while done == 0:
        g.putcells(signal)
        g.run(iperiod/subperiod)
        g.fit()
        g.update()
        if g.getcell(signal[0],signal[1])==1: done=1
      g.run(finaladjustment)
      g.run(100*iperiod/subperiod)
      if subperiod>1 and outputmatch(output)!=1:
        countdown=subperiod
        g.setgen("0")
        while countdown>=0:
          countdown-=1
          g.run(iperiod/subperiod)
          if outputmatch(output)==1:
            break
      if outputmatch(output)!=1:
        g.exit("Looks like something went wrong at period " + period \
             + ".  Output is not showing up after any reasonable number of subperiod cycles.")
      g.select(r)
      g.clear(1)
      g.select([])
      g.setgen("0")
      g.show("Done!  "+ os.path.join(outfolder,str(period)))
      g.putcells(fixedbb)
      g.putcells(movablebb, iadjustment*dx, iadjustment*dy)
      g.save(os.path.join(outfolder,"p"+str(iperiod+100000)[1:]+"_"+basegun+".rle"),"rle")
      countbuilt+=1

  #check we get the expected size
  if usebb==1: r = bb  # guns not built from template should use their LifeHistory bounds
  size = int(size.replace(",","").replace("(",""))
  if r[2]<r[3]:
    warnings+="\nbad orientation " + item
  if r[2] * r[3] != size:
    warnings+="\nbad size " + item.replace("\n","") + ": really "+str(r[2]*r[3])
  maxx = r[0] + r[2]
  maxy = r[1] + r[3]

  #bbox should increase in the south or east
  g.run(1)
  r = g.getrect()
  if r[0] + r[2] <= maxx and r[1] + r[3] <= maxy:
    warnings+="\nno escape " + item

gunfiles = [f for f in listdir(outfolder) if isfile(os.path.join(outfolder, f))]
perioddict=dict()
mismatchreport=""
for item in gunfiles:
  p = int(item[1:6])
  perioddict[p]=item

  if item.find("_fixed")>-1:
    # have to re-open original LifeHistory pattern to get the right bounding box
    g.open(os.path.join(fixedfolder,item.replace("_fixed","")))
    r=g.getrect()
    g.select(r)
    g.duplicate()
    g.setrule("LifeHistoryToLife")
    g.run(1)
    g.setrule("B3/S23")
    g.setgen("0")
    originalONcells = g.getcells(r)
    g.dellayer()
    if g.getrule()!="LifeHistory": g.exit("Uh-oh.") # should already be for this layer
    # The above assumes that fixed guns' LifeHistory envelopes are correct.
    # TODO: check this?
    # going to assume no bounding-box-marker sparks in the fixed guns
    gunpat = str(g.getcells(r))
    cycles=13 # we don't have any pseudoperiod guns with a factor more than 12, do we?
    while cycles>0:
      g.show("LifeHistorifizing period " + str(p) + ", trial #" + str(21-cycles))
      cycles-=1
      g.run(p)
      newgunpat = str(g.getcells(r))
      if gunpat == newgunpat: # this checks LifeHistory cells also
        break
    g.clear(1)
    g.setgen("0")    
    g.save(os.path.join(LHoutfolder,item),"rle")
    if g.getrule()!="LifeHistory": g.exit("Uh-oh 2.") # should already be for this layer
    g.setrule("LifeHistoryToLife")
    g.run(1)
    g.setrule("B3/S23")
    g.putcells(originalONcells, 0, 0, 1, 0, 0, 1, "xor")
    if cycles==0 or g.getpop()!="0":
      mismatchreport+="Fixed-gun LifeHistory mismatch found at period " + str(p) + "-- Cycles: "+str(cycles)+", pop = "+g.getpop()+"\n"
      # if cycles==0 and g.getpop()=="0":
      # #  This is most often due to a single missing state-2 cell just in front of the output glider
      # #  TODO:  catch this case and dispose of it without unnecessary warning messages
      #   g.setclipstr(str([gunpat, newgunpat]))
      #   g.exit() #################################3
  else: # not a fixed gun, therefore a gun built from a template
    g.open(os.path.join(outfolder,item))
    r = g.getrect()
    g.select(r)
    g.run(p)  # get rid of bounding-box marker sparks first
    g.setrule("LifeHistory")
    # there are no pseudo-period template guns, so one cycle should be enough
    g.run(p)
    originalONcells = g.getcells(r)
    g.run(p)
    g.clear(1)
    g.setgen("0")    
    g.save(os.path.join(LHoutfolder,item),"rle")
    if str(originalONcells)!=str(g.getcells(r)):
      mismatchreport+="Template gun LifeHistory mismatch found at period " + str(p) + " after one cycle and two cycles.\n"

missinggunreport=""
for i in range(14, 1025):
  if i not in perioddict:
    missinggunreport+="Missing gun with period " + str(i) + "\n"

outmsg = "Done." if warnings=="" else "Done.  Errors:\n" + warnings
outmsg += "\nGuns built=" + str(countbuilt) \
       + ", fixed=" + str(countfixed) \
       + ", special=" +str(countspecial) \
       + ", from var folder=" + str(countvar0) \
       + "\n -- total=" + str(countbuilt + countfixed + countspecial + countvar0)
if missinggunreport!="":
  outmsg+="\n"+missinggunreport
if mismatchreport!="":
  outmsg+="\n"+mismatchreport
g.show("Processing complete.")
g.setclipstr(outmsg)
g.note(outmsg)