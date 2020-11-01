# isorule.py
# A modification of partialrule.py which returns the isotropic rulespace for a pattern in a format suitable for infoboxes on the wiki.
# This simply checks the number of generations you input to see if the pattern's evolution is the same, so it can be used for non-periodic patterns as well.
# Shamelessly stolen from Rhombic (Feb 2018) by Ian07 (Jan 2019).
# Now fixed for Python 3.x! (Oct 2020)

import golly as g
from glife import validint

Hensel = [
    ['0'],
    ['1c', '1e'],
    ['2a', '2c', '2e', '2i', '2k', '2n'],
    ['3a', '3c', '3e', '3i', '3j', '3k', '3n', '3q', '3r', '3y'],
    ['4a', '4c', '4e', '4i', '4j', '4k', '4n', '4q', '4r', '4t', '4w', '4y', '4z'],
    ['5a', '5c', '5e', '5i', '5j', '5k', '5n', '5q', '5r', '5y'],
    ['6a', '6c', '6e', '6i', '6k', '6n'],
    ['7c', '7e'],
    ['8']
]

# Python versions < 2.4 don't have "sorted" built-in
try:
    sorted
except NameError:
    def sorted(inlist):
        outlist = list(inlist)
        outlist.sort()
        return outlist

# --------------------------------------------------------------------

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

# --------------------------------------------------------------------

def rulestringopt(a):
    result = ''
    context = ''
    lastnum = ''
    lastcontext = ''
    for i in a:
        if i in 'BS':
            context = i
            result += i
        elif i in '012345678':
            if (i == lastnum) and (lastcontext == context):
                pass
            else:
                lastcontext = context
                lastnum = i
                result += i
        else:
            result += i
    result = str.replace(result, '4aceijknqrtwyz', '4')
    result = str.replace(result, '3aceijknqry', '3')
    result = str.replace(result, '5aceijknqry', '5')
    result = str.replace(result, '2aceikn', '2')
    result = str.replace(result, '6aceikn', '6')
    result = str.replace(result, '1ce', '1')
    result = str.replace(result, '7ce', '7')
    return result

clist = []
rule = g.getrule().split(':')[0]

fuzzer = rule + '9'
oldrule = rule
rule = ''
context = ''
deletefrom = []
for i in fuzzer:
    if i == '-':
        deletefrom = [x[1] for x in Hensel[int(context)]]
    elif i in '0123456789/S':
        if deletefrom:
            rule += ''.join(deletefrom)
            deletefrom = []
        context = i
    if len(deletefrom) == 0:
        rule += i
    elif i in deletefrom:
        deletefrom.remove(i)
rule = rule.strip('9')

if not (rule[0] == 'B' and '/S' in rule):
    g.exit('Please set Golly to a Life-like rule.')

if g.empty():
    g.exit('The pattern is empty.')

s = g.getstring('Enter the period:', '', 'Rules calculator')
if not validint(s):
    g.exit('Bad number: %s' % s)

numsteps = int(s)
if numsteps < 1:
    g.exit('Period must be at least 1.')

g.select(g.getrect())
g.copy()
s = int(s)

for i in range(0,s):
    g.run(1)
    clist.append(list(chunks(g.getcells(g.getrect()), 2)))
    mcc = min(clist[i])
    clist[i] = [[x[0] - mcc[0], x[1] - mcc[1]] for x in clist[i]]

g.show('Processing...')

ruleArr = rule.split('/')
ruleArr[0] = ruleArr[0].lstrip('B')
ruleArr[1] = ruleArr[1].lstrip('S')

b_need = []
b_OK = []
s_need = []
s_OK = []

context = ''
fuzzed = ruleArr[0] + '9'
for i in fuzzed:
    if i in '0123456789':
        if len(context) == 1:
            b_need += Hensel[int(context)]
            b_OK += Hensel[int(context)]
        context = i
    elif context != '':
        b_need.append(context[0] + i)
        b_OK.append(context[0] + i)
        context += context[0]
