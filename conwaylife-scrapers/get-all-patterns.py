# get-all-patterns.py, version 1
# Version 1: initial working version

import golly as g
import urllib2
import re
import os

postregex = re.compile(r'<div id="p(\d*)" class="post')

url = "https://conwaylife.com/forums/viewtopic.php?p="

outfolder = "c:/REPLACE/THIS/WITH/YOUR/PATH/"

postset=set()
ruledict={}

ptr =  0 # 86200

count = 0
addthis = 100000

while ptr<86262:  # current most recent post
  ptr+=1
  g.show("Retrieving data for " + str(ptr))
  if ptr in postset:
    continue
  try:
    resp = urllib2.urlopen(url + str(ptr) +"#p" + str(ptr))
    html = resp.read()
  except:
    # g.note("Got an error on p=" + str(ptr))
    continue
  # look for all '<div id="p{n}" class="post', add to dictionary
  posts = postregex.findall(html)
#  for p in posts:
#    postset.add(int(p))
#  g.note(str(len(postset))+"\n"+str(postset)[:500])
#  g.show(str(ptr) + ": now " + str(len(postset)) + " posts seen. Rules exported: " + str(count))
  lastindex = 0
  notdone=1
  while notdone:
    g.show("Retrieved html for post " + str(ptr) + ". Last index = " + str(lastindex))
    index = html.find("<code>",lastindex) + 6
    if index==5: # hmm, I should have added 6 separately after checking for -1
      notdone=0
      break
    if html[index] in ['#', 'x', 'b', 'o', '$', '[', '.', 'O', '*']: # skip any code blocks that don't look like RLE or macrocell or ASCII files
      if html[index]=='#':
        if html[index+1] not in ['C','D','N','O']:
          # don't export this one, it's probably a Python script
          lastindex = index
          continue
      index2 = html.find("</code>", index)
      index3 = html[:index].rfind('" class="post ')
      index4 = html[:index3].rfind('<div id="')+9
      lastpost = html[index4:index3]
      ilastpost = int(lastpost[1:])
    
      if html[index]=="[": # macrocell
        ind1 = html.find("#R",index)
        offset = 2
        ext = ".mc"
      else:
        ind1 = html.find("rule =")
        offset=6
        if ind1==-1:
          ind1 = html.find("rule=")
          offset=5
        ext = ".rle"
        if html[index] in ['.', 'O', '*']:
          ext = ".txt"
      if ind1>-1:
        ind2 = html.find("\n",ind1)
        rulestr = html[ind1+offset:ind2].strip()
    
        if rulestr not in ruledict:
          ruledict[rulestr]=[ilastpost]
        else:
          if ilastpost not in ruledict[rulestr]:
            ruledict[rulestr]+=[ilastpost]
      
      #TODO : check if a pattern can somehow be found in this same post, via a different URL
    
      if int(lastpost[1:]) not in postset:
        patstr = html[index:index2]
        if patstr[-1]!="\n": patstr+="\n"
        fname = os.path.join(outfolder,"pat" + str(count+addthis)[1:] + "_"+lastpost + ext)
        with open(fname,'w') as f:
          if ext==".mc":
            f.write("[M2] (golly VERSION)\n#C https://conwaylife.com/forums/viewtopic.php?p=" + str(ptr) + "#" + lastpost + "\n# "+patstr)
          else:
            f.write("#C https://conwaylife.com/forums/viewtopic.php?p=" + str(ptr) + "#" + lastpost + "\n"+patstr)

        postset.add(int(lastpost[1:]))
        count += 1
        if count==100000:
          addthis = 1000000
    lastindex = index

with open(os.path.join(outfolder,"readme.txt"),'w') as f:
  f.write("Total patterns written: " + str(count) + "\n")
  f.write("Posts with patterns: " + str(postset) + "\n")
  f.write("Rule dictionary:\n" + str(ruledict) + "\n")
