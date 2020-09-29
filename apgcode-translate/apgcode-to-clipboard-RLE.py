
# apgcode-to-clipboard-RLE:
#   takes an input apgcode, and copies equivalent RLE (with a header line)
#   into the clipboard, ready to be pasted into Golly.
# https://conwaylife.com/forums/viewtopic.php?p=27197#p27197
# -- see also the following post for "biggiemac's script" -- rle-to-apgcode.
#
# decodeCanon function:  creates a pattern cell list from a canonical apgcode,
#   an alphanumeric representation used in apgsearch by Adam P. Goucher
#
# By Arie Paap 
# Sept. 2014
# 
# ord2() from apgsearch, by Adam P. Goucher

import golly as g

g.setrule("Life")

def decodeCanon(canonPatt):
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    
    ox = 0
    x = 0
    y = 0
    clist = []
    
    ii = 0
    
    while ii < len(canonPatt):
        c = canonPatt[ii]
        if (c == 'y'):
            ii += 1
            x += 4 + ord2(canonPatt[ii])
            
        elif (c == 'x'):
            x += 3
        
        elif (c == 'w'):
            x += 2
        
        elif (c == '0'):
            x += 1
        
        elif (c == 'z'):
            x = ox
            y += 5
            
        else:
            u = ord2(c)
            v = 1
            for jj in xrange(0,5):
                if (u & v):
                    clist += [x, y+jj]
                v = v << 1
            x += 1
            
        ii += 1
    
    return clist

# Converts a base-36 case-insensitive alphanumeric character into a
# numerical value.
def ord2(char):

    x = ord(char)

    if ((x >= 48) & (x < 58)):
        return x - 48

    if ((x >= 65) & (x < 91)):
        return x - 55

    if ((x >= 97) & (x < 123)):
        return x - 87

    return -1

# Python function to convert a cell list to RLE
# Author: Nathaniel Johnston (nathaniel@nathanieljohnston.com), June 2009.
#          DMG: Refactored slightly so that the function input is a simple cell list.
#               No error checking added.
#               TBD:  check for multistate rule, show appropriate warning.
# --------------------------------------------------------------------

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

# --------------------------------------------------------------------

def giveRLE(clist):
   clist_chunks = list (chunks (g.evolve(clist,0), 2))
   mcc = min(clist_chunks)
   rl_list = [[x[0]-mcc[0],x[1]-mcc[1]] for x in clist_chunks]
   rle_res = ""
   rle_len = 1
   rl_y = rl_list[0][1] - 1
   rl_x = 0
   for rl_i in rl_list:
      if rl_i[1] == rl_y:
         if rl_i[0] == rl_x + 1:
            rle_len += 1
         else:
            if rle_len == 1: rle_strA = ""
            else: rle_strA = str (rle_len)
            if rl_i[0] - rl_x - 1 == 1: rle_strB = ""
            else: rle_strB = str (rl_i[0] - rl_x - 1)

            rle_res = rle_res + rle_strA + "o" + rle_strB + "b"
            rle_len = 1
      else:
         if rle_len == 1: rle_strA = ""
         else: rle_strA = str (rle_len)
         if rl_i[1] - rl_y == 1: rle_strB = ""
         else: rle_strB = str (rl_i[1] - rl_y)
         if rl_i[0] == 1: rle_strC = "b"
         elif rl_i[0] == 0: rle_strC = ""
         else: rle_strC = str (rl_i[0]) + "b"
         
         rle_res = rle_res + rle_strA + "o" + rle_strB + "$" + rle_strC
         rle_len = 1

      rl_x = rl_i[0]
      rl_y = rl_i[1]
   
   if rle_len == 1: rle_strA = ""
   else: rle_strA = str (rle_len)
   rle_res = rle_res[2:] + rle_strA + "o"
   
   return rle_res+"!"

canonPatt = g.getstring('Enter apgcode','xp2_31e8gzoo1vg54','')
canonPatt = canonPatt.strip().lower()
canonPatt = canonPatt.split('_')[-1]

if not canonPatt:
    g.exit('Pattern is empty')

patt = decodeCanon(canonPatt)

RLE = giveRLE(patt)
header="x = " + str(max(patt[0::2])-min(patt[0::2])+1)+", y = " + str(max(patt[1::2])-min(patt[1::2])+1)+", rule = B3/S23\n"
g.setclipstr(header + RLE)
g.show(RLE)
