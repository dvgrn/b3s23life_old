# lifewiki-rlescraper-v0.5.py, alpha release
# This was used to generate and upload a total of 190 
# missing RLE files on http://www.conwaylife.com/wiki,
# that were present in the RLE:{pname} namespace but not
# in the actual LifeWiki pattern collection at
#    http://www. conwaylife.com/patterns/all.zip
#
# Pretty much the only good thing about this code is that it works.
# Later versions might possibly get comments before I forget how things work.
#
# TODO:  add a check for {pname}_synth.rle,
#        and create file for upload if not found in pattern collection
# TODO:  check the contents of {pname}.rle and {pname}_synth.rle
#        and report all cases of discrepancies.  The human running the 
#        script should ideally resolve all these differences, either by
#        reverting changes on the LifeWiki or by submitting the new
#        version of the RLE (from the RLE: namespace) for upload.

import golly as g
import urllib2

samplepath = "C:/users/username/Desktop/"
outfolder = samplepath + "newRLE/"

def retrieveparam(article, param, s):
    chunk = s[s.index(param):s.index(param)+256].replace("\n","|").replace("}","|")
    if chunk.find("|")<0: g.exit("Weird chunk of HTML found in " + article + ":\n" + s[s.index(param):512])
    pnamedef = chunk[:chunk.index("|")]
    if pnamedef.find("=")<0: g.exit("Weird definition found in " + article + ":\n" + pnamedef)
    pval=pnamedef[pnamedef.index("=")+1:].strip()
    return pval
    
linklist=[]
url = 'http://conwaylife.com/wiki/Special:AllPages'
response = urllib2.urlopen(url)
html = response.read()
searchstr = '<td class="mw-allpages-alphaindexline"><a href="/w/index.php?title=Special:AllPages&amp;from='
while html.find(searchstr)>-1:
  start = html.index(searchstr)
  end = html.index(">", start+len(searchstr))
  link=r"http://conwaylife.com/"+html[start+48:end-1].replace("&amp;","&")+"&hideredirects=1"
  linklist+=[link]
  html = html[end:]

articlelist = []
for url in linklist:
  response = urllib2.urlopen(url)
  html = response.read()
  beginindex = html.find('<table class="mw-allpages-table-chunk">')
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

pnamedict = {}
# g.note(str(len(articlelist)))

for item in articlelist:
  if item[:6]!="/wiki/":
    g.note("Weird article link: " +item)
    continue
  articlename = item[6:]
  url = 'http://conwaylife.com/w/index.php?title=' + articlename + '&action=edit'
  response = urllib2.urlopen(url)
  g.show("Checking " + url)
  html = response.read()
  discoverer, discoveryear="", ""
  if html.find("pname")>-1:
    if html.find("discoverer")>-1:
      discoverer=retrieveparam(articlename, "discoverer", html)
    if html.find("discoveryear")>-1:
      discoveryear=retrieveparam(articlename, "discoveryear", html)
  while html.find("pname")>-1:
    nextpname = html.find("pname")
    location = "infobox"
    embedviewer = html.find("EmbedViewer")
    if embedviewer>-1 and nextpname>embedviewer:
      # can't trust discoverer or discoveryear tags for this pattern
      location = "embedded"
      discoverer=""
      discoveryear=""
    pname = retrieveparam(articlename, "pname",html)
    g.show(url + " : " + pname+", " + discoverer + ", " + discoveryear)
    html = html[html.index("pname")+5:]
    if pname not in pnamedict:
      pnamedict[pname] = [url, location, discoverer, discoveryear]
    else:
      pnamedict[pname] = pnamedict[pname] + [url, location, discoverer, discoveryear]
      # g.note("Found multiple uses of " + pname + ":\n"+str(pnamedict[pname]))

missing = []
count = 0
for item in sorted(pnamedict.iterkeys()):
  count +=1
  data = pnamedict[item][:]
  while len(data)>4:
    dtemp = data[0:3]
    if dtemp[1]=="embedded":
      data=data[4:]
    else:
      data = dtemp # not worrying about weird unusual cases like duoplet / diagonal on-off, just take first infobox.
  sourceurl = data[0]
  articlename = sourceurl.replace("http://conwaylife.com/w/index.php?title=","").replace("&action=edit","")
  url = 'http://conwaylife.com/wiki/' + articlename
  response = urllib2.urlopen(url)
  html = response.read()
  if html=="":
    g.note("Problem with article " + articlename + ":\n" + str(pnamedict[item]))
    continue
    # g.exit(articlename + " problem")
  url = 'http://www.conwaylife.com/patterns/' + item + ".rle"
  try:
    response = urllib2.urlopen(url)
    html = response.read()
    # g.note(html[:500])
  except Exception as e:
    if str(e) == "HTTP Error 404: Not Found":
      # g.note("Not Found!  Type error: " + str(e) + " for " + item))
      missing += [item]
      g.show(str(["Missing = ", len(missing), "Count = ", count]))
    else:
      g.show(str(e) + " for " + item)

s=""

for pname in missing:
  url = 'http://conwaylife.com/w/index.php?title=RLE:' + pname + '&action=edit'
  try:
    response = urllib2.urlopen(url)
    html = response.read()
  except:
    s+="\n" + url + "\n"+pname+":  Not Found (or other) error"
  if html.find('name="wpTextbox1">')==-1:
    s+="\n" + url + "\n"+pname+":  Could not find RLE textbox in HTML.  Article probably doesn't exist."
  else:
    start = html.index('name="wpTextbox1">')
    rle = html[start+18:html.index('!',start+17)+1]
    filename = outfolder + pname + ".rle"
    data = pnamedict[pname]
    discoverer, discoveryear = data[2], data[3]
    sourceurl = data[0]
    articlename = sourceurl.replace("http://conwaylife.com/w/index.php?title=","").replace("&action=edit","")
    url = 'http://conwaylife.com/wiki/' + articlename
    paturl = 'http://www.conwaylife.com/patterns/' + pname + ".rle"
    with open(filename, 'w') as f:
      f.write("#N "+pname+".rle\n")
      if discoverer!="":
        if discoveryear!="":
          f.write("#O " + discoverer + ", " + discoveryear + "\n")
        else:
          f.write("#O " + discoverer + "\n")
      f.write("#C " + url + "\n")
      f.write("#C " + paturl + "\n")      
      f.write(rle)
    g.show("Wrote " + filename)
g.setclipstr(s)
g.note("Done!  Exceptions written to clipboard.")
