catalyst v1.0
by Gabriel Nivasch
Released 3/20/2001
   catgl v1.0 modifications (see addendum) by Dave Greene
   Released 5/29/2001; docs updated 8/2/2008, and again 10/8/2012.
   Adjusted to compile with gcc under Cygwin, 12 December 2018
     (this just meant removing a few profiler-related lines,
      and re-saving all text files with Unix line endings)
     

This program finds ways of modifying the evolution of an input pattern by placing catalysts that react with it. It uses only still-life catalysts.

What is a catalyst?
-------------------

According to Stephen Silver's lexicon [1], a catalyst is "An object that participates in a reaction but emerges from it unharmed.  The term is mostly applied to still lifes, but can also be used of oscillators, spaceships, etc."
As mentioned before, this program uses only still-life catalysts.

How to use this program
-----------------------

To compile in Linux or Cygwin with gcc, this command should work:

gcc catgl.cpp -o catgl.exe -Wno-multichar

The last switch is optional -- remove it if you want to see the multichar warnings for some reason.

Once you have catgl.exe compiled, you can run it directly and type your pattern and options manually.  However this can cause annoying errors if you slightly mistype the initial pattern.

It's generally better to save a text file (with Unix line endings) that contains the answers to all the initial questions that catgl will ask, one after another with newlines between them.  Samples text files such as "Herschel-to-beehive.txt" are included in the catgl folder.  To invoke catgl with a given input file, just type, e.g.,

catgl < Herschel-to-beehive.txt

You first tell the program whether to send the output to the screen or to a file.  An initial "y" sends output to a file in the current directory, which will be called "reactions.txt".

Then you enter the initial pattern. The format is:
' ' or '.' for a dead cell
',' for a fixed dead cell
'*' for a fixed live cell
any other character for a regular live cell.
Finish the pattern with a '!'.

Fixed cells have the property that they are not allowed to change. If one of them changes at a certain generation, the program will not calculate any further generations.

Next, you specify which catalysts you want the program to use.

Then you specify the minimum and maximum generations at which the catalysts should react, and how many generations each catalyst should last minimally, after reacting. If, in a configuration, a catalyst gets destroyed before the that minimum time, the configuration is rejected.

You also specify the maximum number of catalysts to place. The best thing is to keep this number low (1 or 2), because with a high number there are many combinations and the program takes a long time to finish. Therefore, run the program with a low value for this parameter, and see if you find an interesting reaction. Then use that reaction as the initial pattern, and run the program again to place more catalysts.

You have several ways to control where the program should and shouldn't place catalysts. You can make a barrier of fixed dead cells surrounding the area the pattern will occupy. That will prevent catalysts from being placed there. Alternatively, you can scatter isolated live cells that will die at generation 1. That will also prevent catalysts from being placed where the original live cells would react with them. If the pattern emits a glider, you can place a block so that the glider will collide with it.

The catalysts
-------------

Each catalyst is identified with a four-letter name. These are the catalysts the program has:

eat1 - eater 1:
 **..
 *.*.
 ..*.
 ..**

eat2 - eater 2:
 ...*.**
 .***.**
 *......
 .***.**
 ...*.*.
 ...*.*.
 ....*..

snak - snake:
 **.*
 *.**

bloc - block:
 **
 **

tubw - block and tub-with-tail combination:
 **....
 **....
 ......
 ......
 ..*...
 .*.*..
 ..*...
 ...***
 .....*

_tub - tub:
 .*.
 *.*
 .*.

boat:
 .*.
 *.*
 .**

The output of the program
-------------------------

Whether you send the results to a file or to the screen, the program outputs the patterns as it finds them. Each pattern is accompanied by information about the number of catalysts it contains and when they react. For example, this is a hypothetical pattern the program might produce:

........................
.**..................*..
..*..,.............***..
..*.*............,*.....
...*o.............o*....
...,................,...
........................
........................
........................
........................
........................
...o....................
...o.o..................
...ooo..................
.....o..................
........................
...............oo...,...
..............,**,.o*...
...................*.*..
..................,..*..
.....................**.
........................
4 catalysts, which react at gens.: 32 42 42 44
Generation reached: 53

