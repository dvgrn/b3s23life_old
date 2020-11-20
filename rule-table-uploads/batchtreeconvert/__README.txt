This folder contains:
1) createbatch - a Linux bash script which finds rules that need an @TREE section added
2) aliases.txt - a text file containing all of the supported LifeViewer rule aliases
3) BatchRuleTableToTree.py - batch rule @TREE adder to run in Golly
4) ReadRuleTable.py - hacked version from Scripts/Python/glife [incompatible]
5) RuleTree.py - hacked version from Scripts/Python/glife [incompatible]

The two files marked [incompatible] are needed for BatchRuleTableToTree.py but will
break the existing RuleTableToTree.py script so it's important you take copies of
the originals before you replace them with these ones.

To use:
createbatch assumes you've already got a set of Rule definitions and RLE patterns.

Assuming the following directory structure:
./
./createbatch
./aliases.txt
./Rules/*.rule
./Patterns/*.rle

Run createbatch against the rule files:

% createbatch Rules/*.rule Rules/*.rule0

Create batch will process each rule specified on the command line and
those that are valid and have a @TREE or have a @TABLE and need a @TREE section
will be copied to a folder called BatchInput/ for later processing by Golly.

1) It will ignore rules that match one of the aliases defined in aliases.txt.
2) It will ignore rules that match a built-in rule such as B3/S23.
3) It will ignore rules that aren't referenced by any of the patterns in Patterns/*.rle
The pattern reference checking will generate a file called "patternrules.txt" the first time it's run to do this.

There's no need to process .rule1, .rule2 etc as these are handled during the .rule0
processing.

When createbatch is finished you'll have two things:

1) A folder called BatchInput/ with all of the needed .rule files for Golly.
2) A file called "batchinput.txt" containing a list of the paths to those files.

You then need to run "BatchRuleTableToTree.py" in Golly which will use the
"batchinput.txt" file and the folder of rules and process each one adding
a @TREE section to those .rule files that need it and just copying across those
rules that already have one.

The finished rules are put in a folder call BatchOutput/ and it's these that should
be uploaded to the Repository.
