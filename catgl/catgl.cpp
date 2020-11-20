/* catgl v1.0 completed 5/29/2001 by Dave Greene
   Based on catalyst v1.0, released 3/21/2001
   Copyright (c) 2001, Gabriel Nivasch
   Changes between catalyst 1.0 and catgl 1.0:
   - all source code combined into a single catgl.cpp file
   - added '1', '0', '+', '-' target options to input (see readme.txt)
   - glider-catcher code avoids rejecting glider-producing reactions
*/

#include <stdio.h>
#include <stdlib.h>

#define SZ 60
#define MAXGENS 300
#define MAXCATS 10

#define NCATS 7
#define CATSZ 15


/* The following array contains the state of the pattern at each
generation from 0 to the current one. For each generation there are two
arrays: now[SZ][SZ] and history[SZ][SZ]. now[][] contains the state of
the pattern at that generation. The format is as follows:
If the cell is alive, then bit #9 (LiveBit) is set.
In addition, exactly one of the bits #0 to #8 is set, indicating the
number of live neighbors the cell has.

history[][] contains the superposition (inclusive "OR") of all the
states each cell has been in, in all the previous generations.

The purpose of history[][] is to know whether the cell has ever been alive,
and if it was never alive, to know all the different neighbor counts it
has had. If bit #9 is set, it means the cell has been alive at some
point, and each of the bits #0 to #8 that is set indicates a neighbor
count the cell has had at some point.

For each generation there are also four variables indicating the current
boundaries of the pattern, the variable numcats, which indicates how
many catalysts have been placed this generation, and the variable numgliders,
which is the total number of gliders created as of this generation.
*/
struct board
{
	int now[SZ][SZ];
	int history[SZ][SZ];
	int xmin, xmax, ymin, ymax;
	int numcats, numgliders;
} stack[MAXGENS];

//Bit values used in now[][] and history[][]:
#define LiveBit 512
#define CountBitMask 511

//This macro function is used in advance1gen():
#define WillLive(x) ((x)==8 || (x)==516 || (x)==520)

/* The following array is used to print out the patterns created.
At the beginning the initial pattern is set in it. In addition, each
time a catalyst is placed on the board at a certain generation, it is
also placed here. When the catalyst is removed from the board, it is
also removed from here.
*/
int boardgen0[SZ][SZ];
int target[SZ][SZ];
int targetgen0[SZ][SZ];
int g0minx=SZ, g0miny=SZ, g0maxx=0, g0maxy=0;

/* This array indicates which cells are fixed, i.e. if they are dead,
they are not allowed to live, and if they are alive, they are not
allowed to die. There are two sources from which fixed cells can come:
From the catalysts (cells marked 'x', 'X', and '*'), or from the input
pattern of the user. Note that cells that were set fixed dead by the
user or by a catalyst, might be set again as fixed dead by another catalyst.
Then, when the second catalyst is removed, the cell should still remain fixed
dead because of the first catalyst or the user's input. Therefore, the
procedure is as follows:
To set a cell as fixed, add 1. To unset it, substract 1. The cell is free
only if the value is 0. If the value is less than 0, it is an error.
*/
int fixed[SZ][SZ];

/* The following array contains info for each catalyst that has
been placed on the board: position, catalyst number, orientation,
generation placed, and the old values of the pattern boundaries, which
are restored when the catalyst is removed.
*/
struct catposition
{
	int x, y, n, orient, gen;
	int oldxmin, oldxmax, oldymin, oldymax; //Used to restore the values
		//after removing the catalyst.
	int g0oldminx, g0oldminy, g0oldmaxx, g0oldmaxy;
		//Used to restore g0minx, etc., after removing the catalyst.
} catplaced[MAXCATS];

struct cell
{ int x, y;};

struct catalyst
{
	char c[CATSZ][CATSZ];
	int x, y, name;
};

