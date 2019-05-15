-- change-random-isotropic-bit-v1.0.lua

local g = golly()
local gp = require "gplus"
local split = gp.split

function fixrule(s)
  return (gp.split(s,":")) -- remove bounded grid spec, if any
end

g.addlayer("temp") -- keep and test the current rule
fixedrule=fixrule(g.getrule())
g.setrule(fixedrule)

bitlist={{-1,-1,256},{0,-1,128},{1,-1,64},{-1,0,32},{0,0,16},{1,0,8},{-1,1,4},{0,1,2},{1,1,1}}
for j = 1, 9 do
    x, y, bit = table.unpack(bitlist[j])
    for i=0, 511 do
        if i&bit>0 then g.setcell(i*5+x,y,1) end
    end
end

g.run(1)
bits={}
ind=1
local rulestr, invstr, revinvstr="","",""
for k=0,2555,5 do
    if g.getcell(k,0)==1 then
        rulestr=rulestr.."1"
        invstr=invstr.."0"
        revinvstr="0"..revinvstr   
    else
        rulestr=rulestr.."0"
        invstr=invstr.."1"
        revinvstr="1"..revinvstr
    end
end

-- build base64 lookup table
local lookupstr="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
bdict={}
for i=1,64 do
    local w=""
    for j=0,5 do
        if (i-1)&2^j>0 then w="1"..w else w="0"..w end
    end
    bdict[w]=lookupstr:sub(i,i)
end

-- decide whether to use standard, inverted, or inverted-reversed bitstring, based on fixedrule
-- (assuming Golly is correctly simulating rules with B0, with or without S8, to avoid strobing)

-- the following won't work for anisotropic non-totalistic rules defined by MAP strings, so
-- we'd have to decode the MAP rulestring into a 512-bit string in that case, check first and last digits.

if string.match(fixedrule,"B0") then rulestr = string.match(fixedrule,"S.*8") and revinvstr or invstr end

g.dellayer()

-- lookup table for isotropic bits
-- Each of the 102 isotropic bits corresponds to one or more bits in the 512-bit binary MAP string.
-- In this script we're assuming the rule in question is isotropic,
-- so technically we just need to check one of the neighborhoods to know the bit setting for all of them.
-- However, we'll check all the anisotropic bits, just to prove that everything is working...
isotropicbits ={{"0",0},
                {"1c",1,4,64,256},
                {"1e",2,8,32,128},
                {"2a",3,6,9,36,72,192,288,384},
                {"2c",5,65,260,320},
                {"2e",10,34,136,160},
                {"2i",40,130},
                {"2k",12,33,66,96,129,132,258,264},
                {"2n",68,257},
                {"3c",69,261,321,324},
                {"3e",42,138,162,168},
                {"3a",11,38,200,416},
                {"3i",7,73,292,448},
                {"3k",98,140,161,266},
                {"3n",13,37,67,193,262,328,352,388},
                {"3j",14,35,74,137,164,224,290,392},
                {"3q",70,76,100,196,259,265,289,385},
                {"3r",41,44,104,131,134,194,296,386},
                {"3y",97,133,268,322},
                {"4c",325},
                {"4e",170},
                {"4a",15,39,75,201,294,420,456,480},
                {"4i",45,195,360,390},
                {"4k",99,141,165,225,270,330,354,396},
                {"4n",71,77,263,293,329,356,449,452},
                {"4j",106,142,163,169,172,226,298,394},
                {"4q",102,204,267,417},
                {"4r",43,46,139,166,202,232,418,424},
                {"4y",101,197,269,323,326,332,353,389},
                {"4t",105,135,300,450},
                {"4w",78,228,291,393},
                {"4z",108,198,297,387},
                {"5c",171,174,234,426},
                {"5e",327,333,357,453},
                {"5a",79,295,457,484},
                {"5i",47,203,422,488},
                {"5k",229,334,355,397},
                {"5n",107,143,167,233,302,428,458,482},
                {"5j",103,205,271,331,358,421,460,481},
                {"5q",110,206,230,236,299,395,419,425},
                {"5r",109,199,301,361,364,391,451,454},
                {"5y",173,227,362,398},
                {"6c",175,235,430,490},
                {"6e",335,359,461,485},
                {"6a",111,207,303,423,459,486,489,492},
                {"6i",365,455},
                {"6k",231,237,363,366,399,429,462,483},
                {"6n",238,427},
                {"7c",239,431,491,494},
                {"7e",367,463,487,493},
                {"8",495}
               }

-- pick a random bit to flip that isn't B012a
bschoice = math.random(2)    -- 1=B, 2=S
-- flipping any bit would look like this:
-- flippedbit = isotropicbits[math.random(#isotropicbits)]

if bschoice==1 then   -- with B bits, don't use the first four
  flippedbit = isotropicbits[math.random(#isotropicbits-4)+4]
else
  flippedbit = isotropicbits[math.random(#isotropicbits)]
end
-- g.note("Chosen bit is "..flippedbit[1])
finalrule = "B"
for i,bitlist in ipairs(isotropicbits) do
  sum=0
  bitname = bitlist[1]
  for j=2,#bitlist do
    value = bitlist[j]
    sum=sum+tonumber(string.sub(rulestr,value+1,value+1))
  end
  if sum==#bitlist-1 then s=bitname else s="" end   -- assuming isotropic rule here
  if bitname==flippedbit[1] and bschoice==1 then 
    -- g.note("B bitname ="..bitname.." and s="..s)
    s = (s=="") and bitname or ""
  end
  finalrule = finalrule..s
end
finalrule = finalrule.."/S"
for i,bitlist in ipairs(isotropicbits) do
  sum=0
  bitname = bitlist[1]
  for j=2,#bitlist do
    value = bitlist[j]+16
    sum=sum+tonumber(string.sub(rulestr,value+1,value+1))
  end
  if sum==#bitlist-1 then s=bitname else s="" end   -- assuming isotropic rule here
  if bitname==flippedbit[1] and bschoice==2 then
    -- g.note("S bitname ="..bitname.." and s="..s)
    s = (s=="") and bitname or ""
  end
  finalrule = finalrule..s
end
-- g.note(finalrule)
g.setrule(finalrule)
canonicalrule = g.getrule()
-- g.note(canonicalrule)