(Note: This is a doctored image. The program usually doesn't produce things like these!)

The numbers "32 42 42 44" indicate the generations at which the catalysts make pre-contact with the pattern (i.e. one generation before they react). The program then indicates that it ran this pattern until generation 53. In this case, it is because at generation 54, one of the fixed cells of one of the catalysts got "pre-destroyed". Therefore, the program did not continue advancing the pattern, and printed out this configuration.

As you can see in the figure, the program marks also the fixed live and dead cells of the catalysts ('*' and ','). This is useful for using the pattern as input again to the program.

How the program works
---------------------

The program tries systematically all possible ways to make catalysts react with the input pattern. This is done with a depth-first traversal of all the possibilities.

The program only places a catalyst at the moment that it will react with the pattern. More specifically, the catalyst is placed in such a way that it makes "pre-contact" with the pattern, i.e. that the next generation the catalyst and the pattern will react.

Since the catalyst is only placed at the moment that it will react, the program has to make sure that, had the catalyst been present on the board all along, it would not have interfered with the pattern previously. In order to do this, the program keeps "history" information of the pattern. For each cell of the board, the program keeps track of whether the cell was ever alive, and what neighbor counts it has had.

When the program places a catalyst on the board, it sets the cells of the catalyst that shouldn't get destroyed as fixed live cells. That is how the program detects if the catalyst gets destroyed later. The program also places some of the neighbor cells of the catalyst as fixed dead. Those are cells that normally do not become alive in a proper reaction with the catalyst, and therefore, if they are born, it is a sign that the catalyst is on the way to destruction. This helps detect catalyst failures early, and speeds up the program significantly.

As mentioned above, the program does a depth-first search. It keeps some global variables that indicate the current position of the search, namely: the current generation, x coordinate, y coordinate, catalyst number, and catalyst orientation. It also keeps two stacks: One of the state of the board in each generation, and another of catalyst placements that have been made. The general outline of the algorithm is like this:

1.- Place as many catalysts as possible in the current generation, by starting to try from the position indicated by the global variables, and going on until we try all positions in this generation. We will thus place 0 or more catalysts.

2.- Advance the board one generation. If successful, go to step 1. If a catalyst got destroyed, go to step 3.

3.- Back up the board to the generation where the last catalyst was placed. Remove that catalyst from the board. Reset the global variables to that catalyst's former position, and increment the position one step (in order not to place the same catalyst again in the same position and fall into an infinite loop). Go back to step 1.

The data structures of the program
----------------------------------

The array stack[] contains the state of the board in each generation. For each generation, it has two 2-D arrays: now[][] and history[][].

stack[g].now[][] contains the state of the board at generation g. The format is as follows: If the cell is alive, then bit #9 (LiveBit) is set. In addition, one of the bits #0 to #8 is set, indicating how many live neighbors the cell currently has. Thus, empty space consists of cells with value 1 (bit #0=1 and all other bits =0).

stack[g].history[][] contains the superposition (bitwise OR) of all previous generations, excluding generation g itself. It is calculated with the formula:
stack[g].history[][] = stack[g-1].history[][] BIT_OR stack[g-1].now[][]

The array fixed[][] indicates which cells on the board are fixed (i.e. they cannot change). Fixed cells can come either from the user's input or from catalysts. Dead fixed cells can overlap: a dead fixed neighbor from a catalyst could be placed on top of a cell that was set fixed dead by the user. When the catalyst is later removed because the program backs up, the cell should still stay fixed. Therefore, fixed[][] keeps a count of how many times a cell has been set fixed. Only if the value is 0 the cell is not fixed.

The array catplaced[] is a stack used to keep track of the catalysts that have been placed on the board. Whenever a catalyst is placed, a new record is added to catplaced[], indicating the following information: x coordinate, y coordinate, catalyst number, catalyst orientation (there are 8 possible rotations and reflections of a catalyst, identified with the numbers 0 through 7), and generation.

There are also five global variables that indicate the current "position" where the program will next try to place a catalyst: currgen, currx, curry, currcatn, and currorient.

The catalysts
-------------

The catalysts that the program uses are stored in the array cata[] (which appears in catalyst2.cpp). The catalysts are represented in this format:

  Not part of the catalyst
. Neighbor cell with 1 neighbor
: Neighbor cell with 2 neighbors
$ Neighbor cell with 4 neighbors
% Neighbor cell with 5 neighbors
^ Neighbor cell with 6 neighbors
1 Starting cell with 1 neighbor
2 Starting cell with 2 neighbors
o Live cell that is allowed to die
* Fixed live cell
x Fixed dead cell with 1 neighbor
X Fixed dead cell with 2 neighbors.

In order to check if a specific catalyst can be placed at a specific location of the board, the program makes sure that:
- No cell from the catalyst or one of its neighbors falls on a cell that has ever been alive.
- No live cell from the catalyst falls on a fixed dead cell.
- If the catalyst cell is dead and has 1 neighbor ('.', '1', or 'x'), the cell on the board never had a count of 2 neighbors.
- If the catalyst cell is dead and has 2 neighbors (':', '2', or 'X'), the cell on the board never had a count of 1 neighbor.
- The catalyst makes pre-contact in the current generation. In other words, there is at least one cell from the starting cells, where the sum of its neighbors, plus the neighbor sum indicated in now[][], equals 3.
- The catalyst will not cause a birth in a fixed dead cell.

If a catalyst passed all the above conditions, then the program proceeds to place it on the board. The catalyst is placed both in now[][] and history[][], to make as if it was present all along on the board. The catalyst is also placed in boardgen0[][] - the array used to print out the patterns.

When the program backs up and removes a catalyst, it restores now[][], history[][], and boardgen0[][] to their previous values.

Parameters that can be changed
------------------------------

There are some things that you can change by changing the source code and re-compiling the program:

The macro SZ controls the size of the board. Take into account that the outermost two-cell-thick frame of the board is not usable. Also, when you enter the input pattern, the program automatically centers it in the board.

You can also change the macros MAXGENS and MAXCATS.

Adding new catalysts
--------------------

If you want to add a new catalyst to the program, you have to do the following:
- Increment the value of NCATS in catalyst.h
- Add an entry for the new catalyst in catalyst2.cpp. Set each cell to its appropriate value. Be careful not to make any mistake, because then I don't know what will happen. You also have to specify the catalyst's dimensions, and give it a four-letter name.
- To check that you entered the catalyst correctly, use the code that is commented-out at the beginning of the main() function, to print it out.
- If the catalyst is symmetric, you have to add some code in placecatalyst(), so that the program will not try repeated orientations and produce every pattern duplicated two times or more. Guide yourself with the code that appears there for the other symmetric catalysts.

Testing that the program works correctly
----------------------------------------

The file tests.txt has some test runs that test for potential bugs in different aspects of the program. If you modify the program, it's a good idea to run these tests.

Other observations
------------------

- I think it wouldn't be too hard to make the program handle catalysts that are oscillators instead of still lifes.

- The program does not support the concept of catalysts based on "action at a distance", even though they are theoretically possible:

 .**......**.....................
 ..*.......*.....................
 ..*.**.***......................
 ...*.*.*........................
 ................................
 ................................
 ...ooooo................ooooo...
 ..o.ooo.o..............o.ooo.o..
 oo.......oo..........oo.......oo

This phenomenon doesn't seem to have any practical use anyway.

- If you find a reaction that uses the boat as a catalyst, and turn around the boat, the boat will become a glider:

 .*........................**........
 *.*.......................*.*.......
 **.........................*........
 ....................................
 ........o.........................o.
 .......ooo.......................ooo
 .......o.........................o..


- Stephen Silver and Alan Hensel are each offering a $100 prize to the first person to find a stable glider reflector that fits in a 50*50 square [2]. Currently, the smallest stable glider reflector known fits in a 81*62 box, and it's based on this reaction:

 ....*.........*.......
 ....***.....***.......
 o......*...*..........
 .oo...**...**.........
 oo....................
 ......................
 ......................
 ......................
 ......................
 ......................
 ......................
 ....................**
 ....................**
 ........**............
 .......*..*...........
 ..**....**............
 .*.*..................
 .*....................
 **....................
 ..........**..........
 ..........*...........
 ...........***........
 .............*........

After 90 generations, the beehive and the block have "magically" appeared back, and a Herschel came out at the right. However, there is a second beehive leftover which must be removed by taking the Herschel through a few Herschel tracks to make it shoot a glider at the beehive.

If one could find a "magic" reaction like this one, but which doesn't produce any leftover, it might be used to construct a smaller stable glider reflector. Maybe this program could be modified to automatically look for reactions where a glider reacts with some object, and the object re-appears with the help of catalysts.

Questions and comments:
Gabriel Nivasch, gnivasch@yahoo.com


Addendum for 'catgl'
--------------------

The following section describes a slightly updated version of the original 'catalyst' program called 'catgl', which catches any output gliders at the pattern boundaries, and also provides a way to specify an optional "target" pattern against which each result pattern is tested.

In the input pattern, four more characters are now considered legal:
 
   '1' means "ON at the start, ON at the end, don't care what happens in between"
   '0' means "OFF at the start, OFF at the end, don't care what happens in between"
   '+' means "OFF at the start, ON at the end, don't care what happens in between"
   '-' means "ON at the start, OFF at the end, don't care what happens in between".
 
The '1' and '0' made sense at the time, though they may be vaguely confusing if you know about the (unrelated) 1's and 2's in the catalyst definitions.  
 
The program does not suppress non-matching output -- it just prints an extra line saying

     Pattern matched target!
 
when it does match.  A text search for 'matched' in reactions.txt will quickly tell you if anything really interesting has turned up.
 
In 'catgl' there's also a count after each pattern of the number of gliders that were suppressed along the edges of the reaction area, where they otherwise would have escaped.  The glider-catcher code was added when 'catalyst' was found to reject perfectly good solutions just because they threw off an extra glider that moved outside the allowed bounding box during the search period.

I haven't quite proven to myself that the glider catcher works correctly in all possible cases -- but it has not failed in any obvious way during random off-and-on searching over several years.  A regular-expression search can quickly locate any results that throw off interesting numbers of gliders.  Technically it should be

   [1-9][0-9]* glider

though "[1-9] glider" is probably plenty optimistic enough in real Life.

A sample batch file and two associated text files are included in the archive.  'Catalyze-HtoB6.bat' and 'H-to-beehive.txt' attempt to convert an undistinguished Herschel-to-beehive converter into a clean Herschel-to-glider converter by catalyzing the large spark at the lower right.  It will produce a 1-megabyte 'reactions.txt' file showing 373 catalyzed reactions.

In 'H-to-beehive.txt' no target is set beyond what is mandated by the catalyst definitions, so all the outputs trivially match the target.  Pointing the batch file to 'H-to-nonbeehive.txt' runs the same search, but specifies that a rectangular area around the input Herschel must be blank when the reaction completes.  The "Pattern matched target!" string is now appended only to those output patterns where this rectangle is blank.

This disqualifies the original beehive output, for example, and of 373 output patterns, 166 now match the target.  (This statistic is reported to stdout and is also included at the end of reactions.txt.)

It is most likely possible to modify the parameters in the input file to find useful or interesting new reactions -- this is left as an exercise for the reader.  I have also been planning for years to write a secondary program (probably at this point it would be a Golly script) to parse the output file and display only the distinct results -- one example of each of the different ash outputs, along with the number of ways found to produce each output.

Questions and comments for 'catgl':
Dave Greene, dave@cranemtn.com
October 8, 2012

References
----------

[1] "Life Lexicon Home Page", http://www.argentum.freeserve.co.uk/lex_home.htm

[2] "The Quest for a Small Stable Reflector", http://www.argentum.freeserve.co.uk/reflect.htm

LEGAL NOTE (Just in case)
-------------------------

THIS PROGRAM IS DISTRIBUTED WITH NO GUARANTEES WHATSOEVER. UNDER NO CIRCUMSTANCES WILL THE AUTHOR BE LIABLE FOR ANYTHING.

Copyright (c) 2001, Gabriel Nivasch.
