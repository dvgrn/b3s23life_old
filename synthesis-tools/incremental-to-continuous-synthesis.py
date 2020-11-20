# incremental-to-continuous-synthesis.py, version 2.1
#
# Original script by Chris Cain, 31 January 2015:
#   http://conwaylife.com/forums/viewtopic.php?p=16375#p16375
# Auto-detect functionality added by Dave Greene, 5 February 2019:
#   http://conwaylife.com/forums/viewtopic.php?p=69753#p69753
# Version 2.1: start separation check at 20, not at 1
#              and allow the time to stability to be modified
#              so that non-power-of-2-period oscillators can be built
#
# To produce an automatically optimized continuous synthesis from an
#   incremental synthesis, arrange all the stages of an incremental
#   synthesis in a single row in Golly.  Exactly the same distance
#   should always separate each construction site from the next one,
#   with no vertical offset -- i.e., sites should be aligned in a
#   precise horizontal line.
#
# If the script finds an empty universe, a incremental 46P4H1V0 synthesis
#   will be loaded and analyzed to produce a continuous synthesis.
#
# If a rectangle is selected in Golly, the script will ask the user
#   to provide the step size between construction sites. The first
#   construction site will be assumed to start at the left edge of
#   the current selection.
#
# The script also asks for a repeat time for a second construction recipe
#   following the first.  This should generally be set to 0 unless the
#   construction produces an object that will move out of the way of the
#   next recipe (generally a spaceship).
#
# Hard-coded assumptions include:
#  -- each stage will match the next at LONG_ENOUGH, when auto-finding offset via XOR
#  -- each stage settles by 256 ticks
#  -- initial best_delay = 200 (seems to give adequate spacing before first collision)
#
# Especially with the default double-check setting of 100, if the search
#   suddenly slows down at some point, watch the delay and step numbers
#   reported in the status bar.  If at some stage the delay number stays
#   at its initial value -- i.e., it stops ever going down as the step size
#   counts down powers of two -- then there's something wrong with the recipe
#   near that point.  The script is no longer finding valid matches.
#
# TODO:  catch the case where no valid matches are being found, and
#        cancel the run, displaying progress so far so that the error
#        in the incremental syntheses can be corrected.

import golly as g

LONG_ENOUGH = int(g.getstring("Enter T value for stability check","4096"))

