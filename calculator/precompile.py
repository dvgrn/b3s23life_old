# This is a precompile functionality for APGompiler.py
# Prepare T and R registers to have initial state. 
# Precompiles current GPC textual data for 99 bottles
# Michael Simkin 2019 

import golly as g 

blck = g.parse("2o$2o!")
boat = g.parse("bo$obo$b2o!")

#Use movement block as center (dx, dy)
def setupR(val, dx, dy):
	g.select([dx, dy, 2, 2])
	g.clear(0)
	g.putcells(blck, dx - val, dy - val)
	
#Use head of slider gun block as center for (dx, dy)
def setupT(dhead, binaryStr, dx, dy):
	setupR(dhead, dx, dy)
	setupR(len(binaryStr) - 1 - dhead, dx + 310, dy - 506)
	setupR(dhead * 16, dx + 130, dy - 3286)
	setupR(dhead * 16, dx - 1113, dy - 2062)

	if len(binaryStr) == 0:
		return 
		
	x = dx + 142
	y = dy - 3305
	g.select([x, y, 3, 3])
	g.clear(0)

	for i in range(len(binaryStr)):
		if binaryStr[i] == '0':
			g.putcells(boat, x, y)
		else:
			g.putcells(boat, x - 3, y - 3)
			
		x -= 16 
		y -= 16

def setRegs(registers):
	T0x = 65281 
	T0y = 29180
	Td = 2560 

	R0x = 16608
	R0y = 79397
	Rd = 1024

	for reg in registers:
		if reg[0] == 'T':
			dreg = int(reg.replace("T", ""))
			dx = T0x - dreg * Td
			dy = T0y + dreg * Td
			setupT(registers[reg][0], registers[reg][1], dx, dy)
		if reg[0] == 'R':
			dreg = int(reg.replace("R", ""))
			dx = R0x - dreg * Rd
			dy = R0y + dreg * Rd
			setupR(registers[reg], dx, dy)
			
