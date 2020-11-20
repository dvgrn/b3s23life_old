# BatchRuleTableToTree.py
# modified version of RuleTableToTree.py,
#   intended to create a version of any @TABLE .rule file that can be copied
#   directly into the LifeWiki Rule: namespace for LifeViewer to use
# This involves adding a @TREE section that contains an equivalent encoding of the @TABLE section
# Version 2: process all rules from a text list, instead of one at a time from clipboard or file
# Version 3: just do the .table to .tree conversion, not .rule to .rule
# Version 4: revert to doing .rule to .rule, allow time limit for rule load and conversion, output log file

import golly
import os
import time
import datetime
import shutil
from glife.ReadRuleTable import *
from glife.RuleTree import *
from glife.EmulateTriangular import *
from glife.EmulateMargolus import *
from glife.EmulateOneDimensional import *
from glife.EmulateHexagonal import *

# configuration
rulefilenames = "batchinput.txt" # set this to "PROMPT" to have Golly use a file selector
reportfile = "reportfile.txt"
outfolder = "BatchOutput/"
loadtimelimit = 120 # loading rule time limit in seconds: set to 0 for unlimited
proctimelimit = 1800 # processing rule time limit in seconds: set to 0 for unlimited

# statistics
n_rules = 0
n_ok = 0
n_loadtimeout = 0
n_proctimeout = 0
n_error = 0
n_name = 0
n_copy = 0

if rulefilenames == "PROMPT":
  rulefilenames = golly.opendialog('Open a newline-delimited list of .table filenames (with paths)', 'Text files (*.txt)|*.txt')
  if len(rulefilenames) == 0: golly.exit()    # user hit Cancel

with open(rulefilenames, "r") as f:
  rulefileslist = f.readlines()

# add new converters here as they become available:
Converters = {
    "vonNeumann":ConvertRuleTableTransitionsToRuleTree,
    "Moore":ConvertRuleTableTransitionsToRuleTree,
    "triangularVonNeumann":EmulateTriangular,
    "triangularMoore":EmulateTriangular,
    "Margolus":EmulateMargolus,
    "square4_figure8v":EmulateMargolus,
    "square4_figure8h":EmulateMargolus,
    "square4_cyclic":EmulateMargolus,
    "oneDimensional":EmulateOneDimensional,
    "hexagonal":EmulateHexagonal,
}

# time batch processing
totaltime = time.time()

# open report file for write and output header
e = open(reportfile, "w")
e.write("Batch started at "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+"\n")
e.write("Using input file: "+rulefilenames+" containing "+str(len(rulefileslist))+" rules\n")
e.write("Load time limit: ")
if loadtimelimit == 0:
  e.write(" unlimited")
else:
  e.write(str(loadtimelimit) + " seconds")
e.write("\nProcessing time limit: ")
if proctimelimit == 0:
  e.write(" unlimited")
else:
  e.write(str(proctimelimit) + " seconds")
e.write('\n\nTime\tStatus\tFile\n')

