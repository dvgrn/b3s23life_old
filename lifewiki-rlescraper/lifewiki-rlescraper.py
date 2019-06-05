# lifewiki-rlescraper-v1.3.py
# Version 0.6 of this script was used to generate and upload 387 missing RLE files on 
#    http://www.conwaylife.com/wiki,
# that were present in the RLE namespace under RLE:{pname} or RLE:{pname}_synth
# but not in the actual LifeWiki pattern collection as of 1/26/2019 --
#    http://www. conwaylife.com/patterns/all.zip
# Version 0.7 also creates .cells files associated with RLE already uploaded
#    to the LifeWiki server, if the pattern in question is less than 65 cells
#    wide and less than 101 cells high (roughly matching Life Lexicon limits),
#    and if no {pname}.cells file has already been uploaded to the server.
#    On 6 February 2019, 695 .cells files created in this way were bulk-uploaded.
# Version 0.8 also checks for capital letters in pnames, and complains if found.
#    Also added a "noRLEheader" list for patterns where pattern size can't be
#    determined from the header line of the raw RLE file.
# Version 0.9 checks that every infobox pname has "rle = true" and "plaintext = true"
#    (embedded viewers automatically add RLE and plaintext links via template change)
# Version 1.0 does a better job of checking that articles reported to be missing
#     "rle = true" parameters actually contain an infobox
# Version 1.1 reports LifeWiki synthesis costs for articles with apgcodes
# Version 1.2 exports info about oscillators, guns and conduits with discoverer and date
# Version 1.3 creates five separate lists of apgcodes:
#    - apgcodes where the LifeWiki synthesis cost agrees with the Catagolue cost
#    - apgcodes where the LifeWiki synthesis cost is greater than the Catagolue cost
#    - apgcodes where the LifeWiki synthesis cost is less than the Catagolue cost
#    - apgcodes associated with a synthesis on the LifeWiki but not on Catagolue
#    - apgcodes associated with a synthesis on Catagolue but not on the LifeWiki
#        These lists will not include objects on Catagolue for which there is no
#        article on the LifeWiki at all, so no apgcode listed for crossreference.
#
# Pretty much the only good thing about this code is that it works, and saves
#   a considerable amount of admin time creating and uploading files one by one.
#
# DONE:  add a check for {pname}_synth.rle,
#        and create file for upload if not found in pattern collection
# DONE:  using the above check of downloaded RLE files, create
#        .cells versions of every 64x64 or smaller RLE on the LifeWiki
#        Have to process the returned web page data (not just check for Not Found),
#        remove any comments, find the header line, load the file into Golly,
#        check the pattern's bounding box, and export modified comments
#        and the correct ASCII pattern if everything seems to be in order.
# TODO:  check the contents of {pname}.rle, {pname}_synth.rle, and {pname}.cells,
#        and report all cases of discrepancies.  The human running the 
#        script should ideally resolve all these differences, either by
#        reverting changes on the LifeWiki or by submitting the new
#        version of the RLE (from the RLE: namespace) for upload.
# TODO:  find a way to mark embedded viewers with oversized RLE patterns,
#        so that the plaintext link doesn't show up -- or redirect that link
# TODO:  track down bug where a trailing comment after the RLE keeps the
#        .cells pattern from being created (unless it's the lack of #N?)
# TODO:  automate retrieval of synthesiscosts.txt, but only do it on specific
#        request (in response to getstring question) and update the local copy

import golly as g
import urllib2
import re

# Change the path here, and optionally the output folder names...
samplepath = "C:/users/{username}/Desktop/LW/"
outfolder = samplepath + "rle/"
cellsfolder = samplepath + "cells/"
rlefolder = samplepath + "rledata/"
# The following folder should contain an updated synthesis file from Catagolue:
#   https://catagolue.appspot.com/textcensus/b3s23/synthesis-costs
synthfile = samplepath + "synthesiscosts/synthesiscosts.txt"