registers = {'R3':9, 'R2':1, 'R4':9, 'R5':0, 'R6':1, 'R8':10, 'T6': [0, '010010010010010010100111011111011111011111011111011100111010010010010111010010111100111011011011111011011011111100111010010111010010010010111100011111011111011111011111011111100100011011100000100100100100100100101001110110110110110111110111001110101110101110101110101110101110101111001110110110111001000110110110111000001001001001001001001010011101101101101101111101110011101001001001001011101011110011101101111101101101101111110011101001001011101001001011110011101101101101111101111110010001101110000010010010010010010100111011011011011011111100111010010010010010010111100111011011011011111011011111100111010111010010111010010010111100011111011111011011011011111100100011100000100100100100101001110111110111001110100101111001110110110111110111001110101110101110101110101110101110101111000110111110111001000110110110111000001001001001001001010011101101101111101111101111110011101001011101001001001011110011101101101101111101101111110011101001011101001001001011110001111101111101111101101101111110010001110000010010010010010010100111011111011111011111011100111010010111010010010111100111011011011111011011011111100111010010010111010010010111100011111011111011100100011011011011100000101001111001110100100100101110101110101111000110110111110110110111111001110100101111000111110111111001000111000001001001001001001010011101111101101111101111101110011101001001011101001001011110011101101101111101101101111110011101001001011101001001011110001111101111101101111101111110010001101110000010010010100111011111011100111010010010111010010010111100111011011011111011011011111100111010010010111010010111100011111011111011111011111100100011011100001001001001001001000001010011110011101001001001001001010011101111101111101111101111101111101111110011110011110010001110000010010010010010010010100111011111011111011111011111011111011111100010010111010100111100010111010010100111011111011111011111011111011111011111100100011100000100100100100100101001110111110111110111110111110111001110100100100100100101111001110110110111110110110111111001110100100101110100100101111001110111110111110111110110111111001000110111000001001001001001001010011101101101110011101001011101001011110011101101111101101111110011101001011101001011110011101111101111101111110010001101101101110000010010010010010010010100111011111011111011111011111011111011111100010010010111010010010111100111011011011011111100111010010010010111100011111011111011111100100011011011011100000100100100100100101001110111110111110111001110100100100101111001110110110110111111001110100100100101111000111110110111001000110110110111000001001001001001001010011101111101111101110011101001001001011110011101101101101111110001011101001001011110011101111101111101111101111101111101111110010001110000010010010010010010100111011111011111011100111010010111010010111100111011011111011011111100111010010111010010111100011011111011111100100011011011011100000100100100101001110110110111001110101110101110101110101110101110101111000110110111110110110110111111001110101001111001000111000001001001001010011101111101110011101001001011101001011110011101101111101101101111110011101001001011101001011110001111101111101111101111101111110010001101110000010010010010010010010100111011111011111011111011111011111011111100010010010111100011111100111010010010010100111011111011111011111100100011011011011100000100100100100100100101001110110110110111110110111001110100101110101110101110101110101111001110110110111001000110110110111000001001001001001001010011110001011110011101101101101101101110011101001011101011101011101011110001101101101101101110000010010010010010010010100111011111011111011111011111011111011111100010010010010111010100111011011111011100111010010010010111100011011011011011011011100000100100100100100100101001110110110110110110111111001110101110101110101110101110101110101111001110110110111001000110110110111000001001001001001001001010011101111101111101111101111110011101001010011101111101110011101001001001010011101111101111101111110010001101101101110000010010010010010010010100111011111011111011111011111100010111100011111100111010010010010100111011111011111011111100100011011011011100000100100100100100101001110111110111110111001110100100100101111001110110110110111111001110100100100101111000111110111110111111001000110110110111000001001001001001001001010011101111101111101111101111110011101001011110011101101111110011101001011110001111110010001101101101110000010010010010100111011100111010010111100111011011111100010111010111010010100111011111011111011111011111100100011011011100000100100100100100100101001110111110111110111110111111000101111000111111001110101001111001000110110110111000001001001001001001001010011101101101111101110011101001011101001011110011101101111101101111110011101001011101001011110001111101101110010001101101101110000010010010100111011011100111010111010111010111010111010111010100111011011011011111100010010010010111100011111011011100100011011011011100000100100100100100101001110111110111110111111000100100100101111001111001111000111110111110111110111111001000110110111000001001001001001010011101111101111110001001001011101010011101110011110001111101111101111110010001101101110000010010010010010010100111011111011111011111100010010010010111100011111011111100010010111100011111011111011111011111100100011011011100000100100100100100100101001110110110110111111000101110100101111000111110111001110100101110101001110110110110111111001000110110111000001001001001010011101111110001001011101001011110011101101111110011101001011110001111101111101111101111110010001101101110000010010010010010010010100111011011011011111100111010010010111010111100111011011111011011111100111010111010010010111100111011011011011111100100011011011100000100100100100100100101001110111111001110101111000110110110110110110111000001001001001001001010011110011101011110001101101101101101101110000'], 'T7': [0, '1111111111111110111111111111111111111111111110111111111111111111111111111111111101111111111111111111111111111111111011111111111111111111111111011111111111111111110111111111111111111111111111111111011111111111011111111111111111111111111111011111111111111111111011111111111011111111111111110111111111111111111101111111111111111111011111111111111111111111111111111011111111111011111111111111111111111111111011111111111111111111111111110111111111110111111111111111111111111111111111101111111111111111111111011111111111111111110111111111110111111111111111111111111111111111111101111111111111110111111111111111111111111110111111111111111111111111110111111111111111111111111111111111111111111011111111111001111111111111110111111111111111111111111111110111111111111111111111111111111111101111111111111111111111111111111111011111111111111111111111111011111111111111111110111111111111111111111111111111111011111111111011111111111111111111111111111011111111111111111111011111111111011111111111111110111111111111111111101111111111111111111011111111111111111111111111111111011111111111111111111111111111111111111111001111111111101111111111111110111111111111111111111111101111111111111111111011111111111011111111111111111111111111111011111111111111111111111111110111111111111111111101111111111101111111111111111110111111111111111111111111111110111111111111111111111111111111111111101111111111111111111111111111011111111111011111111111111101111111111111111111111111111011111111111111111101111111111101111111111111111111111111111110111111111111111011111111111111111111111111111111101111111111111111111111111111111110111111111110111111111111111111111110111111111111111111111111111111111101111111111101111111111111110111111111111111111111111111111110111111111111111111111111111110111111111111111111111111111111111110111111111111111111111111111101111111111111111110111111111111111111111111111111111111111111011111111111001111111111111110111111111111111111111111111110111111111111111111111111111111111101111111111111111111111111111111111011111111111111111111111111011111111111111111110111111111111111111111111111111111011111111111011111111111111111111111111111011111111111111111111011111111111011111111111111110111111111111111111101111111111111111111011111111111111111111111111111111011111111111011111111111111111111111111111011111111111111111111111111110111111111110111111111111111111111111111111111101111111111111111111111011111111111111111110111111111110111111111111111111111111111111111111101111111111111110111111111111111111111111110111111111111111111111111110111111111111111111111111111111111111111110011111111111111101111111111111111111111111111101111111111111111111111111111111111011111111111111111111111111111111110111111111111111111111111110111111111111111111101111111111101111111111111111111111111111101111111111111111111101111111111101111111111111111011111111111111111110111111111111111111101111111111111111111111111111111101111111111101111111111111111111111111111101111111111111111111111111111011111111111011111111111111111111111111111111110111111111111111111111101111111111111111111011111111111011111111111111111111111111111111111110111111111111111011111111111111111111111111011111111111111111111111111011111111111111111111111111111111111111111001011111111111011111111111111110111111111111111111111111111110111111111111111111111111111111111101111111111111111111111111111111111011111111111111111111111111011111111111111111110111111111110111111111111111111111111111110111111111111111111110111111111110111111111111111101111111111111111111011111111111111111110111111111111111111111111111111110111111111110111111111111111111111111111110111111111111111111111111111101111111111101111111111111111111111111111111111011111111111111111111110111111111111111111101111111111101111111111111111111111111111111111111011111111111111101111111111111111111111111101111111111111111111111111101111111111111111111111111111111111111111110111111111110110111111111110111111111111111101111111111111111111111111111101111111111111111111111111111111111011111111111111111111111111111111110111111111111111111111111110111111111111111111101111111111101111111111111111111111111111101111111111111111111101111111111101111111111111111011111111111111111110111111111111111111101111111111111111111111111111111101111111111111111111111111111111111111111100111111111110111111111111111011111111111111111111111110111111111111111111101111111111101111111111111111111111111111101111111111111111111111111111011111111111111111110111111111110111111111111111111011111111111111111111111111111011111111111111111111111111111111111110111111111111111111111111111101111111111101111111111111110111111111111111111111111111101111111111111111110111111111110111111111111111111111111111111011111111111111101111111111111111111111111111111110111111111111111111111111111111111011111111111011111111111111111111111011111111111111111111111111111111110111111111110111111111111111011111111111111111111111111111111011111111111111111111111111111011111111111111111111111111111111111011111111111111111111111111110111111111111111111011111111111111111111111111111111111111111101111111111101111111111111111111111111111011111111111111111111111111111011111111111011111111111111111111111111101111111111111111111111111111101111111111111111111111111111111101111111111111111111011111111111011111111111111110111111111111111111111111111110111111111111111111111111111111111101111111111111111111111111111111111011111111111111111111111111011111111111111111110111111111111111111111111111111111011111111111011111111111111111111111111111011111111111111111111011111111111011111111111111110111111111111111111101111111111111111111011111111111111111111111111111111011111111111011111111111111111111111111111011111111111111111111111111110111111111110111111111111111111111111111111111101111111111111111111111011111111111111111110111111111110111111111111111111111111111111111111101111111111111110111111111111111111111111110111111111111111111111111110111111111111111111111111111111111111111110011111111111101111111111111111111111111111101111111111101111111111111111111111111110111111111111111111111111111110111111111111111111111111111111110111111111111111111101111111111101111111111111111011111111111111111111111111111011111111111111111111111111111111110111111111111111111111111111111111101111111111111111111111111101111111111111111111011111111111111111111111111111111101111111111101111111111111111111111111111101111111111111111111101111111111101111111111111111011111111111111111110111111111111111111101111111111111111111111111111111101111111111101111111111111111111111111111101111111111111111111111111111011111111111011111111111111111111111111111111110111111111111111111111101111111111111111111011111111111011111111111111111111111111111111111110111111111111111011111111111111111111111111011111111111111111111111111011111111111111111111111111111111111111111101111111111101111111111111111111111111111011111111111111111111111111111011111111111011111111111111111111111111101111111111111111111111111111101111111111111111111111111111111101111111111111111111011111111111011111111111111110111111111111111111111111111110111111111111111111111111111111111101111111111111111111111111111111111011111111111111111111111111011111111111111111110111111111111111111111111111111111011111111111011111111111111111111111111111011111111111111111111011111111111011111111111111110111111111111111111101111111111111111111011111111111111111111111111111111011111111111111111111111111111111111111111001111111111111011111111111111111111111111111011111111111011111111111111111111111111111111110111111111111111111111111111110111111111110111111111111111111111111111111111101111111111111111111111011111111111111111110111111111110111111111111111111111111111111111011111111111111111111111111111111110111111111111111111111111111110111111111111111111111111111111110111111111111111111101111111111101111111111111110111111111111111111111111111101111111111111111110111111111110111111111111111101111111111111111111111111111111111101111111111111111111111111111111111111110111111111110111111111111111111111111111111111011111111111111111111111111111011111111111111111111111111101111111111111111111011111111111011111111111111111111111111101111111111111111111111111111101111111111111111111111111111111101111111111111111111011111111111111111111111111111111111111111101111111111101111111111011111111110111111111110111111111111111101111111111111111111111111111101111111111111111111111111111111111011111111111111111111111111111111110111111111111111111111111110111111111111111111101111111111111111111111111111111110111111111110111111111111111111111111111110111111111111111111110111111111110111111111111111101111111111111111111011111111111111111110111111111111111111111111111111110111111111110111111111111111111111111111110111111111111111111111111111101111111111101111111111111111111111111111111111011111111111111111111110111111111111111111101111111111101111111111111111111111111111111111111011111111111111101111111111111111111111111101111111111111111111111111101111111111111111111111111111111111111111100']}
setRegs(registers)