def fill_void():
    # sample incremental 46P4H1V0 synthesis
    pat = g.parse("""1422bo$1422bobo$1422b2o6$1217bo$1218bo191bo$1216b3o141bo50b2o$1226bo
133bobo47b2o$1226bobo127bo3b2o$1226b2o53bo75b2o37bobo29bobo$1276bobo2b
obo72b2o39b2o15bo13b2o$1277b2o2b2o70bo43bo14bobo14bo$1277bo73bobo59b2o
$1343bo8b2o53bo11bo$1284bo57bobo3bo57bobo3bo5bobo$642bo517bo123bo58b2o
3bo39bobo16b2o3bo5b2o16bobo$62bo13bo54bo510bobo513bobo123bo63bo40b2o6b
o14bo16bo6b2o$60bobo13bobo52bobo3bobo365bo132bo3b2o397bo117b2o3bo224bo
5bobo31bobo5bo$61b2o13b2o53b2o4b2o43bobo133bo58bo125bobo133b2o81bobo
119bo68bo127bobo108b2o8b2o52b2o7b2o44b3o6b2o7b2o53b2o7b2o41b2o10b2o7b
2o10b2o$138bo44b2o133bobo57b2o124b2o68bo63b2o82b2o118bobo66b2o128b2o
57bo50bobo9b2o50bobo7bobo45bo5bobo7bobo51bobo7bobo51bobo7bobo$140bo42b
o13bo63bo56b2o5bo51b2o10bo63bo63bo54bobo6bo63bo63bo13bo49bo63bo5b2o56b
o10b2o51bo63bo63bo6bobo48bo5bo57bo5bo5bo44bo6bo5bo5bo51bo5bo5bo51bo5bo
5bo$o60b3o11b3o53bo3bo3b2o45bobo7bobo61bobo53bo7bobo61bobo61bobo61bobo
54b2o5bobo61bobo61bobo7bobo51bobo61bobo7bo53bobo61bobo61bobo61bobo5b2o
48b2o4bobo55b2o4bobo4b2o49b2o4bobo4b2o49b2o4bobo4b2o49b2o4bobo4b2o$b2o
60bo11bo54bobobobo2bobo45b2o7bobo61bobo51bobo7bobo53b2o6bobo61bobo61bo
bo61bobo61bobo61bobo7b2o52bobo61bobo7bobo51bobo6b2o53bobo61bobo61bobo
61bobo61bobo61bobo61bobo61bobo$2o60bo13bo54b2ob2o51bo7b2ob2o59b2ob2o
51b2o6b2ob2o51bo2bo4b2ob2o59b2ob2o59b2ob2o54bo4b2ob2o59b2ob2o59b2ob2o
7bo51b2ob2o59b2ob2o6b2o51b2ob2o4bo2bo51b2ob2o54bo4b2ob2o54bo4b2ob2o4bo
54b2ob2o59b2ob2o59b2ob2o59b2ob2o59b2ob2o$257bo7bo55bo7bo50b2o3bo7bo55b
o7bo55bo7bo51bobobo7bo52bo2bo7bo55bo63bo7bo55bo7bo55bo7bo3b2o50bo7bo
51bobobo7bo51bobobo7bobobo48bo2bo7bo2bo42bo6bo2bo7bo2bo6bo42bo2bo7bo2b
o49bo2bo7bo2bo49bo2bo7bo2bo$6bo42b2o5bo25bo5b2o39b4ob4o45bo9b4ob4o55b
4ob4o55b4ob4o45bo9b4ob4o55b4ob4o55b4ob4o52b2ob4ob4o52b7ob4o55b4ob4o9bo
45b4ob4o55b4ob4o55b4ob4o9bo45b4ob4o52b2ob4ob4o52b2ob4ob4ob2o49b7ob7o
40bobo6b7ob7o6bobo40b7ob7o49b7ob7o49b7ob7o$6bobo39bobo6bo9bo3bo9bo6bob
o38bo2bobo2bo46bo8bo2bobo2bo58bobo61bobo49b2o10bobo61bobo61bobo61bobo
61bobo61bobo2bo8bo49bobo61bobo61bobo10b2o49bobo61bobo61bobo61bobo47b2o
12bobo12b2o47bobo61bobo41bo19bobo19bo$2bo3b2o42bo4b3o8bobobobo8b3o4bo
41bobobobo45b3o3bo5bobobobo56b2obobob2o55b2obobob2o45b2o2b3o3b2obobob
2o53b4obobob2o53b4obobob2o52b5obobob2o52b5obobob2o55b2obobobo5bo3b3o
42b4obobob2o53b4obobob2o53b4obobob2o3b3o2b2o43b4obobob4o50b5obobob4o
50b5obobob5o49b5obobob5o44b2o3b5obobob5o3b2o40b2o2b5obobob5o2b2o41b2o
2b5obobob5o2b2o31b2o8b2o2b5obobob5o2b2o8b2o$3b2o62b2ob2o59b2ob2o53bo5b
2ob2o57bob2ob2obo55bob2ob2obo51bo3bob2ob2obo52bo2bob2ob2obo52bo2bob2ob
2obo52bo2bob2ob2obo52bo2bob2ob2obo55bob2ob2o5bo48bo2bob2ob2obo52bo2bob
2ob2obo52bo2bob2ob2obo3bo48bo2bob2ob2obo2bo49bo2bob2ob2obo2bo49bo2bob
2ob2obo2bo49bo2bob2ob2obo2bo43bobo3bo2bob2ob2obo2bo3bobo39b2o2bo2bob2o
b2obo2bo2b2o41b2o2bo2bob2ob2obo2bo2b2o30bobo8b2o2bo2bob2ob2obo2bo2b2o
8bobo$2b2o183b3o182b3o5bo65b2o61bobo205b3o46b2o62b2o62b2o14bo5b3o38bob
o11b2o62bobo172bo21bo$54b3o25b3o289bo67bo67bo405bo41bo17bo59bo$56bo25b
o105bo184bo8b2o59b2o273bo188b2o8bo56b2o$55bo27bo103b2o65b2o121b2o2bo2b
o57b2o8b2o264b2o59b2o125bo2bo2b2o51b2o8b2o$187bobo59b3ob2o121bobo2bo2b
o63bo2b2o50b2o212bobo60b2ob3o120bo2bo2bobo51b2o2bo71b2o$194b2o55bo3bo
122bo3b2o64b2o3bo50b2o205b2o66bo3bo123b2o3bo52bo3b2o70b2o$194bobo53bo
196bobo53bo3b2o201bobo71bo184bobo66b2o3bo348b3o21b3o13b3o$194bo245b3o
56b2o5b2o204bo263b3o60b2o5b2o346bo6b2o13bo7b2o6bo$442bo57b2o6bo467bo
61bo6b2o346bo8b2o8b2o3bo5b2o8bo$441bo57bo477bo69bo353bo9bobo11bo$443b
3o527b3o437bo$443bo531bo$444bo529bo!""")
    g.putcells(pat)