# ... and *don't* change the path here!
if samplepath == "C:/users/{username}/Desktop/LW/":
  g.note("Please edit the paths on lines 58-64 of the script before running this script.  " \
       + "If samplepath, outfolder, cellsfolder, rlefolder do not point to folders " \
       + " that you have permission to write to, or if synthfile is not present, " \
       + "the data collection process will eventually fail with an error.")
  g.exit()

# first load synth costs from Catagolue into a dictionary
with open(synthfile,"r") as f:
  foundheader = False
  catapgcodes = {}
  for line in f:
    if foundheader == False:
      if line!='"apgcode","cost"\n':
        # TODO:  automate retrieval of synthesiscosts.txt, but only do it on specific request, and update the local copy
        g.exit("synthesiscosts.txt not in correct format.\nGet a copy of https://catagolue.appspot.com/textcensus/b3s23/synthesis-costs .")
      foundheader = True
      continue
    if line.find(',')>-1:
      apgcode, coststr = line.replace('"','').split(',')
      if coststr[:9]=="100000000": coststr=coststr[1:]
      cost = int(coststr)
      if cost == 999999999999999999L: cost = -1
      catapgcodes[apgcode]=cost    
  
toobigpatternslist = ["0e0pmetacell","caterloopillar","caterpillar","centipede","centipede caterloopillar", \
                      "collatz5nplus1simulator","demonoid","gemini","halfbakedknightship","hbkgun",         \
                      "linearpropagator","orthogonoid","parallelhbk","picalculator","shieldbug","succ",     \
                      "telegraph","waterbear"]

# same list as before, but article names, just to keep them off of the "no rle/plaintext param" lists
toobigarticleslist = ['0E0P_metacell', 'Caterloopillar', 'Caterpillar', 'Centipede', 'Centipede_caterloopillar', \
                      'Collatz_5n%2B1_simulator', 'Demonoid', 'Gemini', 'Half-baked_knightship', 'HBK_gun', \
                      'Linear_propagator', 'Orthogonoid', 'Parallel_HBK', 'Pi_calculator', 'Shield_bug', \
                      'Spartan_universal_computer-constructor', 'Telegraph', 'Waterbear']

templatetypes = ['{{Agar', '{{Conduit', '{{Crawler', '{{Fuse', '{{GrowingSpaceship', '{{Gun', '{{InductionCoil', \
                 '{{Methuselah', '{{MovingBreeder', '{{Oscillator', '{{Pattern', '{{Puffer', '{{Reflector', \
                 '{{Rotor', '{{Sawtooth', '{{Spaceship', '{{Stilllife', '{{UnitCell', '{{Wave', '{{Wick', '{{Wickstretcher']


def retrieveparam(article, param, s):
  if s.find(param)<0:
    g.note("Setting clipboard to current html -- can't find '"+param+"'.")
    g.setclipstr(s)
    g.exit()
  regexstr = param+r'\s*=\s*(.*)$' #######################
  match = re.search(regexstr, s, re.MULTILINE)
  if match:
    pval = match.group(1)+"|"
    return pval[:pval.index("|")] # handle the case where newlines are not added before each pipe character
  else:
    g.note("Could not find definition of parameter '"+param+"' in article '"+article+"'.")
    g.setclipstr(s)
    g.exit()

def hasinfobox(s):
  hasinfobox = False
  for item in templatetypes:
    if s.find(item)>-1:
      hasinfobox = True
      break
  return hasinfobox

# first collect all pages of non-redirect links
#   from the Special:AllPages list
###############################################
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

# follow each link, retrieve the page of links
# and collect all the relevant article names on it
##################################################
articlelist = []
for url in linklist: ##############################################
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

# now start collecting pname references from each article,
#   with discoverers and discoveryears when possible
##########################################################
pnamedict = {}
capitalizedpnames, norleparam, noRLEheader = [], [], []
noplaintextparam = {}
apgcodesLWsynthagreeswithC = []
apgcodesLWsynthbetterthanC = []
apgcodesLWsynthworsethanC = []
apgcodesLWsynthbutnoCsynth = []
apgcodesnoLWsynthbutCsynth = []

