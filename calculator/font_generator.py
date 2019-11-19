import golly as g 

font = g.parse("701bo$307bo26bo21b2o18bo26bo11b2o90bo192b3o226bo2bo11b3o74b2o9bobo5bo8bo$2b3o7b4o9b3o7b4o8b5o7b5o7b3o8bo3bo5b3o9b3o6bo3bo6bo11bo3bo6bo3bo6b3o8b4o9b3o7b4o9b3o8b5o6bo3bo7bo3bo6bo3bo7bo3bo7bo3bo6b5o17bo26bo20bo20bo10bo9bo5bo12bo90bo77b3o9bo8b2o9b3o10bo8b5o8b3o8b5o7b3o9b3o9bobobo25bo4bo67bo14bo7bo44b2o12bo14bo13bo15bo2bo10bo3bo14bo6bo28b2o7b2o11bo2bo8bobo5bo7bobo$bo3bo6bo3bo7bo3bo6bo3bo7bo11bo10bo3bo7bo3bo6bo11bo7bo2bo7bo11b2ob2o6b2o2bo5bo3bo7bo3bo7bo3bo6bo3bo7bo3bo9bo8bo3bo7bo3bo6bo3bo7bo3bo7bo3bo10bo17bo26bo20bo20bo26bo2bo9bo89b3o75bo3bo7b2o7bo2bo7bo3bo8b2o8bo11bo15bo6bo3bo7bo3bo8bobo11b5o10bobo2bo29bo22bobo12bo14bo9bo22bo8bo10bo2bo12bo13bo13bo14b6o9bo2b2o13bo8bo10bo7bo8bo9bo11bo2bo23bo3bo$bo3bo6bo3bo7bo10bo3bo7bo11bo10bo11bo3bo6bo11bo7bobo8bo11bobobo6bobobo5bo3bo7bo3bo7bo3bo6bo3bo7bo13bo8bo3bo7bo3bo6bo3bo8bobo8bo3bo9bo7b3o8b4o9b3o8b4o8b3o8b3o8b4o7b4o7bo9bo5bobo10bo8b4o7bob2o8b3o8b4o9b4o6bob2o9b4o8bo8bo3bo7bo3bo6bobobo7bo3bo7bo3bo6b5o5bo2b2o8bo10bo11bo7bobo8bo11bo15bo6bo3bo7bo3bo9b3o26bo2bo30bo23bo13bo14bo9bo45bo12bo13bo13bo15bo2bo10bobobo13bo8bo9bo9bo7bo9bo11bobo$b5o6b4o8bo10bo3bo7b4o8b4o7bob3o7b5o6bo11bo7b2o9bo11bo3bo6bo2b2o5bo3bo7b4o8bo3bo6b4o9b3o10bo8bo3bo8bobo7bo3bo9bo10bobo9bo11bo7bo3bo7bo3bo6bo3bo7bo3bo8bo8bo3bo7bo3bo6bo9bo5b2o11bo8bobobo6b2o2bo6bo3bo7bo3bo7bo3bo6b2o2bo7bo12bo8bo3bo7bo3bo6bobobo8bobo8bo3bo9bo6bobobo8bo9bo10b2o7bo2bo8b4o8b4o11bo8b3o9b4o10bobo27bo29b5o5b4o10b5o10bo15bo9bo44bo14bo12bo13bo15bo2bo10bobobo12bo10bo7bo11bo6bo9bo10bobo2bo$bo3bo6bo3bo7bo10bo3bo7bo11bo10bo3bo7bo3bo6bo7bo3bo7bobo8bo11bo3bo6bo3bo5bo3bo7bo11bo3bo6bo3bo11bo9bo8bo3bo8bobo7bobobo8bobo10bo9bo9b4o7bo3bo7bo10bo3bo7b5o8bo8bo3bo7bo3bo6bo9bo5b3o10bo8bobobo6bo3bo6bo3bo7bo3bo7bo3bo6bo12b3o9bo8bo3bo8bobo7bobobo9bo9bo3bo8bo7b2o2bo8bo8bo13bo6b5o11bo7bo3bo9bo8bo3bo11bo8bobobo9b5o12bo3bo28bo23bo11bo16bo9bo22bo8bo11bo16bo11bo13bo14b6o9bo2b2o13bo8bo9bo9bo7bo9bo10bo2b2o$bo3bo6bo3bo7bo3bo6bo3bo7bo11bo10bo3bo7bo3bo6bo7bo3bo7bo2bo7bo11bo3bo6bo3bo5bo3bo7bo11bo3bo6bo3bo7bo3bo9bo8bo3bo9bo8b2ob2o7bo3bo9bo8bo9bo3bo7bo3bo7bo10bo3bo7bo12bo8bo3bo7bo3bo6bo9bo5bo2bo9bo8bobobo6bo3bo6bo3bo7bo3bo7bo3bo6bo15bo8bo8bo2b2o8bobo7bobobo8bobo8bo3bo7bo8bo3bo8bo7bo10bo3bo9bo8bo3bo7bo3bo9bo8bo3bo7bo3bo9b3o26bo3bobo27bo22bobo10bo16bo9bo22bo37bo11bo29bo2bo10bo17bo8bo10bo7bo8bo9bo10bo3bo$bo3bo6b4o9b3o7b4o8b5o7bo11b3o8bo3bo5b3o7b3o8bo3bo6b5o7bo3bo6bo3bo6b3o8bo12b3o7bo3bo8b3o10bo9b3o10bo8bo3bo7bo3bo9bo8b5o6b4o7b4o9b4o7b4o8b4o8bo9b4o7bo3bo6bo9bo5bo3bo7b3o7bobobo6bo3bo7b3o8b4o9b4o6bo11b4o10b2o7b2obo9bo9bobo8bo3bo8b4o6b5o6b3o8b3o6b4o8b3o10bo9b3o9b3o10bo9b3o9b3o11bo26bo5bo12b4o47bo18bo7bo9bo5bo6bo21bo17bo10bo13bo15bo2bo11b4o14bo6bo28b2o7b2o11b3obo$184b2o182bo28bo61bo15bo91bo267bo$368bo26b2o62bo15bo91bo266bo$365b3o91bo15bo88b3o!")
textLet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789$=%_+-*/(),.;:?\\|!#@{}<>[]&\"\'"

