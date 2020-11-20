# RuleTableToTree-hacked3.py
# modified version of RuleTableToTree.py,
#   intended to create a version of any @TABLE .rule file that can be copied
#   directly into the LifeWiki Rule: namespace for LifeViewer to use
# This involves adding a @TREE section that contains an equivalent encoding of the @TABLE section
# Version 2: process all rules from a text list, instead of one at a time from clipboard or file
# Version 3: just do the .table to .tree conversion, not .rule to .rule

import golly
import os
from glife.ReadRuleTable import *
from glife.RuleTree import *
from glife.EmulateTriangular import *
from glife.EmulateMargolus import *
from glife.EmulateOneDimensional import *
from glife.EmulateHexagonal import *

rulefilenames = "C:/PUT/YOUR/FILE/PATH/HERE/tablelist.txt"
reportfile = "C:/PUT/YOUR/LOG/FILE/PATH/HERE/errorreportfile.txt"
outfolder = "C:/PUT/YOUR/FOLDER/PATH/HERE/outtrees/"

if rulefilenames == "C:/PUT/YOUR/FILE/PATH/HERE.txt":
  rulefilenames = golly.opendialog('Open a newline-delimited list of .table filenames (with paths)', 'Text files (*.txt)|*.txt')
  if len(rulefilenames) == 0: golly.exit()    # user hit Cancel

with open(rulefilenames, "r") as f:
  rulefileslist = f.readlines()

for item in rulefileslist:
  # do rule @TREE creation for each item in rule list
  filename = item.replace("\n","")
  golly.show("Processing " + filename)
      
  # DMG: now this hacked script can proceed in the same way as the original RuleTableToTree.py 
  
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
  
  golly.show("Reading from rule table file...")
  n_states, neighborhood, transitions = ReadRuleTable(filename)
  
  if not neighborhood in Converters:
      golly.warn("Unsupported neighborhood: "+neighborhood)
      golly.show('')
      golly.exit()
  
  # all converters now create a .rule file
  golly.show("Building rule...")
  rule_name = Converters[neighborhood]( neighborhood,
                                        n_states,
                                        transitions,
                                        filename )
  
  golly.new(rule_name+'-demo.rle')
  golly.setalgo('RuleLoader')
  golly.show("Created rule " + rule_name + ".")
  
  # now go find the rule just created
  newrulefilename = golly.getdir('rules')+rule_name+".rule"
  with open(newrulefilename,"r") as f2:
    treelines = f2.readlines()
  
  # rewrite the rule file to include a @TABLE as well as a @TREE section 
  with open(os.path.join(outfolder, rule_name + ".tree"),"w") as f3:
    for line in treelines:
      f3.write(line)
  