with open(rlefolder + "rledata.csv","w") as f:
  for item in articlelist: #########################
    if item[:6]!="/wiki/":
      g.note("Weird article link: " +item)
      continue
    articlename = item[6:]
    url = 'http://conwaylife.com/w/index.php?title=' + articlename + '&action=edit'
    response = urllib2.urlopen(url)
    g.show("Checking " + url)
    html = response.read()
    begintext = html.find('wpTextbox1">')
    if begintext<0:
      g.note("Could not find article text textbox 'wpTextbox1' in HTML for " + articlename + ".")
    else:
      html = html[begintext+11:]
    discoverer, discoveryear="", ""
    if html.find("pname")>-1:
      pname = retrieveparam(articlename, 'pname', html)
      if html.find("discoverer")>-1:
        discoverer=retrieveparam(articlename, "discoverer", html)
      if html.find("discoveryear")>-1:
        discoveryear=retrieveparam(articlename, "discoveryear", html)
      if html.find("|rle")<0: # pipe character included because "rle" is too common -- e.g., it's in "Charles Corderman"
        if articlename not in toobigarticleslist:
          if hasinfobox(html):
            norleparam += [articlename]
      else:
        rletext = retrieveparam(articlename, "rle", html)
        if rletext != "true":
          norleparam += ["[nonstandard value for '"+articlename+"' rle = "+rletext+"]"]
      if html.find("|plaintext")<0:
        if articlename not in toobigarticleslist:
          if hasinfobox(html):
            noplaintextparam[pname] = articlename
      else:
        plaintexttext = retrieveparam(articlename, "plaintext", html)
        if plaintexttext != "true":
          noplaintextparam += ["[nonstandard value for '"+articlename+"' plaintext = "+plaintexttext+"]"]
  
      if html.find("|synthesis ")>-1 or html.find("|synthesis=")>-1:
        synth=retrieveparam(articlename, "synthesis", html)
      else:
        synth="none"
      
      if html.find("|apgcode")>-1:
        code = retrieveparam(articlename, "apgcode", html)
        if code in catapgcodes: #Catagolue has a synthesis
          if synth == "none":
            apgcodesnoLWsynthbutCsynth += [(articlename, pname, code, synth)]
          else:
            synthC = int(synth)
            synthLW = catapgcodes[code]
            if synthC > synthLW:
              apgcodesLWsynthbetterthanC  += [(articlename, pname, code, synthC, "better than", synthLW)]
            elif synthC < synthLW:
              apgcodesLWsynthworsethanC  += [(articlename, pname, code, synthC, "worse than", synthLW)]
            else:
              apgcodesLWsynthagreeswithC += [(articlename, pname, code, synth)]
        else:
          if synth != "none":
            apgcodesLWsynthbutnoCsynth += [(articlename, pname, code, synth)]
          else:
            pass # no synthesis in either LW or Catagolue -- nothing to do

      if html.find("{{Oscillator")>-1:
        f.write(str([pname, articlename, discoverer, discoveryear])[1:-1]+", 'Oscillator'\n")
      if html.find("{{Gun")>-1:
        f.write(str([pname, articlename, discoverer, discoveryear])[1:-1]+", 'Gun'\n")
      if html.find("{{Conduit")>-1:
        f.write(str([pname, articlename, discoverer, discoveryear])[1:-1]+", 'Conduit'\n")
      
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
      if pname.lower() != pname:
        capitalizedpnames += [pname]
      g.show(url + " : " + pname+", " + discoverer + ", " + discoveryear)
      html = html[html.index("pname")+5:]
      if pname not in pnamedict:
        pnamedict[pname] = [url, location, discoverer, discoveryear]
      else:
        pnamedict[pname] = pnamedict[pname] + [url, location, discoverer, discoveryear]
        # g.note("Found multiple uses of " + pname + ":\n"+str(pnamedict[pname]))