context = ''
fuzzed = ruleArr[1] + '9'
for i in fuzzed:
    if i in '0123456789':
        if len(context) == 1:
            s_need += Hensel[int(context)]
            s_OK += Hensel[int(context)]
        context = i
    elif context != '':
        s_need.append(context[0] + i)
        s_OK.append(context[0] + i)
        context += context[0]

for i in [iter2 for iter1 in Hensel for iter2 in iter1]:
    if not i in b_OK:
        b_OK.append(i)
        execfor = 1
        # B0 and nontotalistic rulestrings are mutually exclusive
        try:
            g.setrule(rulestringopt('B' + ''.join(b_OK) + '/S' + ruleArr[1]))
        except:
            b_OK.remove(i)
            execfor = 0
        for j in range(0, s * execfor):
            g.run(1)
            try:
                dlist = list(chunks(g.getcells(g.getrect()), 2))
                mcc = min(dlist)
                dlist = [[x[0] - mcc[0], x[1] - mcc[1]] for x in dlist]
                if not(clist[j] == dlist):
                    b_OK.remove(i)
                    break
            except:
                b_OK.remove(i)
                break
        g.new('')
        g.paste(0, 0, 'or')
        g.select(g.getrect())
        b_OK.sort()

    if not i in s_OK:
        s_OK.append(i)
        execfor = 1
        # B0 and nontotalistic rulestrings are mutually exclusive
        try:
            g.setrule(rulestringopt('B' + ruleArr[0] + '/S' + ''.join(s_OK)))
        except:
            s_OK.remove(i)
            execfor = 0
        for j in range(0, s * execfor):
            g.run(1)
            try:
                dlist = list(chunks(g.getcells(g.getrect()), 2))
                mcc = min(dlist)
                dlist = [[x[0] - mcc[0], x[1] - mcc[1]] for x in dlist]
                if not(clist[j] == dlist):
                    s_OK.remove(i)
                    break
            except:
                s_OK.remove(i)
                break
        g.new('')
        g.paste(0, 0, 'or')
        g.select(g.getrect())
        s_OK.sort()

    if i in b_need:
        b_need.remove(i)
        g.setrule(rulestringopt('B' + ''.join(b_need) + '/S' + ruleArr[1]))
        for j in range(0, s):
            g.run(1)
            try:
                dlist = list(chunks(g.getcells(g.getrect()), 2))
                mcc = min(dlist)
                dlist = [[x[0] - mcc[0], x[1] - mcc[1]] for x in dlist]
                if not(clist[j] == dlist):
                    b_need.append(i)
                    break
            except:
                b_need.append(i)
                break
        g.new('')
        g.paste(0, 0, 'or')
        g.select(g.getrect())
        b_need.sort()

    if i in s_need:
        s_need.remove(i)
        g.setrule(rulestringopt('B' + ruleArr[0] + '/S' + ''.join(s_need)))
        for j in range(0, s):
            g.run(1)
            try:
                dlist = list(chunks(g.getcells(g.getrect()), 2))
                mcc = min(dlist)
                dlist = [[x[0] - mcc[0], x[1] - mcc[1]] for x in dlist]
                if not(clist[j] == dlist):
                    s_need.append(i)
                    break
            except:
                s_need.append(i)
                break
        g.new('')
        g.paste(0, 0, 'or')
        g.select(g.getrect())
        s_need.sort()

g.setrule('B' + ''.join(sorted(b_need)) + '/S' + ''.join(sorted(s_need)))
rulemin = g.getrule()

g.setrule('B' + ''.join(sorted(b_OK)) + '/S' + ''.join(sorted(s_OK)))
rulemax = g.getrule()

ruleres = '|isorulemin       = ' + rulemin + '|isorulemax       = ' + rulemax
g.show(ruleres)
g.setclipstr(ruleres)
g.setrule(oldrule)
