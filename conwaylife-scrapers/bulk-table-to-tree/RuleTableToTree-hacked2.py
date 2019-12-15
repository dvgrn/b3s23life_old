# RuleTableToTree-hacked2.py
# modified version of RuleTableToTree.py,
#   intended to create a version of any @TABLE .rule file that can be copied
#   directly into the LifeWiki Rule: namespace for LifeViewer to use
# This involves adding a @TREE section that contains an equivalent encoding of the @TABLE section
# Version 2: process all rules from a text list, instead of one at a time from clipboard or file

import golly
import os
from glife.ReadRuleTable import *
from glife.RuleTree import *
from glife.EmulateTriangular import *
from glife.EmulateMargolus import *
from glife.EmulateOneDimensional import *
from glife.EmulateHexagonal import *

rulefilenames = "C:/users/greedd/Desktop/rulelist.txt" # "C:/PUT/YOUR/FILE/PATH/HERE.txt"
reportfile = "C:/users/greedd/Desktop/errorreportfile.txt" # "C:/PUT/YOUR/LOG/FILE/PATH/HERE.txt"
outfolder = "C:/users/greedd/Desktop/outrules/" # "C:/PUT/YOUR/FOLDER/PATH/HERE/"

# rulesource="The selected rule"
# s = golly.getclipstr()
# if s[:5]=="@RULE":
#   # create a temporary file and set rulefilename to that
#   firstline = s.split("\n")[0]
#   rulefilename = golly.getdir("temp") + firstline.split(" ")[1] + ".rule"
#  with open(rulefilename, "w") as f0:
#     f0.write(s)
#   rulesource = "The rule in the clipboard"
# else:
#   # ask user to select .rule file
#   rulefilename = golly.opendialog('Open a rule table file, to add a @TREE section:', 'Rule files (*.rule)|*.rule')
# 
# if len(rulefilename) == 0: golly.exit()    # user hit Cancel

if rulefilenames == "C:/PUT/YOUR/FILE/PATH/HERE.txt":
  rulefilenames = golly.opendialog('Open a newline-delimited list of rule filenames (with paths)', 'Text files (*.txt)|*.txt')
  if len(rulefilenames) == 0: golly.exit()    # user hit Cancel

with open(rulefilenames, "r") as f:
  rulefileslist = f.readlines()

for item in rulefileslist:
  # do rule @TREE section addition for each rule in rulefileslist
  rulefilename = item.replace("\n","")
  golly.show("Processing " + rulefilename)
  with open(rulefilename,"r") as f:
    rulelines = f.readlines()

  filename = rulefilename.replace(".rule",".table")
  if rulefilename == filename:
    with open(reportfile, "a") as e:    
      e.write(rulefilename + ": This script only works with saved files called *.rule\n-- otherwise things get too confusing.\n")
    continue  
  with open(filename,"w") as f1:
    export = 0
    for line in rulelines:
      if line[:5] == "@TREE":
        with open(reportfile, "a") as e:
          e.write(rulefilename + " already has a @TREE section.  Nothing to do here.\n")
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
    if export==-1:
      continue # don't try to process a file that probably only has a @TREE section
      
  # DMG: now the .table section (only) has been written to a separate file in the same folder,
  #      and this hacked script can proceed in the same way as the original RuleTableToTree.py 
  
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
        # if (line[:7] == "@COLORS" or line[:6] == "@ICONS"):
          # @TREE version of file will include @COLORS and @ICONS
          #   so no need to write them out twice.
          # This assumes that @COLORS and @ICONS come after @TABLE
          #   -- not a good assumption, but it matches current reality
          #   and it's a little easier to write the parser this way
        #   break
        # else:
          f3.write(line)