# go through dictionary of all pnames found, looking for
# raw RLE for either pattern or synthesis or .cells
########################################################
missing, missingsynth, missingcells, toobigforcells = [], [], [], []
count = 0
# g.note("Starting check of pnames")
for item in sorted(pnamedict.iterkeys()):
  count +=1
  g.show("Checking pname '" + item + "'")
  g.update()
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
  width, height = 999999, 999999
  try:
    response = urllib2.urlopen(url)
    html = response.read()
    match = re.search(r'x\s*=\s*([0-9]*),\s*y\s*=\s*([0-9]*)', html)
    if match:
      width = int(match.group(1))
      height = int(match.group(2))
      hdrindex = html.find("x = " + match.group(1) + ",")
      if hdrindex == -1:
        g.note("Problem found with pname '" + item + "' RLE header.")
        hdrindex = 0
      nextnewline = html.find("\n",hdrindex)
      rleonly = html[nextnewline+1:]
      ascii=""
      for line in html.split("\n"):  # collect any comments and add them to .cells file
        if line[0]!="#": break
        if line[1]==" ":
          comment = line[2:]
        elif len(line)==2:
          continue  # ran into this problem with period14glider gun -- an empty "#C" comment
        elif line[2] == " ":
          comment = line[3:]
        else:
          comment = line  # this shouldn't happen, but you never know
        # fix the comment lines that refer to the RLE location
        if comment[-len(item)-4:]==item+".rle":
          comment = comment[:-len(item)-4]+item+".cells"
        ascii += "! " + comment + "\n"
    else:
      noRLEheader += [item]
  except Exception as e:
    if str(e) == "HTTP Error 404: Not Found":
      # g.note("Not Found!  Type error: " + str(e) + " for " + item))
      if item not in toobigpatternslist:  # skip patterns known to be too big for RLE -- they use other formats
        missing += [item]
      # g.show(str(["Missing = ", len(missing), "Count = ", count]))
    else:
      g.note(str(e) + " for rle pname " + item)

# check for an uploaded {pname}_synth.rle  
  url = 'http://www.conwaylife.com/patterns/' + item + "_synth.rle"
  try:
    response = urllib2.urlopen(url)
    html = response.read()
    # g.note(html[:500])
  except Exception as e:
    if str(e) == "HTTP Error 404: Not Found":
      # g.note("Not Found!  Type error: " + str(e) + " for " + item))
      if item not in toobigpatternslist:  # skip patterns known to be too big for RLE -- they use other formats
        missingsynth += [item]
        # g.show(str(["Missing synth = ", len(missing), "Count = ", count]))
    else:
      g.note(str(e) + " for synth pname " + item)

# check for an uploaded {pname}.cells  
  url = 'http://www.conwaylife.com/patterns/' + item + ".cells"
  try:
    response = urllib2.urlopen(url)
    html = response.read()
    # g.note(html[:500])
  except Exception as e:
    if str(e) == "HTTP Error 404: Not Found":
      # g.note("Not Found!  Type error: " + str(e) + " for " + item))
      if item not in toobigpatternslist:  # skip patterns known to be too big for RLE -- they use other formats
        if width <=64 and height <= 100:
          missingcells += [item]
          g.show(str(["Number of missing cells files = ", len(missingcells), "Count of pnames = ", count]))
          # To be consistent with the code below, .cells files should be created in a separate pass
          # -- but we've already had a chance to collect width, height, and RLE from the RLE scan
          # So we'll just make a .cells files using that info, as soon as a missing .cells is found.
          #
          # Notice that this means that .cells files are only created _after_ RLE files are already on the server.
          # That is, we're not going and looking for RLE information in the RLE namespace, only on the server.
          # This is suboptimal, because getting the .cells files there will require two bulk uploads instead of one.
          # On the other hand, doing that in one step needs more code:
          # TODO:  get RLE from raw RLE namespace if we're going to be uploading that
          #        (this will need some fairly serious refactoring, probably moving .cells creation to a separate pass)
          #
          pat = g.parse(rleonly)
          if len(pat)%2 == 0:  # don't try to make a .cells for a multistate file like RLE:briansbrainp3
            g.new(item)
            g.putcells(pat)
            r = g.getrect()
            for y in range(r[3]):
              for x in range(r[2]):
                ascii+="O" if g.getcell(x+r[0],y+r[1]) > 0 else "."
              ascii+="\n"
            with open(cellsfolder + item + ".cells","w") as f:
              f.write(ascii)
        else:  # width and/or height are too big
          toobigforcells += [item]
          # remove from the list of articles that could have cells files but don't
          if item in noplaintextparam:
	      noplaintextparam.pop(item,"Default value. Means if item is not there, I don't care, don't want error.")
    else:
      pass     # g.note(str(e) + " for cells pname " + item) ##########################################

