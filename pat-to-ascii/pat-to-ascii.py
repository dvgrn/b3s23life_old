# pat-to-ascii.py
# select a pattern in Golly, run this script,
#   and a plaintext ASCII format version of
#   the pattern will be copied to the clipboard
#
# For a variant producing Life Lexicon format, see also
#   http://conwaylife.com/forums/viewtopic.php?p=64427#p64427

import golly as g
r = g.getselrect()
s=""
for y in range(r[3]):
  for x in range(r[2]):
    s+="*" if g.getcell(x+r[0],y+r[1]) == 1 else "."
  s+="\n"
g.setclipstr(s)
