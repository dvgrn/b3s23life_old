import golly as g
base64dict={}
for index, char in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"):
    base64dict[char]="".join(["1" if index & 2**(5-j) else "0" for j in range(6)])
mapstr = g.getstring("Enter MAP string to convert to a rule: ", "ARYXfhZofugWaH7oaIDogBZofuhogOiAaIDogIAAgAAWaH7oaIDogGiA6ICAAIAAaIDogIAAgACAAIAAAAAAAA")
if mapstr[:3]=="MAP": mapstr=mapstr[3:]
if len(mapstr)!=86: g.warn("Map string is the wrong length -- should be 86 characters."); g.exit()
s = "".join([base64dict[char] for char in mapstr])
ruletablestr="@RULE MAPblahblahblah\nRule table for nontotalistic rule MAPblahblahblah" \
            +"\n\n@TABLE\nn_states:2\nneighborhood:Moore\nsymmetries:none\n\n"
for i in range(512):
    binary = "{0:09b}".format(i)
    for j in binary[4]+binary[:4]+binary[5:]:
      ruletablestr+=j+","
    ruletablestr+=s[i]+"\n"
g.setclipstr(ruletablestr.replace("blahblahblah", mapstr))