# create RLE files for any patterns that have raw RLE
#   but can not be found on the LifeWiki server
#####################################################
s=""  # cumulative error report
for pname in missing:
  url = 'http://conwaylife.com/w/index.php?title=RLE:' + pname + '&action=edit'
  try:
    response = urllib2.urlopen(url)
    html = response.read()
  except:
    s+="\n" + url + "\n"+pname+":  Not Found (or other) error"
  if html.find('name="wpTextbox1">')==-1:
    s+="\n" + url + "\n"+pname+":  Could not find RLE textbox in HTML.  Article must have pname but no LifeViewer animation."
    g.show("No raw RLE for '" + pname + ".")
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

# create files for any pattern syntheses that have raw RLE
#   but can not be found on the server
##########################################################
for pname in missingsynth:
  url = 'http://conwaylife.com/w/index.php?title=RLE:' + pname + '_synth&action=edit'
  try:
    response = urllib2.urlopen(url)
    html = response.read()
  except:
    # s+="\n" + url + "\n"+pname+":  Not Found (or other) error"
    continue  # for syntheses this is pretty normal, no need to mention it
  if html.find('name="wpTextbox1">')==-1:
    g.show(pname+"_synth:  Could not find RLE textbox in HTML.")
  else:
    s+="\n" + url + "\n" + pname + "_synth: found synthesis that has not yet been uploaded."
    start = html.index('name="wpTextbox1">')
    rle = html[start+18:html.index('!',start+17)+1]
    filename = outfolder + pname + "_synth.rle"
    data = pnamedict[pname]
    discoverer, discoveryear = data[2], data[3]
    sourceurl = data[0]
    articlename = sourceurl.replace("http://conwaylife.com/w/index.php?title=","").replace("&action=edit","")
    url = 'http://conwaylife.com/wiki/' + articlename
    paturl = 'http://www.conwaylife.com/patterns/' + pname + "_synth.rle"
    with open(filename, 'w') as f:
      f.write("#N "+pname+"_synth.rle\n")
      f.write("#C " + url + "\n")
      f.write("#C " + paturl + "\n")      
      f.write(rle)
    g.show("Wrote " + filename)

g.note("Done!  Click OK to write exceptions to clipboard.")
g.setclipstr(s + "\nCells files created: " + str(missingcells) + "\nPatterns too big to create cells files: " + str(toobigforcells) \
               + "\nIllegal capitalized pnames: " + str(capitalizedpnames) + "\npnames with no RLE header: " + str(noRLEheader) \
               + "\nNo RLE param in infobox: " + str(norleparam) + "\nNo plaintext param in infobox; " + str(noplaintextparam) \
               + "\napgcodes where LifeWiki synth agrees with Catagolue: " + str(apgcodesLWsynthagreeswithC) \
               + "\napgcodes where LifeWiki synth is better than Catagolue: " + str(apgcodesLWsynthbetterthanC) \
               + "\napgcodes where LifeWiki synth is worse than Catagolue: " + str(apgcodesLWsynthworsethanC) \
               + "\napgcodes where LifeWiki synth exists but no Catagolue synth: " +str(apgcodesnoLWsynthbutCsynth) \
               )