# process each rule in the rule list
status = "OK"
for item in rulefileslist:
  elapsed = "[00:00]"
  rulefilename = item.replace("\n", "")
  with open(rulefilename,"r") as f:
    rulelines = f.readlines()

  # create the output file name from the input file name
  filename = rulefilename.replace(".rule",".table")
  if rulefilename == filename:
    # input must end in .rule
    status = "NAME"
    message = "Input file must be called *.rule"
    n_name = n_name + 1
  else:
    # process input file
    with open(filename,"w") as f1:
      export = 0
      for line in rulelines:
        if line[:5] == "@TREE":
          status = "COPY"
          message = "Already has a @TREE section."
          n_copy = n_copy + 1
          export = -1
          break
        if export != 1:
          if line[:6] == "@TABLE":
            export = 1
        else:       
          if line[:1] == "@":
            export = 2
          else:
            f1.write(line)
    if export == -1:
      # rule already constants @TREE so copy the rule to the output folder
      shutil.copy(rulefilename, outfolder)
    else:
      # attempt to read the rule
      readtime = time.time()
      n_states, neighborhood, transitions, message = ReadRuleTable(filename, loadtimelimit)
      seconds = time.time() - readtime
  
      # check if read was successful
      if n_states == -1:
        # check if read timed out
        if message == "Exceeded loading time limit":
          message = message+" ("+str(loadtimelimit)+" seconds)."
          elapsed = "[{0:02d}:{1:02d}]".format(int(seconds/60),int(seconds%60))
          status = "LOAD"
          n_loadtimeout = n_loadtimeout + 1
        else:
          status = "ERROR"
          n_error = n_error + 1
      else:
        # check if we have a converter for the rule's neighborhood
        if not neighborhood in Converters:
          status = "ERROR"
          message = "Unsupported neighborhood: "+neighborhood+"."
          n_error = n_error + 1
        else:
          # time the converter
          starttime = time.time()
          timeout = 0

          # all converters now create a .rule file
          if neighborhood == "vonNeumann" or neighborhood == "Moore":
            # for VN or Moore run the converter with a time limit
            rule_name, timeout = Converters[neighborhood]( neighborhood,
                                                n_states,
                                                transitions,
                                                filename,
                                                proctimelimit )
          else:
            rule_name = Converters[neighborhood]( neighborhood,
                                                n_states,
                                                transitions,
                                              filename )

          # get elapsed time     
          seconds = time.time() - starttime
          elapsed = "[{0:02d}:{1:02d}]".format(int(seconds/60),int(seconds%60))

          # check if the processing time exceeded the limit
          if timeout > 0:
            status = "PROC"
            message = "Exceeded processing time limit ("+str(proctimelimit)+" seconds)."
            n_proctimeout = n_proctimeout + 1
          else:
            # processing successful
            status = "OK"
            n_ok = n_ok + 1
            golly.new(rule_name+'-demo.rle')
            golly.setalgo('RuleLoader')
        
            # now go find the rule just created
            newrulefilename = golly.getdir('rules')+rule_name+".rule"
            with open(newrulefilename,"r") as f2:
              treelines = f2.readlines()
      
            # rewrite the rule file to include a @TABLE as well as a @TREE section 
            with open(os.path.join(outfolder, rule_name + ".rule"),"w") as f3:
              wrotetree = 0
              for line in rulelines:
                if wrotetree == 0:
                  if line[:6] == "@TABLE":
                    foundtree = 0
                    for treeline in treelines:
                      if treeline[:5] == "@TREE":
                        foundtree=1
                      if foundtree==1:
                        f3.write(treeline)
                    wrotetree = 1
                    f3.write("\n")
                  f3.write(line)
                else:
                  f3.write(line)

    # delete .table file
    try:
      os.remove(filename)
    except WindowsError:
      e.write("Warning: Could not delete "+filename+"\n")

  # add entry in the log file and flush it so it's up to date if there is a crash
  e.write(elapsed+'\t'+status+'\t'+rulefilename+'\t'+message+'\n')
  e.flush()

# batch finished so compute total time and create summary line
seconds = time.time() - totaltime
elapsed = "[{0:02d}:{1:02d}]".format(int(seconds/60),int(seconds%60))
summary1 = "Batch completed at "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+" "+elapsed
summary2 = "Batch completed in "+elapsed
summary3 = "OK: "+str(n_ok)+"    COPY: "+str(n_copy)+"    ERROR: "+str(n_error)+"    NAME: "+str(n_name)+"    LOAD: "+str(n_loadtimeout)+"    PROC: "+str(n_proctimeout)

# display the summary and add to the log file
e.write("\n"+summary1+"\n"+summary3+"\n\n")
golly.show(summary2+"   "+summary3+"    Log file: "+reportfile)

# close log file and exit
e.close()