g.new("")
g.setrule("LifeHistory")
g.putcells(font)	

rect = g.getrect()
cells = g.getcells(rect)

for i in range(2, len(cells), 3):
	if cells[i] == 1:
		cells[i] = 4

g.putcells(cells)

x0 = rect[0]
y0 = rect[1] - 1
l = rect[2] + 2
h = rect[3] + 2

def ReadLetters(x0, y0, l, h):
	res = []
	xs = x0
	d = 0 
	zerocnt = 0 
	
	for x in range(x0, x0 + l):
	
		if len(g.getcells([x, y0, 1, h])) == 0:
			zerocnt += 1
			
		if zerocnt == 2:
			
			if d > 1:
				res.append((xs, y0, d + 1, h))
				
			xs = x
			d = 0 
			zerocnt = 0 
		else: 
			d += 1
		
	return res

letters = ReadLetters(x0, y0, l, h)
allcells = []

for let in letters:
	x0, y0, l, h = let
	cells = g.getcells([x0, y0, l, h])
	allcells.append(cells)

idx = 0 
for let in letters:
	x0, y0, l, h = let
	g.new("")
	g.putcells(allcells[idx], -x0)
	allcells[idx] = g.getcells([0, y0, l, h])
	idx += 1	
	

def Write(dic, L, dx = 0, dy = 0):
	d = 0
	for i in range(len(L)):
		let, dl = dic[L[i]]
		g.putcells(let, dx + d, dy)
		d += dl
		
dic = {}
for i in range(len(textLet)):
	dic[textLet[i]] = (allcells[i], letters[i][2])

dic[' '] = ([], 5)

g.new("")
Write(dic, "Hello World!")

g.setclipstr(str(dic))
