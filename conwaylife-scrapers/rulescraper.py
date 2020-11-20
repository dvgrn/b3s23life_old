# lifewiki-rulescraper-v1.1.py
# v1.0: initial working version
# v1.1: fix problem with names incorrectly containing forward slashes or backslashes
# v1.2: fix a few limitations of the error-checking and problem-reporting code

import golly as g
import urllib2
import os

samplepath = g.getstring("Enter path to save .rule files (scroll left to see full path)","C:/users/{username}/Desktop/LWRules/")
if samplepath == "C:/users/{username}/Desktop/LWRules/":
  g.note("Please run this script again and change the sample path to something that works on your system.\n\n" \
       + "If the path you supply does not point to folders that you have permission to write to, " \
       + "or if synthfile is not present, the data collection process will eventually fail with an error.")
  g.exit()

if not samplepath.endswith("/"): samplepath += "/"
if not os.path.exists(samplepath):
  resp = g.getstring("No folder exists at '" + samplepath + "'.  Create it?","Yes")
  if resp.lower()[:1]=="y":
    os.makedirs(samplepath)  # this has no effect if folder(s) already present and/or contain files

# first collect all pages of non-redirect links
#   from the Special:AllPages list
###############################################
url = 'https://conwaylife.com/wiki/Special:AllPages?from=&to=&namespace=3794'
linklist = [url]
response = urllib2.urlopen(url)
html = response.read()
while 1:
   searchind1 = html.find('<div class="mw-allpages-nav">')
   searchind2 = html.find('<div class="mw-allpages-body">')
   substr = html[searchind1:searchind2]
   if substr.find("Previous page")>0: substr=substr[substr.find("Previous page"):]
   ind = substr.find('href="/w/index')
   if ind<0: break  # the last page won't have a "next" link, so we're done collecting at that point
   newurl = 'https://conwaylife.com' + substr[ind+6:substr.find('"',ind+6)]
   newurl = newurl.replace("&amp;","&")
   linklist+=[newurl]
   g.show("Retrieving " + newurl)
   response = urllib2.urlopen(newurl)
   html = response.read()
   if len(linklist)>10: break

# follow each link, retrieve the page of links
# and collect all the relevant article names on it
##################################################
articlelist = []
for url in linklist: ##############################################
  g.show("Retrieving " + url)
  response = urllib2.urlopen(url)
  html = response.read()
  beginindex = html.find('<ul class="mw-allpages-chunk">') 
  endindex = html.find('<div class="printfooter">')
  if beginindex>-1:
    if endindex>-1:
      html=html[beginindex:endindex]
    else:
      g.note("Couldn't find printfooter in HTML for " + url)
      html=""
  else:
    g.note("Couldn't find mv-allpages in HTML for " + url)
    html=""
    
  while html.find('href="')>-1:
    start = html.index('href="')
    end = html.index('" title=',start+6)
    articlelink = html[start+6:end]
    if articlelink.find("hideredirects=1")<0:
      articlelist += [articlelink]
      g.show(articlelink)
    html=html[end:]

s = ""
count = 0
for item in articlelist:
  if item[:6]!="/wiki/":
    s += "Weird article link: " +item +"\n"
    continue
  articlename = item[6:]
  url = 'http://conwaylife.com/w/index.php?title=' + articlename + '&action=edit'
  try:
    response = urllib2.urlopen(url)
    html = response.read()
  except:
    s += "ERROR READING " + url + "\n"
  begintext = html.find('wpTextbox1">')
  if begintext<0:
    s += "Could not find article text textbox 'wpTextbox1' in HTML for " + articlename + "\n"
  else:
    ind = html.find('</textarea>')
    if ind<0:
      s += "Could not find /textarea tag at end of textbox in HTML for " + articlename + "\n"
    html = html[begintext+12:ind]
    rulename1 = html.split("\n")[0].replace("@RULE ","").replace("\n","")
    rulename2 = item.replace("/wiki/Rule:","")
    g.show(str(count) + ": Saving " + rulename1 + str(len(s)))
    with open(samplepath + rulename1.replace("/","").replace("\\","") + ".rule","w") as f:
      f.write(html)
    if rulename1 != rulename2:
      rulename2 = rulename2[0].lower() + rulename2[1:]
      if rulename1 != rulename2:
        s += rulename1 + " doesn't match " + item + "\n"
    if rulename1.find("/")>-1:
      s += "(THE ABOVE IS A BAD ONE, CONTAINING FORWARD SLASHES)\n\n"
    if rulename1.find("\\")>-1:
      s += "(THE ABOVE IS A BAD ONE, CONTAINING BACKSLASHES)\n\n"
g.note("Done.  Click OK to copy list of exceptions to clipboard.")
g.setclipstr(s)