def find_best_selection():
    r = g.getrect()
    all = g.getcells(r)
    sep = 10
    # - run the pattern for LONG_ENOUGH ticks, get the new settled pattern
    # - try XORing new pattern with original pattern for every possible offset up to 512
    # - one of the offsets should give the lowest total population
    #      (will probably decrease the population instead of increasing it,
    #       unless what is being built is a prolific puffer or gun or some such)
    bestscore, bestsep = len(all),-1  # = population * 2
    allplus = g.evolve(all, LONG_ENOUGH)
    g.addlayer()
    while sep<=512:
        g.show("Finding stage spacing -- testing " + str(sep))
        g.new("sep=" + str(sep))
        g.putcells(all)
        g.putcells(allplus,sep,0,1,0,0,1,"xor")
        score = int(g.getpop())
        if bestscore>score: bestscore, bestsep = score, sep
        sep += 1
    g.dellayer()
    
    sep = bestsep
    g.show("found separation: " + str(sep))
    bestblockscore, bestoffset = -999999, -1
    for offset in range(sep):
        g.select([r[0]-offset, r[1], sep, r[3]])
        g.update()
        blockscore = 0
        for blockx in range(r[0]-offset,r[0]+r[2],sep):
            g.select([blockx, r[1], sep, r[3]])
            blockrect = g.getselrect()
            block = g.getcells(blockrect)
            if len(block)==0:  # ran into empty block, this must not be the right separation
                g.exit("Invalid pattern format found at separation = " + str(sep) + ": selected block is empty.")
            g.shrink(1)
            shrunkblockrect = g.getselrect()
            leftdiff = shrunkblockrect[0]-blockrect[0]
            rightdiff = (blockrect[0]+blockrect[2])-(shrunkblockrect[0]+shrunkblockrect[2])
            blockscore += leftdiff + rightdiff
            if leftdiff<10: blockscore -= (10-leftdiff)**2
            if rightdiff<10: blockscore -= (10-rightdiff)**2
        if blockscore>bestblockscore: bestblockscore, bestoffset = blockscore, offset
    g.select([r[0]-bestoffset, r[1], r[2]+offset, r[3]])
    return sep

def make_target(cells):

    range_x = range(min(cells[::2])  - 1, max(cells[::2])  + 2)
    range_y = range(min(cells[1::2]) - 1, max(cells[1::2]) + 2)

    cells = zip(cells[::2], cells[1::2])

    rect = set((x, y) for x in range_x for y in range_y)

    for x, y in cells:
        rect.remove((x, y))

    for i, j in [(0,0), (0,-1), (-1,-1),(-1,0)]:
        rect.remove((range_x[i], range_y[j]))

    x0, y0 = cells[0]

    return [(x-x0, y-y0) for x, y in cells], [(x-x0, y-y0) for x, y in rect]
        

def add_it(objs, s, dx, dy):
    cells = g.parse(s)
    for i in range(4):
        objs.append((make_target(cells), dx, dy))
        cells = g.evolve(cells, 1)

def delay_construction(obj_list, delay):

    pat = []
    phase = -delay % 4
    n = (delay + phase) // 4

    for cells, dx, dy in obj_list:
        pat += g.transform(g.evolve(cells, phase), -n * dx, -n * dy)

    return pat