const catalyst cata[NCATS]=
{
	{{{' ', ' ', 'x', ':', '2', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', '.', '*', 'o', ':', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'.', ':', '$', '%', '*', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {':', '*', '*', '*', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {':', '*', '$', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'.', '.', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '}},
	  6, 6, 'eat1'},
	{{{' ', ' ', ' ', '.', '.', 'X', ':', '2', '1', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', '.', ':', '$', '*', '$', 'o', 'o', '2', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'.', ':', '*', '*', '*', '$', 'o', 'o', ':', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'.', '*', '%', '^', '$', '$', '$', '$', 'X', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'.', ':', '*', '*', '*', '$', '*', '*', '.', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', '.', ':', '%', '*', '^', '*', '$', '.', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ':', '*', '%', '*', ':', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', '.', ':', '*', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', '.', '.', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '}},
	  9, 9, 'eat2'},
	{{{'x', '.', ':', ':', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'2', '*', '$', '*', '*', ':', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'X', '*', '*', '$', '*', ':', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'x', ':', ':', ':', '.', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '}},
	  4, 6, 'snak'},
	{{{'.', 'X', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {':', '*', 'o', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {':', '*', 'o', '2', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'.', 'X', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '}},
	  4, 4, 'bloc'},
	{{{' ', ' ', ' ', ' ', '.', ':', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ':', '*', '*', ':', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ':', 'o', 'o', ':', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', '.', ':', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', 'x', '.', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', '.', ':', 'o', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', '.', '*', '$', 'o', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'.', ':', '$', '$', '*', 'X', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {':', '*', '*', '*', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {':', '*', '$', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'.', '.', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '}},
	  11, 8, 'tubw'},
	{{{' ', '.', 'x', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'.', ':', '*', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'1', 'o', '$', '*', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'.', ':', '*', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', '.', 'x', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '}},
	  5, 5, '_tub'},
	{{{' ', 'x', '.', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'x', ':', '*', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'1', 'o', '%', '*', ':', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {'1', 'X', '*', '*', ':', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', '.', ':', ':', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '},
	  {' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '}},
	  5, 5, 'boat'}
};

int catisused[NCATS]; //The user can select which catalysts to use.

int startinggen, gens, catstoplace, catspergen, catsurvive;
int currgen, currx, curry, currcatn, currorient;
int nCatsTotal=0; //Used to index catplaced[]
int callcount=0;
int nummatched=0;

int advance1gen(void);
int placecatalyst(void);
int removelastcat(void);
void printgen(int);
void printboard(FILE *);
void checkboard(FILE *);
void printinfo(FILE *);

int main()
{
	int initial[SZ][SZ];
	int x, y, g;
	int xmin=SZ, xmax=0, ymin=SZ, ymax=0;
	char ch;
	int tofile;
	FILE *fi;

	//Use this commented-out code to print out a catalyst and check that
	//it is correct:
	/*for (y=0; y<cata[6].y; y++)
	{
		for (x=0; x<cata[6].x; x++)
			printf("%c", cata[6].c[x][y]);
		printf("\n");
	}
	if(1)return 0;*/

	for (x=0; x<SZ; x++)
		for (y=0; y<SZ; y++)
		{
			initial[x][y]=0;
			boardgen0[x][y]=0;
			fixed[x][y]=0;

			for (g=0; g<MAXGENS; g++)
			{
				stack[g].now[x][y]= 1<<0;
				stack[g].history[x][y]= 1<<0;
			}
		}

	for (x=0; x<NCATS; x++)
		catisused[x]=0;

	printf("Print output to file (y/n)? ");
	do
	{ scanf("%c", &ch); }
	while (ch!='n' && ch!='N' && ch!='y' && ch!='Y');

	tofile=((ch=='Y') || (ch=='y'));
	if (tofile)
		fi=fopen("reactions.txt", "w");
	else
		fi=stdout;

	printf("\nPlease enter the pattern. Use ' ' or '.' for regular dead cells,\n"
		"',' for fixed dead cells, '*' for fixed live cells, and any other \n"
		"character for regular live cells. Finish the pattern with '!':\n");

	//Read the pattern entered by the user and store it in initial[][].
	// target[][] will contain a 1 for cells that must be off at end, 2 if must be on
	//Set the fixed cells in fixed[][]:
	x=3;
	y=3;
	char c;
	while ((c=getchar())!='!')
	{
		if (c == '\n' || c == 'n' || c == 'N')
		{
			x=3;
			y++;
			continue;
		}

		if (c != ' ' && c != '.')
		{
			if (x>=SZ-3)
			{ printf("Error: Pattern too wide.\n"); return 1; }
			if (y>=SZ-3)
			{ printf("Error: Pattern too tall.\n"); return 1; }

			if (c == ',')
			{
				initial[x][y]=1; //Fixed dead
				target[x][y]=1;  //Must (obviously) be dead in final pattern
			}
			else if (c == '*')
			{
				initial[x][y]=2; //Fixed live
				target[x][y]=2;  //Must (obviously) be live in final pattern
			}
			else if (c == '1')
				{
					initial[x][y]=3; //Live
					target[x][y]=2;  //Must be live in final pattern
				}
			else if (c == '0')
				target[x][y]=1;   //Must be dead in final pattern
			else if (c == '+')
				target[x][y]=2;   //Must be live in final pattern
			else if (c == '-')
				{
					initial[x][y]=3; //Live
					target[x][y]=1;  //Must be dead in final pattern
				}
			else
				initial[x][y]=3; //Live

			if (x<xmin) xmin=x;
			if (x>xmax) xmax=x;
			if (y<ymin) ymin=y;
			if (y>ymax) ymax=y;
		}

		x++;
	}

	//Initialize fixed[][], stack[0], boardgen0[][], and targetgen0[][],
	//centering the pattern in the middle of the board:
	int xoffset=(SZ-xmax-xmin-2)/2, yoffset=(SZ-ymax-ymin-2)/2;
	for (x=xmin-1; x<=xmax+1; x++)
		for (y=ymin-1; y<=ymax+1; y++)
		{
			stack[0].now[x+xoffset][y+yoffset]=0;

			if (initial[x][y]>1) //2 or 3, which is alive
			{
				stack[0].now[x+xoffset][y+yoffset]=LiveBit;
				//Little hack so that things work properly:
				stack[0].history[x+xoffset][y+yoffset] = 1<<3;

				boardgen0[x+xoffset][y+yoffset]=1;
			}

			if (initial[x][y]==1 || initial[x][y]==2) //Fixed
				fixed[x+xoffset][y+yoffset]=1;

			// copy target pattern to correct offset
			targetgen0[x+xoffset][y+yoffset]=target[x][y];

			//Count the neighbors:
			int count=(initial[x-1][y-1]>1) + (initial[x][y-1]>1) + (initial[x+1][y-1]>1)
			         +(initial[x-1][y  ]>1)                       + (initial[x+1][y  ]>1)
			         +(initial[x-1][y+1]>1) + (initial[x][y+1]>1) + (initial[x+1][y+1]>1);

			if (count<0 || count>8)
			{ printf("Error: count is out of range.\n"); return 1; }

			//Check for inconsistency:
			if ((initial[x][y]==2 && count!=2 && count!=3) ||
				(initial[x][y]==1 && count==3))
			{ printf("Error: Inconsistency in the starting pattern.\n"); return 1; }

			//Set the neighbor count bit:
			stack[0].now[x+xoffset][y+yoffset] |= 1<<count;
		} //for for

	//Set boundary variables:
	stack[0].xmin= g0minx= xmin-1 + xoffset;
	stack[0].xmax= g0maxx= xmax+1 + xoffset;
	stack[0].ymin= g0miny= ymin-1 + yoffset;
	stack[0].ymax= g0maxy= ymax+1 + yoffset;

	stack[0].numcats=0;

	//Repeat the initial pattern to the user:
	printf("\nYou entered:\n");
	if (tofile)
		fprintf(fi, "Initial pattern:\n");
	for (y=ymin; y<=ymax; y++)
	{
		for (x=xmin; x<=xmax; x++)
		{
			switch (initial[x][y])
			{
				case 0: ch='.'; break;
				case 1: ch=','; break;
				case 2: ch='*'; break;
				case 3: ch='o'; break;
			}
			printf("%c", ch);
			if (tofile)
				fprintf(fi, "%c", ch);
		}
		printf("\n");
		if (tofile)
			fprintf(fi, "\n");
	}

	//Also repeat the target grid (temp diagnostic)
	printf("\nYou entered a target pattern of:\n");
	if (tofile)
		fprintf(fi, "Target pattern:\n");
	for (y=ymin; y<=ymax; y++)
	{
		for (x=xmin; x<=xmax; x++)
		{
			switch (target[x][y])
			{
				case 0: ch='.'; break;
				case 1: ch=','; break;
				case 2: ch='*'; break;
			}
			printf("%c", ch);
			if (tofile)
				fprintf(fi, "%c", ch);
		}
		printf("\n");
		if (tofile)
			fprintf(fi, "\n");
	}

	printf("\nCustomize which catalysts to use (y/n)? ");
	do
	{ scanf("%c", &ch); }
	while (ch!='n' && ch!='N' && ch!='y' && ch!='Y');

	if ((ch=='Y') || (ch=='y'))
	{
		printf("These are the available catalysts:\n");
		for (x=0; x<NCATS; x++)
			printf("%2d: %c%c%c%c\n", x+1, cata[x].name>>24, cata[x].name>>16,
				cata[x].name>>8, cata[x].name);
		do
		{
			printf("Enter a number from the above list, or 0 to finish: ");
			scanf("%d", &x);
			if (x==0)
				break;
			if (x>NCATS || x<0)
			{ printf("Invalid number.\n"); continue; }
			x--;
			catisused[x]=1;
			printf("%c%c%c%c selected.\n", cata[x].name>>24, cata[x].name>>16,
				cata[x].name>>8, cata[x].name);
		}
		while(1);
	}
	else
		for (x=0; x<NCATS; x++)
			catisused[x]=1;

	if (tofile)
	{
		fprintf(fi, "\nCatalysts to use:\n");
		for (x=0; x<NCATS; x++)
			if (catisused[x])
				fprintf(fi, "%c%c%c%c\n", cata[x].name>>24, cata[x].name>>16,
					cata[x].name>>8, cata[x].name);
	}

	printf("\nEarliest generation for placing catalysts? ");
	scanf("%d", &startinggen);

	printf("Latest generation for placing catalysts? ");
	scanf("%d", &gens);

	if (tofile)
		fprintf(fi, "\nGenerations for placing catalysts: %d through %d.\n",
			startinggen, gens);

	printf("How many generations must a catalyst survive? ");
	scanf("%d", &catsurvive);

	gens += catsurvive;
	if (gens>=MAXGENS)
	{
		printf("Error: %d exceeds the maximum number of generations, which is %d.\n",
			gens, MAXGENS-1);
		return 1;
	}

	printf("Maximum number of catalysts? ");
	scanf("%d", &catstoplace);
	if (catstoplace>MAXCATS)
	{
		printf("Error: %d exceeds the maximum number of catalysts, which is %d.\n",
			catstoplace, MAXCATS);
		return 1;
	}

	/* The purpose of this option was to allow the user to restrict the number of
	catalysts that can be placed in one generation, in order to reduce the
	huge number of possibilities that occur when catstoplace has a large value.
	However, searching with a large value of catstoplace is inconvenient in any
	case. Therefore, I deactivated this option but still left it in the code.
	To re-activate it, un-comment this code and remove the line
	"catspergen=catstoplace;":
	*/
	/*printf("Maximum number of catalysts in one generation? ");
	scanf("%d", &catspergen);*/
	catspergen=catstoplace;


	printf("\n");

	if (tofile)
	{
		fprintf(fi, "Catalysts must survive %d generation%s.\n", catsurvive,
			catsurvive==1?"":"s");

		/*fprintf(fi, "%d catalysts maximum (%d maximum in one generation).\n\n",
			catstoplace, catspergen);*/
		fprintf(fi, "%d catalyst%s maximum.\n\n", catstoplace,
			catstoplace==1?"":"s");
	}

	currgen=0;
	currx=0;
	curry=0;
	currcatn=0;
	currorient=0;

	int numprinted=0;

	//Main loop:
	while(currgen>=0)
	{
		//Place another catalyst at this generation
		//until you can no more.
		if (currgen >= startinggen && currgen+catsurvive <= gens)
			while (nCatsTotal < catstoplace &&
				stack[currgen].numcats < catspergen &&
				placecatalyst())
			{ }

		if (currgen==gens)
		{
			fprintf(fi, "Pattern # %d:\n", ++numprinted);
			printboard(fi);
			checkboard(fi);
			printinfo(fi);

			if (removelastcat())
				break; //Finished. Out of main loop.

			//Increment the current position:
			currx++;
			continue;
		}

		//Advance 1 generation.
		if (advance1gen())
		{
			if (nCatsTotal==0 ||
				currgen-catplaced[nCatsTotal-1].gen>=catsurvive)
			{
				fprintf(fi, "Pattern # %d:\n", ++numprinted);
				printboard(fi);
				checkboard(fi);
				printinfo(fi);
			}

			if (removelastcat())
				break; //Finished. Out of main loop.

			//Increment the current position:
			currx++;
		}

		if (callcount%1000==0)
		{
			printf("%d calls to advance1gen().\n", callcount);
			printinfo(stdout);
			if (tofile)
			{
				fprintf(fi, "%d calls to advance1gen().\n", callcount);
				printinfo(fi);
			}
		}
	}

	printf("The end.\n%d call%s to advance1gen()\n"
		"%d pattern%s printed.\n%d pattern%s matched target.\n",
		callcount, callcount==1?"":"s",
		numprinted, numprinted==1?"":"s",
		nummatched, nummatched==1?"":"s");
	if (tofile)
		fprintf(fi, "The end.\n%d call%s to advance1gen()\n"
			"%d pattern%s printed.\n%d pattern%s matched target.\n",
			callcount, callcount==1?"":"s",
			numprinted, numprinted==1?"":"s",
			nummatched, nummatched==1?"":"s");

#if Profilea
	ProfilerDump("\pprofile");
	ProfilerTerm();
#endif

	return 0;
} //main()

/* This function advances the pattern 1 generation and checks that nothing
of this occurs:
- A 'fixed' cell changes
- The pattern reaches the edge of the board

If one of these occurs the function returns 1.
*/
int advance1gen(void)
{
	int x, y, xtemp, ytemp;

	callcount++;

	if (currgen==MAXGENS)
	{ printf("Error in advance1gen(): Too many generations.\n"); exit(1); }

	do
	{
		if (stack[currgen].xmin == 1)
		{
			xtemp=2;
			for (ytemp=2; ytemp<SZ-2; ytemp++)
			{
				if (stack[currgen].now[xtemp][ytemp] & LiveBit)
				{
					/* the three cells (besides the leading cell) that must be on in any glider */
					if (!(stack[currgen].now[xtemp+1][ytemp] &
						stack[currgen].now[xtemp+2][ytemp+1] &
						stack[currgen].now[xtemp+2][ytemp-1] & LiveBit)) break;
					/* one of these two cells must be on, depending on glider direction */
					if (!((stack[currgen].now[xtemp+1][ytemp-1] ^ stack[currgen].now[xtemp+1][ytemp+1]) & LiveBit)) break;
					/* other neigboring cells must all be off */
					if ((stack[currgen].now[xtemp][ytemp+1] | stack[currgen].now[xtemp][ytemp+2] |
						stack[currgen].now[xtemp+1][ytemp+2] | stack[currgen].now[xtemp+2][ytemp+2] |
						stack[currgen].now[xtemp+3][ytemp+2] | stack[currgen].now[xtemp+3][ytemp+1] |
						stack[currgen].now[xtemp+3][ytemp]) & LiveBit) break;
					if ((stack[currgen].now[xtemp][ytemp-1] | stack[currgen].now[xtemp][ytemp-2] |
						stack[currgen].now[xtemp+1][ytemp-2] | stack[currgen].now[xtemp+2][ytemp-2] |
						stack[currgen].now[xtemp+3][ytemp-2] | stack[currgen].now[xtemp+3][ytemp-1] |
						stack[currgen].now[xtemp+2][ytemp]) & LiveBit) break;
					/* pattern matches a glider with 1-cell empty boundary -- not quite certain to persist,
					   but good enough.  Clear glider pattern and return a match for this cell */
					stack[currgen].now[xtemp][ytemp] = 1;
					stack[currgen].now[xtemp][ytemp-1] = 1;
					stack[currgen].now[xtemp][ytemp+1] = 1;
					stack[currgen].now[xtemp+1][ytemp] = 1;
					stack[currgen].now[xtemp+1][ytemp+1] = 1;
					stack[currgen].now[xtemp+1][ytemp-1] = 1;
					stack[currgen].now[xtemp+2][ytemp+1] = 1;
					stack[currgen].now[xtemp+2][ytemp-1] = 1;

					stack[currgen].history[xtemp-1][ytemp-1] = 1;
					stack[currgen].history[xtemp-1][ytemp] = 1;
					stack[currgen].history[xtemp-1][ytemp+1] = 1;
					stack[currgen].now[xtemp-1][ytemp-1] = 1;
					stack[currgen].now[xtemp-1][ytemp] = 1;
					stack[currgen].now[xtemp-1][ytemp+1] = 1;

					stack[currgen].numgliders++;
					stack[currgen].xmin++;
				}
			}
		}
		if (stack[currgen].xmax == SZ-2)
		{
			xtemp=SZ-3;
			for (ytemp=2; ytemp<SZ-2; ytemp++)
			{
				if (stack[currgen].now[xtemp][ytemp] & LiveBit)
				{
					/* the three cells (besides the leading cell) that must be on in any glider */
					if (!(stack[currgen].now[xtemp-1][ytemp] &
						stack[currgen].now[xtemp-2][ytemp+1] &
						stack[currgen].now[xtemp-2][ytemp-1] & LiveBit)) break;
					/* one of these two cells must be on, depending on glider direction */
					if (!((stack[currgen].now[xtemp-1][ytemp-1] ^ stack[currgen].now[xtemp-1][ytemp+1]) & LiveBit)) break;
					/* other neigboring cells must all be off */
					if ((stack[currgen].now[xtemp][ytemp+1] | stack[currgen].now[xtemp][ytemp+2] |
						stack[currgen].now[xtemp-1][ytemp+2] | stack[currgen].now[xtemp-2][ytemp+2] |
						stack[currgen].now[xtemp-3][ytemp+2] | stack[currgen].now[xtemp-3][ytemp+1] |
						stack[currgen].now[xtemp-3][ytemp]) & LiveBit) break;
					if ((stack[currgen].now[xtemp][ytemp-1] | stack[currgen].now[xtemp][ytemp-2] |
						stack[currgen].now[xtemp-1][ytemp-2] | stack[currgen].now[xtemp-2][ytemp-2] |
						stack[currgen].now[xtemp-3][ytemp-2] | stack[currgen].now[xtemp-3][ytemp-1] |
						stack[currgen].now[xtemp-2][ytemp]) & LiveBit) break;
					/* pattern matches a glider with 1-cell empty boundary -- not quite certain to persist,
					   but good enough.  Clear glider pattern and return a match for this cell */
					stack[currgen].now[xtemp][ytemp] = 1;
					stack[currgen].now[xtemp][ytemp-1] = 1;
					stack[currgen].now[xtemp][ytemp+1] = 1;
					stack[currgen].now[xtemp-1][ytemp] = 1;
					stack[currgen].now[xtemp-1][ytemp+1] = 1;
					stack[currgen].now[xtemp-1][ytemp-1] = 1;
					stack[currgen].now[xtemp-2][ytemp+1] = 1;
					stack[currgen].now[xtemp-2][ytemp-1] = 1;

					stack[currgen].history[xtemp+1][ytemp-1] = 1;
					stack[currgen].history[xtemp+1][ytemp] = 1;
					stack[currgen].history[xtemp+1][ytemp+1] = 1;
					stack[currgen].now[xtemp+1][ytemp-1] = 1;
					stack[currgen].now[xtemp+1][ytemp] = 1;
					stack[currgen].now[xtemp+1][ytemp+1] = 1;

					stack[currgen].numgliders++;
					stack[currgen].xmax--;
				}
			}
		}
		if (stack[currgen].ymin == 1)
		{
			ytemp=2;
			for (xtemp=2; xtemp<SZ-2; xtemp++)
			{
				if (stack[currgen].now[xtemp][ytemp] & LiveBit)
				{
					/* the three cells (besides the leading cell) that must be on in any glider */
					if (!(stack[currgen].now[xtemp][ytemp+1] &
						stack[currgen].now[xtemp+1][ytemp+2] &
						stack[currgen].now[xtemp-1][ytemp+2] & LiveBit)) break;
					/* one of these two cells must be on, depending on glider direction */
					if (!((stack[currgen].now[xtemp-1][ytemp+1] ^ stack[currgen].now[xtemp+1][ytemp+1]) & LiveBit))
						break;
					/* other neigboring cells must all be off */
					if ((stack[currgen].now[xtemp+1][ytemp] | stack[currgen].now[xtemp+2][ytemp] |
						stack[currgen].now[xtemp+2][ytemp+1] | stack[currgen].now[xtemp+2][ytemp+2] |
						stack[currgen].now[xtemp+2][ytemp+3] | stack[currgen].now[xtemp+1][ytemp+3] |
						stack[currgen].now[xtemp][ytemp+3]) & LiveBit) break;
					if ((stack[currgen].now[xtemp-1][ytemp] | stack[currgen].now[xtemp-2][ytemp] |
						stack[currgen].now[xtemp-2][ytemp+1] | stack[currgen].now[xtemp-2][ytemp+2] |
						stack[currgen].now[xtemp-2][ytemp+3] | stack[currgen].now[xtemp-1][ytemp+3] |
						stack[currgen].now[xtemp][ytemp+2]) & LiveBit) break;
					/* pattern matches a glider with 1-cell empty boundary -- not quite certain to persist,
					   but good enough.  Clear glider pattern and return a match for this cell */
					stack[currgen].now[xtemp][ytemp] = 1;
					stack[currgen].now[xtemp-1][ytemp] = 1;
					stack[currgen].now[xtemp+1][ytemp] = 1;
					stack[currgen].now[xtemp][ytemp+1] = 1;
					stack[currgen].now[xtemp+1][ytemp+1] = 1;
					stack[currgen].now[xtemp-1][ytemp+1] = 1;
					stack[currgen].now[xtemp+1][ytemp+2] = 1;
					stack[currgen].now[xtemp-1][ytemp+2] = 1;

					stack[currgen].history[xtemp-1][ytemp-1] = 1;
					stack[currgen].history[xtemp][ytemp-1] = 1;
					stack[currgen].history[xtemp+1][ytemp-1] = 1;
					stack[currgen].now[xtemp-1][ytemp-1] = 1;
					stack[currgen].now[xtemp][ytemp-1] = 1;
					stack[currgen].now[xtemp+1][ytemp-1] = 1;

					stack[currgen].numgliders++;
					stack[currgen].ymin++;
				}
			}
		}
		if (stack[currgen].ymax == SZ-2)
		{
			ytemp=SZ-3;
			for (xtemp=2; xtemp<SZ-2; xtemp++)
			{
				if (stack[currgen].now[xtemp][ytemp] & LiveBit)
				{
					/* the three cells (besides the leading cell) that must be on in any glider */
					if (!(stack[currgen].now[xtemp][ytemp-1] &
						stack[currgen].now[xtemp+1][ytemp-2] &
						stack[currgen].now[xtemp-1][ytemp-2] & LiveBit)) break;
					/* one of these two cells must be on, depending on glider direction */
					if (!((stack[currgen].now[xtemp-1][ytemp-1] ^ stack[currgen].now[xtemp+1][ytemp-1]) & LiveBit))
						break;
					/* other neigboring cells must all be off */
					if ((stack[currgen].now[xtemp+1][ytemp] | stack[currgen].now[xtemp+2][ytemp] |
						stack[currgen].now[xtemp+2][ytemp-1] | stack[currgen].now[xtemp+2][ytemp-2] |
						stack[currgen].now[xtemp+2][ytemp-3] | stack[currgen].now[xtemp+1][ytemp-3] |
						stack[currgen].now[xtemp][ytemp-3]) & LiveBit) break;
					if ((stack[currgen].now[xtemp-1][ytemp] | stack[currgen].now[xtemp-2][ytemp] |
						stack[currgen].now[xtemp-2][ytemp-1] | stack[currgen].now[xtemp-2][ytemp-2] |
						stack[currgen].now[xtemp-2][ytemp-3] | stack[currgen].now[xtemp-1][ytemp-3] |
						stack[currgen].now[xtemp][ytemp-2]) & LiveBit) break;
					/* pattern matches a glider with 1-cell empty boundary -- not quite certain to persist,
					   but good enough.  Clear glider pattern and return a match for this cell */
					stack[currgen].now[xtemp][ytemp] = 1;
					stack[currgen].now[xtemp-1][ytemp] = 1;
					stack[currgen].now[xtemp+1][ytemp] = 1;
					stack[currgen].now[xtemp][ytemp-1] = 1;
					stack[currgen].now[xtemp+1][ytemp-1] = 1;
					stack[currgen].now[xtemp-1][ytemp-1] = 1;
					stack[currgen].now[xtemp+1][ytemp-2] = 1;
					stack[currgen].now[xtemp-1][ytemp-2] = 1;

					stack[currgen].history[xtemp-1][ytemp+1] = 1;
					stack[currgen].history[xtemp][ytemp+1] = 1;
					stack[currgen].history[xtemp+1][ytemp+1] = 1;
					stack[currgen].now[xtemp-1][ytemp+1] = 1;
					stack[currgen].now[xtemp][ytemp+1] = 1;
					stack[currgen].now[xtemp+1][ytemp+1] = 1;

					stack[currgen].numgliders++;
					stack[currgen].ymax--;
				}
			}
		}
		break;
		/* what's the proper way to do this kind of thing, anyway? */
	}
	while(1);

	if (stack[currgen].xmin<=1 || stack[currgen].xmax>= SZ-2 ||
	    stack[currgen].ymin<=1 || stack[currgen].ymax>= SZ-2)
	    return 1; //Edge of the board reached.

	stack[currgen+1].xmin=SZ;
	stack[currgen+1].xmax=0;
	stack[currgen+1].ymin=SZ;
	stack[currgen+1].ymax=0;

	//We have to clear additional space around the pattern because it may
	//contain junk from before, and the function placecatalyst() sometimes
	//expands the boundaries without clearing.
	int xstart=stack[currgen].xmin-1-CATSZ,
		ystart=stack[currgen].ymin-1-CATSZ;
	if (xstart<1) xstart=1;
	if (ystart<1) ystart=1;
	for (x=xstart; x<=stack[currgen].xmax+1+CATSZ && x<SZ-1; x++)
		for (y=ystart; y<=stack[currgen].ymax+1+CATSZ && y<SZ-1; y++)
		{
			if (x<stack[currgen].xmin-1 || x>stack[currgen].xmax+1 ||
				y<stack[currgen].ymin-1 || y>stack[currgen].ymax+1)
			{
				stack[currgen+1].now[x][y]= 1<<0;
				stack[currgen+1].history[x][y]= 1<<0;
				continue;
			}

			//Set the cell itself's next generation:
			if(WillLive(stack[currgen].now[x][y]))
				stack[currgen+1].now[x][y] = LiveBit;
			else
				stack[currgen+1].now[x][y] = 0;

			//Count number of the live neighbors the cell will have the next
			//generation:
			int count=0;
			if (WillLive(stack[currgen].now[x-1][y-1])) count++;
			if (WillLive(stack[currgen].now[x-1][y  ])) count++;
			if (WillLive(stack[currgen].now[x-1][y+1])) count++;
			if (WillLive(stack[currgen].now[x  ][y-1])) count++;
			if (WillLive(stack[currgen].now[x  ][y+1])) count++;
			if (WillLive(stack[currgen].now[x+1][y-1])) count++;
			if (WillLive(stack[currgen].now[x+1][y  ])) count++;
			if (WillLive(stack[currgen].now[x+1][y+1])) count++;

			//If it's a fixed cell, check that it will not change 2 generations
			//from now. We assume that it has already been checked that it will
			//not change next generation:
			if (fixed[x][y] &&
				(((stack[currgen].now[x][y] & LiveBit) && count!=2 && count!=3) ||
				((stack[currgen].now[x][y] & LiveBit)==0 && count==3)))
				return 1;

			//Set the cell's count bit:
			stack[currgen+1].now[x][y] |= 1<<count;

			//Also set the next generation's history board:
			stack[currgen+1].history[x][y] = stack[currgen].history[x][y] |
				stack[currgen].now[x][y];

			//Adjust next gen's boundary variables if necessary.
			//Note that the pattern's boundaries will never become smaller than
			//in a previous generation, because of history[][]:
			if ((stack[currgen+1].now[x][y] & (~1)) ||
				(stack[currgen+1].history[x][y] & (~1)))
			{
				if (x < stack[currgen+1].xmin) stack[currgen+1].xmin=x;
				if (x > stack[currgen+1].xmax) stack[currgen+1].xmax=x;
				if (y < stack[currgen+1].ymin) stack[currgen+1].ymin=y;
				if (y > stack[currgen+1].ymax) stack[currgen+1].ymax=y;
			}
		} //for for

	stack[currgen+1].numgliders=stack[currgen].numgliders;
	currgen++;
	currx=curry=currcatn=currorient=0;
	return 0;
} //advance1gen()

/* This function looks for a place to place a catalyst on this generation's
board, starting from the position specified by the globals currx, curry,
currorient, and currcatn, and going ahead. It makes sure that the
catalyst would not have reacted at any previous generation. It also makes
sure that the catalyst will react now, i.e. next generation.
*/
int placecatalyst()
{
	int catszx, catszy;
	char catcell;

	while (currcatn<NCATS)
	{
	//Skip this catalyst if it is deactivated:
	if (!catisused[currcatn])
	{
		currorient=0;
		currcatn++;
		continue;
	}

	while (currorient<8)
	{
	//Skip some orientations for symmetric patterns:
	if (cata[currcatn].name=='eat2')
		if (currorient>=4)
			break;
	if (cata[currcatn].name=='bloc' || cata[currcatn].name=='_tub')
		if (currorient==1 || currorient==3 || currorient==5 || currorient==7)
		{
			curry=0;
			currorient++;
			continue;
		}

	if (currorient<4)
	{
		catszy=cata[currcatn].y;
		catszx=cata[currcatn].x;
	}
	else
	{
		catszy=cata[currcatn].x;
		catszx=cata[currcatn].y;
	}
	if (curry<stack[currgen].ymin - catszy)
		curry=stack[currgen].ymin - catszy;

	while (curry<SZ-catszy && curry<=stack[currgen].ymax + catszy)
	{
	if (currx<stack[currgen].xmin - catszx)
		currx=stack[currgen].xmin - catszx;

	while (currx<SZ-catszx && currx<=stack[currgen].xmax + catszx)
	{
		int x, y, reacts=0, isgood=1;

		//Check the catalyst in this position cell by cell:
		for (x=0; x<catszx && isgood; x++)
		for (y=0; y<catszy && isgood; y++)
		{
		//Select the cell according to the orientation:
		if      (currorient==0) catcell=cata[currcatn].c[         x][         y];
		else if (currorient==1) catcell=cata[currcatn].c[catszx-1-x][         y];
		else if (currorient==2) catcell=cata[currcatn].c[         x][catszy-1-y];
		else if (currorient==3) catcell=cata[currcatn].c[catszx-1-x][catszy-1-y];
		else if (currorient==4) catcell=cata[currcatn].c[         y][         x];
		else if (currorient==5) catcell=cata[currcatn].c[catszy-1-y][         x];
		else if (currorient==6) catcell=cata[currcatn].c[         y][catszx-1-x];
		else                    catcell=cata[currcatn].c[catszy-1-y][catszx-1-x];

		if (catcell=='o' || catcell=='*')
			if ((stack[currgen].history[currx+x][curry+y] != 1<<0) ||
				(fixed[currx+x][curry+y] > 0))
			{ isgood=0; continue; }

		if (catcell=='.' || catcell=='1' || catcell=='x')
			if (stack[currgen].history[currx+x][curry+y] &
				(LiveBit | (1<<2) | (1<<3)))
			{ isgood=0; continue; }

		if (catcell=='$' || catcell=='%' || catcell=='^')
			if (stack[currgen].history[currx+x][curry+y] & LiveBit)
			{ isgood=0; continue; }

		if (catcell==':' || catcell=='2' || catcell=='X')
			if (stack[currgen].history[currx+x][curry+y] &
				(LiveBit | (1<<1) | (1<<3)))
			{ isgood=0; continue; }

		if (catcell=='1')
			if ((stack[currgen].now[currx+x][curry+y] & CountBitMask) == (1<<2))
				reacts=1;

		if (catcell=='2')
			if ((stack[currgen].now[currx+x][curry+y] & CountBitMask) == (1<<1))
				reacts=1;

		if (catcell=='x')
			if ((stack[currgen].now[currx+x][curry+y] & CountBitMask) == (1<<2))
			{ isgood=0; continue; }

		if (catcell=='X')
			if ((stack[currgen].now[currx+x][curry+y] & CountBitMask) == (1<<1))
			{ isgood=0; continue; }

		//Reject also if the catalyst will cause a birth in a fixed cell:
		if (fixed[currx+x][curry+y] && (catcell=='.' || catcell=='1') &&
			(stack[currgen].now[currx+x][curry+y] & CountBitMask) == (1<<2))
			{ isgood=0; continue; }

		if (fixed[currx+x][curry+y] && (catcell==':' || catcell=='2') &&
			(stack[currgen].now[currx+x][curry+y] & CountBitMask) == (1<<1))
			{ isgood=0; continue; }
		} //for for

		if (isgood && reacts)
		{
			//Save the current values of the boundary variables:
			catplaced[nCatsTotal].oldxmin=stack[currgen].xmin;
			catplaced[nCatsTotal].oldxmax=stack[currgen].xmax;
			catplaced[nCatsTotal].oldymin=stack[currgen].ymin;
			catplaced[nCatsTotal].oldymax=stack[currgen].ymax;
			//Save the current boundaries of boardgen0[][]:
			catplaced[nCatsTotal].g0oldminx=g0minx;
			catplaced[nCatsTotal].g0oldminy=g0miny;
			catplaced[nCatsTotal].g0oldmaxx=g0maxx;
			catplaced[nCatsTotal].g0oldmaxy=g0maxy;

			//Place the catalyst on the board.
			//Also, modify the history board as if the
			//catalyst was always there.
			//Also place the catalyst on boardgen0[][]:
			for (x=0; x<catszx; x++)
			for (y=0; y<catszy; y++)
			{
			if      (currorient==0) catcell=cata[currcatn].c[         x][         y];
			else if (currorient==1) catcell=cata[currcatn].c[catszx-1-x][         y];
			else if (currorient==2) catcell=cata[currcatn].c[         x][catszy-1-y];
			else if (currorient==3) catcell=cata[currcatn].c[catszx-1-x][catszy-1-y];
			else if (currorient==4) catcell=cata[currcatn].c[         y][         x];
			else if (currorient==5) catcell=cata[currcatn].c[catszy-1-y][         x];
			else if (currorient==6) catcell=cata[currcatn].c[         y][catszx-1-x];
			else                    catcell=cata[currcatn].c[catszy-1-y][catszx-1-x];

			//Adjust now[][],  history[][], and boardgen0[][]:
			if (catcell=='o')
			{
				stack[currgen].now[currx+x][curry+y]=LiveBit+(1<<3);
				stack[currgen].history[currx+x][curry+y]=LiveBit+(1<<3);
				boardgen0[currx+x][curry+y]=2;
			}
			//It doesn't necessarily have 3 neighbors, but it doesn't matter.

			if (catcell=='*')
			{
				stack[currgen].now[currx+x][curry+y]=LiveBit+(1<<3);
				stack[currgen].history[currx+x][curry+y]=LiveBit+(1<<3);
				boardgen0[currx+x][curry+y]=2;
				fixed[currx+x][curry+y]++;
			}

			//Adjust the boundaries of boardgen0[][]:
			if (catcell=='o' || catcell=='*' || catcell=='x' || catcell=='X')
			{
				if (currx+x < g0minx) g0minx=currx+x;
				if (currx+x > g0maxx) g0maxx=currx+x;
				if (curry+y < g0miny) g0miny=curry+y;
				if (curry+y > g0maxy) g0maxy=curry+y;
			}

			if (catcell=='.' || catcell=='1' || catcell=='x')
			{
				stack[currgen].now[currx+x][curry+y] <<= 1;
				stack[currgen].history[currx+x][curry+y] <<= 1;
			}

			if (catcell==':' || catcell=='2' || catcell=='X')
			{
				stack[currgen].now[currx+x][curry+y] <<= 2;
				stack[currgen].history[currx+x][curry+y] <<= 2;
			}

			if (catcell=='$')
			{
				stack[currgen].now[currx+x][curry+y] <<= 4;
				stack[currgen].history[currx+x][curry+y] <<= 4;
			}

			if (catcell=='%')
			{
				stack[currgen].now[currx+x][curry+y] <<= 5;
				stack[currgen].history[currx+x][curry+y] <<= 5;
			}

			if (catcell=='^')
			{
				stack[currgen].now[currx+x][curry+y] <<= 6;
				stack[currgen].history[currx+x][curry+y] <<= 6;
			}

			if (catcell=='x' || catcell=='X')
				fixed[currx+x][curry+y]++;

			//Adjust the boundary variables if necessary:
			if (catcell != ' ')
			{
				if (currx+x < stack[currgen].xmin)
					stack[currgen].xmin=currx+x;
				if (currx+x > stack[currgen].xmax)
					stack[currgen].xmax=currx+x;
				if (curry+y < stack[currgen].ymin)
					stack[currgen].ymin=curry+y;
				if (curry+y > stack[currgen].ymax)
					stack[currgen].ymax=curry+y;
			}
			} //for for

			//Record the placement:
			catplaced[nCatsTotal].x=currx;
			catplaced[nCatsTotal].y=curry;
			catplaced[nCatsTotal].n=currcatn;
			catplaced[nCatsTotal].orient=currorient;
			catplaced[nCatsTotal].gen=currgen;
			nCatsTotal++;
			stack[currgen].numcats++;

			return 1;
		} //isgood && reacts
		currx++;
	} //while currx
	currx=0;
	curry++;
	} //while curry
	curry=0;
	currorient++;
	} //while currorient
	currorient=0;
	currcatn++;
	} //while currcatn
	return 0; //No way to place a catalyst
} //placecatalyst()

/* This function removes the last catalyst that was placed, according to
the array catplaced[]. It backs up to the generation when that catalyst
was placed. It returns 1 if there are no catalysts to remove.
*/
int removelastcat()
{
	if (nCatsTotal==0)
		return 1;
	nCatsTotal--;

	currgen=catplaced[nCatsTotal].gen;
	currx=catplaced[nCatsTotal].x;
	curry=catplaced[nCatsTotal].y;
	currcatn=catplaced[nCatsTotal].n;
	currorient=catplaced[nCatsTotal].orient;

	stack[currgen].numcats--;

	int catszx, catszy, x, y;
	char catcell;

	if (currorient<4)
	{
		catszy=cata[currcatn].y;
		catszx=cata[currcatn].x;
	}
	else
	{
		catszy=cata[currcatn].x;
		catszx=cata[currcatn].y;
	}

	//Undo the placement of the catalyst, by restoring the values of
	//new[][] and history[][].
	//Also, remove the catalyst from boardgen0[][]:
	for (x=0; x<catszx; x++)
		for (y=0; y<catszy; y++)
		{
			if      (currorient==0) catcell=cata[currcatn].c[         x][         y];
			else if (currorient==1) catcell=cata[currcatn].c[catszx-1-x][         y];
			else if (currorient==2) catcell=cata[currcatn].c[         x][catszy-1-y];
			else if (currorient==3) catcell=cata[currcatn].c[catszx-1-x][catszy-1-y];
			else if (currorient==4) catcell=cata[currcatn].c[         y][         x];
			else if (currorient==5) catcell=cata[currcatn].c[catszy-1-y][         x];
			else if (currorient==6) catcell=cata[currcatn].c[         y][catszx-1-x];
			else                    catcell=cata[currcatn].c[catszy-1-y][catszx-1-x];

			if (catcell=='o' || catcell=='*')
			{
				stack[currgen].now[currx+x][curry+y]= 1<<0;
				stack[currgen].history[currx+x][curry+y]= 1<<0;
				boardgen0[currx+x][curry+y]=0;
			}

			if (catcell=='*')
			{
				stack[currgen].now[currx+x][curry+y]= 1<<0;
				stack[currgen].history[currx+x][curry+y]= 1<<0;
				boardgen0[currx+x][curry+y]=0;
				fixed[currx+x][curry+y]--;
				if (fixed[currx+x][curry+y]<0)
				{
					printf("Error 1 in removelastcat(): fixed[%d][%d] < 0.\n",
						currx+x, curry+y);
					exit(1);
				}
			}

			if (catcell=='x' || catcell=='X')
			{
				fixed[currx+x][curry+y]--;
				if (fixed[currx+x][curry+y]<0)
				{
					printf("Error 2 in removelastcat(): fixed[%d][%d] < 0.\n",
						currx+x, curry+y);
					exit(1);
				}
			}

			if (catcell=='.' || catcell=='1' || catcell=='x')
			{
				stack[currgen].now[currx+x][curry+y] >>= 1;
				stack[currgen].history[currx+x][curry+y] >>= 1;
			}

			if (catcell==':' || catcell=='2' || catcell=='X')
			{
				stack[currgen].now[currx+x][curry+y] >>= 2;
				stack[currgen].history[currx+x][curry+y] >>= 2;
			}

			if (catcell=='$')
			{
				stack[currgen].now[currx+x][curry+y] >>= 4;
				stack[currgen].history[currx+x][curry+y] >>= 4;
			}

			if (catcell=='%')
			{
				stack[currgen].now[currx+x][curry+y] >>= 5;
				stack[currgen].history[currx+x][curry+y] >>= 5;
			}

			if (catcell=='^')
			{
				stack[currgen].now[currx+x][curry+y] >>= 6;
				stack[currgen].history[currx+x][curry+y] >>= 6;
			}
		} //for for

	//Restore the boundary variables:
	stack[currgen].xmin=catplaced[nCatsTotal].oldxmin;
	stack[currgen].xmax=catplaced[nCatsTotal].oldxmax;
	stack[currgen].ymin=catplaced[nCatsTotal].oldymin;
	stack[currgen].ymax=catplaced[nCatsTotal].oldymax;
	//Restore boardgen0[][]'s boundaries:
	g0minx=catplaced[nCatsTotal].g0oldminx;
	g0miny=catplaced[nCatsTotal].g0oldminy;
	g0maxx=catplaced[nCatsTotal].g0oldmaxx;
	g0maxy=catplaced[nCatsTotal].g0oldmaxy;

	return 0;
} //removelastcat()

void printgen(int gen)
{
	int x, y;

	for (y=stack[gen].ymin; y<=stack[gen].ymax; y++)
	{
		for (x=stack[gen].xmin; x<=stack[gen].xmax; x++)
			if (stack[gen].now[x][y] & LiveBit)
				if (fixed[x][y]) printf("*");
				else printf("o");
			else
				if (fixed[x][y]) printf(",");
				else printf(".");
		printf("\n");
	}
//	printf("Catalysts placed at gens:");
//	for (int n=0; n<nCatsTotal; n++)
//		printf(" %d", catplaced[n].gen);
	printf("\nGeneration %d\n   -----\n", gen);
} //printgen()

void printboard(FILE *f)
{
	int x, y;
	char ch;

	for (y=g0miny; y<=g0maxy; y++)
	{
		for (x=g0minx; x<=g0maxx; x++)
			//Fix this:
			if (boardgen0[x][y])
				if (fixed[x][y]) fprintf(f, "*");
				else fprintf(f, "o");
			else
				if (fixed[x][y]) fprintf(f, ",");
				else fprintf(f, ".");

		fprintf(f, "\n");
	}

	fprintf(f,"\nFinal position:\n");
	for (y=stack[currgen].ymin; y<=stack[currgen].ymax; y++)
	{
		for (x=stack[currgen].xmin; x<=stack[currgen].xmax; x++)
			if (stack[currgen].now[x][y] & LiveBit) fprintf(f, "*");
			else fprintf(f,".");

		fprintf(f, "\n");
	}
fprintf(f, "\n%d glider%s escaped.",stack[currgen].numgliders, stack[currgen].numgliders==1?"":"s");

for (x=1; x==currgen; x++)
{
	printgen(x);
	do { scanf("%c", &ch); } while (ch!='\n');
}
} //printboard()

void checkboard(FILE *f)
{
	int x, y, z;

	z=0;

	for (y=g0miny; y<=g0maxy; y++)
	{
		// check for any mismatches with target pattern
		for (x=g0minx; x<=g0maxx; x++)
			if (((stack[currgen].now[x][y] & LiveBit) && (targetgen0[x][y] == 1)) ||
				(((stack[currgen].now[x][y] & LiveBit) == 0) && (targetgen0[x][y] == 2))) z=1;

			//if (stack[currgen].now[x][y] & LiveBit)
			//{
			//	if (target[x][y] == 1) z=1;
			//}
			//else if (target[x][y] == 2) z=1;
	}
	if (z == 0)
	{
		fprintf(f, "\nPattern matched target!\n");
		nummatched++;
	}
} //checkboard()

void printinfo(FILE *f)
{
	int n;

	fprintf(f, "%d catalyst%s", nCatsTotal, nCatsTotal==1?"":"s");
	if (nCatsTotal>0)
	{
		fprintf(f, ", which react%s", nCatsTotal==1 ? "s at gen." : " at gens.:");
		for (n=0; n<nCatsTotal; n++)
			fprintf(f, " %d", catplaced[n].gen);
	}
	else
		fprintf(f, ".");
	fprintf(f, "\nGeneration reached: %d\n   -----\n", currgen);
} //printinfo()
