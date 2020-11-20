# get-all-rules.py, version 3.0
# Version 1: initial working version
# Version 2: improve behavior of numbered variants of same rule
# Version 3: make ruledict into a list of posts where the rule was found,
#            and don't create file if it's the same post found again somehow
#            (not sure yet why this happens on rare occasions)
# TODO: fix bug pointed out by muzik (if two or more rules are posted in the same message,
#                                     only the first rule is collected)
import golly as g
import urllib2
import re
import os

postregex = re.compile(r'<div id="p(\d*)" class="post')
# couldn't make the following work, due to something about multiline matching I don't understand:
# ruleregex = re.compile(r'<div class="codebox"><p>Code: <a href="#" onclick="selectCode\(this\); return false;">Select all</a></p><pre><code>@RULE (.*)(?:\n|\r\n?)(.*)</code></pre></div>')
ruleregex = re.compile(r'<div class="codebox"><p>Code: <a href="#" onclick="selectCode\(this\); return false;">Select all</a></p><pre><code>@RULE (.*)')
ruleregex = re.compile(r'<code>@RULE (.*)')

url = "https://conwaylife.com/forums/viewtopic.php?p="

outfolder = "c:/REPLACE/WITH/YOUR/PATH/"

postset=set()
postswithrules=set()
ruledict=dict()

ptr =  8342 # 73300

# TODO:  in future runs, disallow rules found in posts earlier than the starting ptr value

count = 0
while ptr<85945:  # current most recent post
  ptr+=1
  if ptr in postset:
    continue
  try:
    resp = urllib2.urlopen(url + str(ptr) +"#p" + str(ptr))
    html = resp.read()
  except:
    #g.note("Got an error on p=" + str(ptr))
    continue

  # look for all '<div id="p{n}" class="post', add to dictionary
  posts = postregex.findall(html)
  for p in posts:
    postset.add(int(p))
  g.show(str(ptr) + ": now " + str(len(postset)) + " posts seen. Rules exported: " + str(count))
  found = ruleregex.findall(html)
  for item in found:
    trimmeditem = item.rstrip()
    fname = os.path.join(outfolder,trimmeditem + ".rule")

    index = html.find("<code>@RULE " + trimmeditem) + 6
    index2 = html.find("</code>", index)
    index3 = html[:index].rfind('" class="post ')
    index4 = html[:index3].rfind('<div id="')+9
    lastpost = html[index4:index3]
    if trimmeditem in ruledict:
      if int(lastpost[1:]) in ruledict[trimmeditem]:
        continue  # this rule has already been found in this same post, via a different URL -- TODO: find out how this happens
    rulestr = html[index:index2]
    rulelines = rulestr.split("\n")
    firstnonblank=1
    if len(rulelines)<7:  # must not be a real rule -- too short
      continue
    else:
      while rulelines[firstnonblank].rstrip()=="":
        firstnonblank+=1
        if firstnonblank>=len(rulelines): break
    rulewithurl = [rulelines[0]]+["","https://conwaylife.com/forums/viewtopic.php?p=" + str(ptr) + "#" + lastpost,""]+rulelines[firstnonblank:]
    trimmedrule = "\n".join([s.rstrip() for s in rulewithurl])
    if trimmeditem in ruledict:
      if len(ruledict[trimmeditem])==1:
	if os.path.exists(fname):
          os.rename(fname,fname+"0") # all the cases with competing rule definitions should be checked manually
        else:
          g.note("Something strange happened with the rule '" + trimmeditem + "'.  File wasn't there when it should have been.\n" \
          "Contents of ruledict for this item: " + str(ruledict[trimmeditem]) + ".")
      ind=1
      basefname = fname
      while os.path.exists(fname+str(ind)):
        ind+=1
      fname += str(ind)
      if len(ruledict[trimmeditem])!=ind:
        g.note("Something strange is going on with rule '" + trimmeditem + "'.  The count is off for some reason.")

    
    with open(fname,'w') as f:
      f.write(trimmedrule)
    if trimmeditem in ruledict:
      ruledict[trimmeditem] += [int(lastpost[1:])]
    else:
      ruledict[trimmeditem] = [int(lastpost[1:])]
    postswithrules.add(int(lastpost[1:]))
    count += 1

with open(os.path.join(outfolder,"readme.txt"),'w') as f:
  f.write(str(ruledict)+"\n")
  f.write("Total rules written: " + str(count) + "\n")
  f.write("Posts with rules: " + str(postswithrules) + "\n")