def post_state(current_state, obj_list, delay):
    new_state = delay_construction(obj_list, delay)
    return g.evolve(current_state + new_state, delay + 256)

if len(g.getrect()) == 0:
    if g.numstates()>2:
        g.setrule("Life")
    # Script has been run starting from an empty universe.
    # Display a sample continuous synthesis starting from an incremental 46P4H1V0 synthesis.
    fill_void()
    g.select([])
if g.numstates()>2:
    g.exit("Please start this script with a two-state universe as the current layer.")

objs = []

add_it(objs, '3o$2bo$bo!', 1, -1)
add_it(objs, '3o$o$bo!', -1, -1)
add_it(objs, 'bo$2bo$3o!', 1, 1)
add_it(objs, 'bo$o$3o!', -1, 1)
add_it(objs, '3o$o2bo$o$o$bobo!', 0, -2)
add_it(objs, 'bobo$o$o$o2bo$3o!', 0, 2)
add_it(objs, 'o2bo$4bo$o3bo$b4o!', 2, 0)
add_it(objs, 'bo2bo$o$o3bo$4o!', -2, 0)

site_step = 0

rect = g.getselrect()
if not rect:
    site_step = find_best_selection()
    rect = g.getselrect()
    if not rect:
        g.exit("No selection. Could not locate a valid separation and offset automatically.")
    g.fitsel()
    g.update()

if site_step == 0:
    site_step = int(g.getstring("Enter step between construction sites"))
delay2 = int(g.getstring("Enter delay for 2nd construction (only relevant for spaceships)", "0"))
offset = 100

paranoidcheck = int(g.getstring("Enter number of ticks to check below binary search result (min=1)","100"))
if paranoidcheck<1: g.exit("Invalid value for maximum ticks to double-check the binary search result.")
srect = g.getselrect()
cells = g.getcells(srect)
cells = zip(cells[::2], cells[1::2])

obj_lists = []

for x0, y0 in cells:
    for ((wanted, unwanted), dx, dy) in objs:
        if all(g.getcell(x0+x, y0+y) for x, y in wanted):
            if not any(g.getcell(x0+x, y0+y) for x, y in unwanted):

                n = (x0 - rect[0]) // site_step

                for _ in range(n-len(obj_lists)+1):
                    obj_lists.append([])
                
                out_cells = []
                for x, y in wanted:
                    out_cells.append(x0 + x- n * site_step)
                    out_cells.append(y0 + y)
                
                obj_lists[n].append((out_cells, dx, dy))

best_delay = 200
current_state = delay_construction(obj_lists[0], best_delay)
out_list = [(obj_lists[0], best_delay)]

count=len(obj_lists)
sitex, sitey,siteh = srect[0],srect[1],srect[3] #DMG
for obj_list in obj_lists[1:]:
    count-=1
    g.show(str(count))
    sitex+=site_step                            #DMG
    g.select([sitex, sitey, site_step, siteh])  #DMG
    g.update()                                  #DMG
    step = 512
    delay = best_delay + step

    valid_state = post_state(current_state, obj_list, delay)

    while step:
        g.show(str(count)+": count = " + str(step) + ", delay = " + str(delay))
        if post_state(current_state, obj_list, delay - step) == valid_state:
            delay -= step
        step //= 2
        
    best_delay = delay
    for i in range(1, paranoidcheck):
        g.show(str(count)+": count = " + str(step) + ", delay = " + str(delay) + " -- testing for valid state " + str(i))
        if post_state(current_state, obj_list, delay - i) == valid_state:
            best_delay = delay - i
            g.show(str(count)+": count = " + str(step) + ", delay = " + str(delay) + " -- found valid state " + str(i))
            

    current_state += delay_construction(obj_list, best_delay)
    out_list.append((obj_list, best_delay))

for obj_list, delay in out_list:
    g.putcells(delay_construction(obj_list, delay), -4*offset, offset) # y offset allows for input *WSSes
    if delay2:
        g.putcells(delay_construction(obj_list, delay + delay2), -4*offset, offset)

g.show("Done.  See continuous recipe at left.")
