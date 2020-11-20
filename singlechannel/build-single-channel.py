# build-single-channel.py, version 3.0

import golly as g 

gliders=["3o$o$bo!","b2o$2o$2bo!","b2o$bobo$bo!","2bo$b2o$bobo!"]
gliderlist=[g.parse(gl) for gl in gliders]
elbow=g.parse("2C$2C!")

def makerecipe(recipe):
  g.putcells(gliderlist[0])
  totaltime=0
  for i in recipe[1:]:
    totaltime+=i
    g.putcells(g.transform(gliderlist[totaltime%4],totaltime/4,totaltime/4))
    g.show(str(totaltime))

# sample combined recipe
recipe = [0, 109, 91, 94, 91, 90, 96, 90, 91, 92, 90, 217, 90, 103, 90,                                         # 7move-3 -- move block to other side of the channel
             109, 91, 93, 91, 156, 91, 91, 126, 90, 91, 91, 91, 147, 90, 122, 95, 91, 91, 90, 119, 91, 112, 90, # 7move3 0move-28 -- duplicate elbow & replace block
             109, 91, 94, 91, 91, 92, 90, 169, 91, 90, 116, 90, 113, 90]                                        # 7move-29 -- widen the space between the two elbows
# The final number in each recipe below represents the amount of time that must elapse
#     before another recipe can be safely appended.
# To string recipes together, remove all leading "0"s except for the first, and
#     remove the final number from the last recipe to avoid a pi explosion at the end
#     (or append the elbowdestroy recipe to delete the elbow block completely).

g.addlayer()
g.setrule("LifeHistory")
g.putcells(g.transform(elbow,-5,-2))
g.setstep(4)
g.fit()
g.setmag(1)
makerecipe(recipe)

"""
# Sample recipes from slmake repository:  https://gitlab.com/apgoucher/slmake/blob/master/data/simeks/pp.txt

recipe = [0, 109, 90, 93, 91, 90, 90, 90, 90]    # elbowdestroy

# elbow duplicators
recipe = [0, 109, 91, 93, 91, 127, 91, 90, 145, 91, 90, 90, 146, 90, 91, 91, 92, 90]    # 7move9 7move-7
recipe = [0, 109, 90, 93, 91, 91, 90, 90, 100, 90, 90, 146, 96, 90, 90, 90, 92, 156, 144, 90]    # 7move19 0move-12
recipe = [0, 109, 91, 94, 91, 91, 128, 126, 90, 152, 91, 176, 125, 90, 90, 90, 91, 90, 90, 108, 90, 99, 90]    # 0move-4 0move-30
recipe = [0, 109, 91, 94, 91, 91, 128, 126, 90, 152, 91, 176, 125, 90, 90, 90, 91, 90, 90, 108, 90, 109, 90]    # 0move-4 7move-33
recipe = [0, 109, 90, 93, 91, 90, 95, 90, 90, 91, 90, 91, 90, 147, 90, 151, 126, 90, 107, 90, 111, 90, 99, 90]    # 0move-18 7move-37
recipe = [0, 109, 91, 93, 91, 156, 91, 91, 126, 90, 91, 91, 91, 147, 90, 122, 95, 91, 91, 90, 119, 91, 112, 90]    # 7move3 0move-28
recipe = [0, 109, 91, 93, 90, 171, 90, 90, 90, 91, 144, 90, 90, 119, 90, 108, 90, 91, 91, 90, 103, 90, 116, 90]    # 0move6 7move-33
recipe = [0, 109, 91, 93, 90, 123, 90, 105, 90, 90, 111, 90, 112, 91, 90, 130, 90, 91, 131, 121, 90, 91, 98, 90]    # 7move1 7move-17
recipe = [0, 109, 91, 94, 91, 91, 179, 90, 91, 94, 91, 102, 90, 156, 107, 113, 91, 134, 180, 91, 148, 91, 91, 90]    # 7move17 0move-2
recipe = [0, 109, 91, 93, 91, 145, 215, 106, 90, 90, 91, 91, 174, 90, 144, 90, 90, 90, 91, 137, 90, 91, 128, 90]    # 7move15 0move-6

# elbow block moves
recipe = [0, 109, 90, 93, 91, 90, 95, 91, 91, 138, 157, 96, 90, 120, 91, 97, 107, 90, 90, 93, 188]    # 0move44
recipe = [0, 109, 91, 93, 91, 155, 106, 91, 90, 139, 91, 104, 91, 90, 93, 104, 91, 91, 143, 91, 110, 153, 162, 90, 91, 93, 163]    # 0move-32
recipe = [0, 109, 91, 94, 91, 91, 92, 90, 97, 91, 90, 91, 90, 161, 91, 91, 91, 91, 91, 103, 130]    # 0move22
recipe = [0, 109, 91, 93, 91, 92, 90, 128, 90, 91, 138, 99, 118, 91, 90, 91, 91, 169, 90, 91, 95, 91, 131, 90]    # 7move21
recipe = [0, 109, 91, 93, 91, 145, 215, 106, 90, 90, 91, 91, 174, 90, 158, 90, 90, 90, 91, 137, 90, 91, 127, 90]    # 0move20
recipe = [0, 109, 91, 94, 91, 91, 92, 90, 113, 90, 91, 101, 90, 91, 93, 90, 90, 90, 106, 90, 91, 91, 91, 90, 109, 90, 90, 90, 90]    # 7move19
recipe = [0, 109, 91, 93, 91, 113, 91, 132, 91, 91, 133, 91, 90, 98, 91, 90, 131, 90, 112, 132, 90, 90]    # 0move18
recipe = [0, 109, 90, 93, 91, 91, 90, 90, 100, 90, 90, 174, 90, 90, 90, 90, 105, 90, 130, 90, 90]    # 7move17
recipe = [0, 109, 91, 94, 91, 91, 96, 90, 97, 91, 91, 130, 94, 90, 105, 90, 95, 143, 99]    # 0move16
recipe = [0, 109, 91, 93, 91, 97, 91, 90, 90, 94, 91, 118, 90, 91, 99, 213, 102, 90, 90, 90, 90]    # 7move15
recipe = [0, 109, 91, 93, 90, 140, 150, 113, 90, 90, 90, 90, 91, 136, 119, 127, 90, 154, 142, 132, 91, 91, 90]    # 0move14
recipe = [0, 109, 91, 93, 91, 92, 90, 97, 91, 116, 91, 93, 115, 90, 91, 130, 90]    # 7move13
recipe = [0, 109, 91, 93, 91, 92, 90, 97, 91, 116, 91, 93, 115, 90, 91, 127, 90, 124, 112, 90]    # 0move12
recipe = [0, 109, 91, 93, 91, 117, 90, 91, 90, 163, 91, 163, 91, 90, 149, 109, 109, 162, 91, 162, 91, 90, 90]    # 7move11
recipe = [0, 109, 91, 93, 91, 129, 149, 91, 90, 90, 105, 90, 90, 90, 90, 114, 91, 100, 90, 90]    # 0move10
recipe = [0, 109, 90, 93, 91, 91, 90, 90, 95, 90, 91, 90, 90, 140, 90, 90, 128, 93]    # 7move9
recipe = [0, 109, 91, 94, 91, 91, 92, 90, 119, 90, 90]    # 0move8
recipe = [0, 109, 91, 94, 91, 90, 96, 90, 91, 146, 240, 109, 91, 94, 91, 91, 92, 90, 119, 90, 90]    # 7move7
recipe = [0, 109, 91, 93, 91, 145, 215, 104, 90, 90, 90, 90, 90, 102, 92, 90, 90, 90, 106, 155, 150, 90]    # 0move6
recipe = [0, 109, 91, 93, 91, 92, 90, 110, 90, 152, 90, 90, 91, 91, 91, 90, 90, 90, 90, 175, 119, 115, 193]    # 7move5
recipe = [0, 109, 91, 93, 91, 92, 90, 90, 90, 151, 93, 90, 143, 134, 94, 90, 90, 90, 109, 91, 90]    # 0move4
recipe = [0, 109, 91, 94, 91, 91, 92, 90, 143, 90, 90, 90, 129, 101, 102, 90]    # 7move3
recipe = [0, 109, 90, 93, 91, 91, 90, 90, 91, 91, 90, 90, 91, 90, 90, 94, 90, 90]    # 0move2
recipe = [0, 109, 91, 94, 91, 91, 92, 90, 143, 90, 91, 156, 90, 104, 164]    # 7move1
recipe = [0, 109, 91, 93, 91, 129, 148, 90, 93, 90, 93, 90, 161, 153, 155, 90, 107, 90, 90, 90]    # 0move0
recipe = [0, 109, 91, 94, 91, 90, 96, 90, 91, 146, 240]    # 7move-1
recipe = [0, 109, 91, 94, 91, 91, 136, 90, 90, 91, 171, 100, 118, 90, 90]    # 0move-2
recipe = [0, 109, 91, 94, 91, 90, 96, 90, 91, 92, 90, 217, 90, 103, 90]    # 7move-3
recipe = [0, 109, 90, 93, 91, 91, 90, 90, 92, 90, 95, 91, 170, 90, 90, 91, 91, 98, 91, 91, 90]    # 0move-4
recipe = [0, 109, 91, 94, 91, 91, 92, 90, 173, 100, 90, 141, 91, 90, 90, 90, 147, 90, 117, 192]    # 7move-5
recipe = [0, 109, 91, 93, 91, 156, 91, 91, 94, 90, 91, 140, 91, 103, 91, 91, 132, 90]    # 0move-6
recipe = [0, 109, 91, 93, 91, 118, 90, 91, 91, 91, 90, 90, 156, 114, 90, 90, 90, 90, 141, 90]    # 7move-7
recipe = [0, 109, 90, 93, 91, 90, 95, 91, 90, 91, 91, 90, 90, 91, 90, 90, 99, 90, 90, 91, 90, 94, 90, 90]    # 0move-8
recipe = [0, 109, 91, 94, 91, 91, 179, 90, 91, 94, 91, 102, 91, 105, 91, 108, 90, 91, 91, 120, 90, 90]    # 7move-9
recipe = [0, 109, 91, 94, 91, 91, 96, 90, 97, 91, 91, 130, 94, 90, 105, 90, 95, 111, 90]    # 0move-10
recipe = [0, 109, 91, 93, 91, 92, 90, 90, 90, 151, 93, 90, 137, 113, 112, 90, 121, 90]    # 7move-11
recipe = [0, 109, 91, 93, 91, 137, 91, 91, 125, 172, 108, 90, 109, 91, 101, 120, 90, 90]    # 0move-12
recipe = [0, 109, 91, 94, 91, 91, 114, 94, 90, 106, 90, 91, 107, 233, 118, 90, 90, 90]    # 7move-13
recipe = [0, 109, 91, 93, 91, 155, 106, 91, 91, 145, 90, 90, 91, 91, 90, 91, 90, 90, 118, 90]    # 0move-14
recipe = [0, 109, 91, 94, 91, 90, 152, 91, 90, 91, 145, 90, 90, 139, 91, 90, 92, 90]    # 7move-15
recipe = [0, 109, 90, 93, 91, 91, 128, 91, 91, 90, 100, 90, 90, 176, 94, 153, 90, 145, 115]    # 0move-16
recipe = [0, 109, 91, 93, 90, 97, 91, 91, 93, 91, 90, 90, 91, 123, 114, 92, 90, 90, 154, 90, 117, 126, 141, 90, 92, 106, 90]    # 7move-17
recipe = [0, 109, 91, 94, 91, 91, 136, 91, 90, 91, 120, 90, 144, 90, 90, 90, 90, 102, 90, 90]    # 0move-18
recipe = [0, 109, 91, 93, 90, 171, 90, 90, 91, 154, 110, 169, 107, 91, 90, 99, 91, 122, 90, 90, 159, 90, 90]    # 7move-19
recipe = [0, 109, 91, 94, 91, 91, 93, 90, 103, 120, 105, 101, 91, 106, 90, 90, 125, 90, 107, 91, 101, 90, 130, 91, 90, 90]    # 0move-20
recipe = [0, 109, 91, 93, 91, 132, 115, 102, 90, 91, 91, 91, 90, 90, 154, 98]    # 7move-21
recipe = [0, 109, 91, 93, 90, 118, 91, 90, 90, 91, 120, 132, 90, 101, 91, 125, 179, 91, 116, 108, 128, 90]    # 0move-22
recipe = [0, 109, 91, 94, 91, 91, 92, 90, 173, 100, 90, 141, 91, 90, 90, 90, 145, 98, 107, 90]    # 7move-23
recipe = [0, 109, 91, 93, 90, 129, 149, 91, 90, 90, 108, 91, 90, 113, 97, 167, 90, 91, 105, 94, 90]    # 0move-24
recipe = [0, 109, 91, 93, 91, 129, 148, 91, 93, 154, 91, 91, 91, 90, 90, 90, 90, 143, 91, 90, 90, 107, 90]    # 7move-25
recipe = [0, 109, 91, 93, 90, 156, 90, 90, 95, 138, 91, 90, 96, 122, 91, 90, 95, 91, 90, 90, 91, 110, 130, 90, 131, 128]    # 0move-26
recipe = [0, 109, 91, 93, 91, 145, 215, 97, 91, 91, 90, 91, 158, 95, 90, 112, 90, 91, 97, 90, 100, 91, 90, 91, 107, 90]    # 7move-27
recipe = [0, 109, 91, 93, 90, 118, 91, 90, 90, 90, 97, 91, 90, 90, 129, 90, 164, 91, 94, 91, 91, 90, 96, 91, 111, 172]    # 0move-28
recipe = [0, 109, 91, 94, 91, 91, 92, 90, 169, 91, 90, 116, 90, 113, 90]    # 7move-29
recipe = [0, 109, 91, 94, 91, 91, 92, 90, 119, 90, 90, 109, 90, 93, 91, 90, 100, 131, 101, 90, 113, 95]    # 0move-30
recipe = [0, 109, 91, 93, 90, 140, 150, 113, 90, 90, 90, 90, 91, 136, 119, 127, 90, 103, 91, 99, 116]    # 7move-31

# moves with narrow reaction envelopes -- elbow block on the narrow side of the envelope
recipe = [0, 109, 90, 95, 245, 90, 126, 211, 91, 90, 98, 90, 96, 104, 91, 105, 91, 90, 90, 148, 90, 90, 124, 97, 91, 90, 111, 114, 161, 90, 90]    # 0move18
recipe = [0, 109, 90, 95, 245, 90, 126, 211, 91, 90, 120, 90, 91, 91, 90, 91, 90, 118, 90, 90, 91, 90, 113, 91, 105, 90, 90, 90, 90, 90]    # 0move12
recipe = [0, 109, 90, 93, 91, 90, 95, 91, 91, 139, 90, 163, 90, 91, 148, 104, 98, 91, 91, 90, 90, 92, 91, 173, 93, 136, 90, 100, 90, 92, 90, 91, 90]    # 0move10
recipe = [0, 109, 90, 93, 91, 90, 95, 91, 91, 118, 90, 93, 91, 90, 91, 91, 90, 113, 91, 90, 91, 91, 149, 91, 90, 90, 96, 91, 142, 91, 134, 197]    # 0move8
recipe = [0, 93, 90, 90, 90, 90, 90, 90, 91, 105, 159, 92, 90, 115, 100, 231, 99, 91, 90, 90, 91, 130, 91, 90, 90, 90, 91, 97, 91, 116, 90, 99, 174]    # 0move6
recipe = [0, 109, 90, 93, 91, 90, 95, 90, 90, 91, 90, 90, 151, 91, 91, 90, 93, 90, 90, 90, 100, 91, 90, 90, 90, 91, 90, 90, 97, 90, 90]    # 0move0
recipe = [0, 109, 90, 95, 245, 90, 126, 211, 91, 90, 113, 90, 90, 90, 92, 91, 90, 98, 165, 91, 125, 90, 90, 110, 112, 90, 90, 100, 90]    # 0move-2
recipe = [0, 109, 90, 93, 91, 90, 100, 131, 103, 91, 90, 91, 91, 90, 90, 90, 111, 90, 90, 163, 91, 91, 110, 90, 91, 90]    # 0move-4
recipe = [0, 109, 90, 93, 91, 90, 95, 91, 90, 91, 91, 90, 90, 91, 90, 90, 99, 90, 90, 91, 90, 94, 90, 90]    # 0move-8
recipe = [0, 109, 90, 95, 245, 90, 126, 211, 91, 90, 98, 90, 96, 115, 90, 90, 90, 123, 91, 112, 91, 101, 91, 91, 90, 105, 91, 90, 109, 90]    # 0move-10
recipe = [0, 109, 90, 93, 91, 90, 95, 90, 90, 91, 90, 91, 90, 158, 90, 90, 104, 91, 91, 91, 90, 141, 91, 91, 176, 91, 113, 91, 90, 138, 90, 117, 90]    # 0move-12
recipe = [0, 109, 90, 95, 245, 90, 126, 208, 139, 125, 90, 100, 91, 170, 156, 96, 90, 95, 91, 126, 90]    # 0move-14
recipe = [0, 109, 90, 93, 91, 90, 95, 91, 91, 102, 90, 106, 146, 91, 195, 105, 91, 90, 94, 90, 90, 104, 90, 146, 90, 91, 97, 90, 91, 90]    # 0move-16
recipe = [0, 109, 90, 95, 245, 90, 133, 91, 90, 123, 90, 96, 90, 91, 90, 90, 100, 90, 91, 90, 148, 90, 90, 90, 90, 119, 174, 91, 96, 104, 159, 183]    # 0move-18
recipe = [0, 109, 90, 93, 91, 90, 95, 91, 90, 91, 91, 90, 90, 91, 90, 90, 120, 91, 91, 151, 135, 90, 90, 90]    # 0move-20
recipe = [0, 109, 90, 93, 91, 90, 95, 90, 90, 91, 90, 90, 104, 115, 96, 90, 109, 90, 90, 90, 97, 90, 90, 90, 90, 90, 91, 90, 90]    # 0move-22
recipe = [0, 109, 90, 95, 245, 90, 131, 135, 91, 132, 91, 91, 90, 91, 105, 91, 90, 91, 90, 113, 91, 90, 119, 90, 96, 90, 90, 91, 91, 90, 90]    # 0move-26
recipe = [0, 109, 90, 93, 91, 90, 95, 91, 91, 139, 90, 157, 90, 91, 93, 90, 109, 90, 123, 119, 135, 94, 90, 161, 91, 90, 90, 90, 91, 91, 90, 139, 90]    # 0move-34

# glider outputs
recipe = [0, 109, 91, 94, 91, 91, 92, 90, 143, 90, 91, 158, 90]    # 2xO 7move3
recipe = [0, 109, 91, 94, 91, 91, 124, 91, 105, 90, 106, 112, 108, 90]    # -18iE 0move-20
recipe = [0, 109, 91, 94, 91, 91, 136, 91, 90, 91, 139, 98, 90, 156, 133]    # 5iE 0move8
recipe = [0, 109, 91, 93, 91, 127, 91, 90, 113, 90, 90, 111, 90, 111, 91, 91, 91, 90]    # -15xE 0move-26
recipe = [0, 109, 91, 93, 90, 155, 106, 90, 90, 92, 91, 109, 90, 93, 91, 90, 100, 124, 90]    # -21xO 7move-37
recipe = [0, 109, 91, 94, 91, 91, 136, 91, 90, 91, 140, 94, 166, 90, 90, 91, 94, 101, 90]    # -22iE 0move8
recipe = [0, 109, 91, 94, 91, 91, 136, 91, 90, 91, 104, 90, 90, 90, 110, 90, 90, 98, 90]    # -7iO 7move-25
recipe = [0, 109, 91, 93, 91, 127, 91, 90, 145, 91, 90, 90, 172, 110, 92, 90, 107, 90, 90, 90]    # -36iO 7move9
recipe = [0, 109, 91, 94, 91, 91, 92, 90, 97, 91, 90, 91, 90, 149, 90, 98, 91, 90, 95, 90]    # 19iE 7move15
recipe = [0, 109, 91, 94, 91, 91, 92, 90, 97, 91, 90, 91, 90, 149, 90, 98, 91, 90, 97, 90]    # 19iE 7move27
recipe = [0, 109, 91, 93, 91, 156, 91, 91, 126, 90, 91, 91, 91, 147, 90, 113, 90, 102, 90, 91, 90]    # -22xO 7move-31
recipe = [0, 109, 91, 93, 91, 132, 115, 135, 95, 94, 91, 91, 164, 91, 90, 128, 211, 96, 90, 90, 90]    # 2xE 0move2
recipe = [0, 109, 90, 93, 91, 91, 142, 90, 109, 91, 92, 90, 92, 90, 118, 91, 91, 90, 90, 119, 90]    # 3iE 7move-27
recipe = [0, 109, 91, 93, 91, 97, 91, 91, 106, 91, 90, 90, 90, 90, 90, 91, 163, 90, 90, 104, 90]    # -3xE 7move-15
recipe = [0, 109, 90, 95, 245, 90, 126, 208, 128, 90, 96, 91, 90, 90, 91, 91, 91, 91, 100, 90, 90, 90]    # 8iE 0move-8
recipe = [0, 109, 91, 93, 91, 129, 149, 91, 90, 91, 90, 90, 90, 90, 121, 91, 90, 90, 91, 91, 108, 90]    # 2xO 0move-8
recipe = [0, 109, 91, 94, 91, 91, 136, 91, 90, 91, 139, 98, 90, 94, 90, 95, 90, 91, 118, 207, 93, 90]    # -1xO 7move-5
recipe = [0, 109, 91, 93, 91, 97, 90, 90, 122, 91, 132, 90, 98, 91, 91, 105, 91, 90, 116, 90, 112, 90]    # -27iE 0move-12
recipe = [0, 109, 91, 94, 91, 91, 95, 91, 90, 90, 90, 90, 146, 91, 177, 91, 90, 97, 90, 90, 95, 90]    # 2xO 0move8
recipe = [0, 109, 91, 94, 91, 91, 128, 126, 90, 152, 91, 176, 125, 90, 90, 90, 91, 90, 90, 108, 90, 95, 90]    # -22xE 0move-4
recipe = [0, 109, 90, 93, 91, 91, 92, 90, 90, 91, 90, 110, 90, 90, 91, 124, 133, 90, 91, 113, 90, 90, 90]    # -15iO 0move-4
recipe = [0, 109, 91, 94, 91, 91, 136, 91, 90, 91, 101, 90, 90, 90, 92, 90, 144, 90, 91, 90, 90, 126, 90]    # -11xO 0move8
recipe = [0, 109, 91, 94, 91, 90, 96, 90, 91, 146, 240, 109, 91, 94, 91, 91, 92, 90, 143, 90, 91, 158, 90]    # 1iO 0move2
recipe = [0, 109, 91, 94, 91, 91, 92, 90, 119, 90, 90, 109, 91, 94, 91, 91, 92, 90, 143, 90, 91, 158, 90]    # 10xE 7move11
recipe = [0, 109, 90, 93, 91, 91, 90, 90, 100, 90, 91, 91, 90, 115, 91, 91, 131, 91, 91, 117, 176, 91, 121, 90]    # -39xE 7move-33
recipe = [0, 109, 90, 93, 91, 91, 98, 90, 90, 93, 91, 90, 90, 90, 246, 90, 109, 91, 92, 90, 90, 90, 93, 90]    # 4iO 0move0
recipe = [0, 109, 91, 93, 90, 123, 90, 105, 90, 90, 111, 90, 112, 91, 90, 98, 90, 96, 104, 91, 91, 90, 107, 181]    # -14iE 0move-18
recipe = [0, 109, 91, 93, 90, 156, 91, 91, 94, 90, 91, 118, 91, 91, 100, 90, 91, 123, 91, 91, 90, 91, 101, 90]    # 2xE 7move-13
recipe = [0, 109, 91, 93, 91, 174, 90, 91, 90, 148, 90, 101, 163, 146, 90, 143, 91, 91, 90, 123, 90, 91, 132, 99]    # 6xO 7move3
recipe = [0, 109, 91, 93, 91, 174, 90, 91, 90, 148, 90, 101, 163, 121, 91, 144, 90, 129, 90, 115, 90, 120, 91, 101, 90]    # 11xE 7move-1
recipe = [0, 109, 91, 93, 90, 140, 150, 100, 119, 91, 90, 90, 91, 91, 90, 121, 91, 90, 91, 158, 90, 97, 91, 115, 90]    # -13xE 0move-30
recipe = [0, 109, 90, 93, 91, 91, 135, 91, 144, 90, 90, 123, 91, 90, 120, 90, 91, 91, 91, 163, 90, 95, 91, 134, 90]    # -8iE 7move-11
recipe = [0, 109, 90, 93, 91, 91, 135, 90, 144, 91, 91, 123, 91, 90, 120, 91, 90, 91, 91, 163, 90, 95, 90, 134, 90]    # 7move-11
recipe = [0, 109, 91, 93, 90, 123, 90, 99, 90, 98, 93, 91, 155, 172, 134, 90, 90, 91, 92, 91, 91, 168, 143, 145, 90]    # 1iO 0move-14
recipe = [0, 109, 91, 93, 90, 173, 90, 90, 90, 90, 90, 141, 90, 90, 96, 91, 132, 90, 100, 90, 91, 119, 90, 90, 90]    # 5xO 0move12
recipe = [0, 109, 91, 94, 91, 91, 136, 91, 90, 91, 168, 90, 90, 97, 91, 91, 91, 90, 116, 90, 90, 90, 90, 90, 90]    # -9xE 0move16
recipe = [0, 109, 91, 93, 91, 132, 115, 104, 90, 97, 90, 90, 90, 90, 110, 90, 111, 137, 91, 91, 162, 90, 90, 93, 163]    # 5iE 7move-19
recipe = [0, 109, 91, 94, 91, 91, 136, 90, 90, 90, 124, 90, 91, 106, 150, 149, 90, 90, 114, 90, 137, 160, 91, 92, 90]    # -3iO 0move-22
recipe = [0, 109, 90, 93, 91, 91, 90, 90, 95, 90, 91, 90, 90, 217, 103, 90, 110, 98, 91, 91, 90, 91, 90, 109, 91, 90]    # 5xO 0move0
recipe = [0, 109, 91, 93, 90, 121, 90, 91, 144, 91, 90, 90, 91, 101, 90, 90, 153, 91, 167, 165, 91, 128, 91, 90, 114, 141]    # -7xE 0move-6
recipe = [0, 109, 90, 93, 91, 91, 90, 90, 95, 91, 90, 91, 123, 90, 90, 90, 90, 117, 91, 90, 90, 91, 91, 91, 108, 90]    # 15xE 0move8
recipe = [0, 109, 91, 94, 91, 91, 179, 90, 91, 94, 91, 102, 91, 171, 91, 110, 91, 156, 90, 119, 90, 90, 90, 90, 91, 90]    # -11iO 0move8
recipe = [0, 109, 91, 94, 91, 91, 96, 90, 135, 90, 109, 91, 94, 91, 91, 105, 91, 90, 91, 98, 91, 90, 127, 172, 92, 90]    # 1xE 0move16
recipe = [0, 109, 91, 93, 90, 123, 91, 103, 90, 91, 157, 90, 133, 90, 118, 91, 118, 91, 90, 103, 90, 90, 97, 143, 90, 90]    # -8iO 0move8
recipe = [0, 109, 91, 93, 90, 129, 148, 91, 112, 140, 113, 91, 106, 91, 91, 121, 90, 103, 221, 146, 90, 128, 154, 90, 91, 90]    # -12xE 7move-21
recipe = [0, 109, 91, 94, 91, 91, 136, 91, 90, 91, 140, 94, 112, 91, 129, 90, 90, 92, 90, 100, 90, 115, 91, 91, 93, 90]    # -8xE 7move-1
recipe = [0, 109, 90, 93, 91, 90, 95, 91, 91, 109, 91, 90, 90, 91, 99, 90, 98, 90, 90, 118, 91, 90, 90, 90, 90, 90]    # 2iO 0move-14
recipe = [0, 93, 91, 90, 140, 94, 100, 186, 164, 90, 205, 94, 106, 109, 91, 99, 91, 90, 91, 127, 90, 90, 91, 90, 90, 91, 90]    # -2xE 7move-11
recipe = [0, 109, 91, 94, 91, 91, 90, 91, 91, 91, 166, 91, 91, 105, 91, 90, 90, 144, 90, 118, 91, 90, 91, 107, 165, 148, 90]    # 1iO 0move-22
recipe = [0, 109, 90, 93, 91, 91, 98, 90, 90, 100, 90, 90, 91, 91, 126, 90, 116, 90, 90, 156, 91, 101, 91, 104, 90, 114, 90]    # -6xO 0move-2
recipe = [0, 109, 91, 93, 91, 92, 90, 97, 91, 116, 91, 119, 90, 90, 91, 104, 99, 90, 92, 94, 91, 97, 91, 92, 91, 98, 90]    # 15iO 7move-9
recipe = [0, 124, 126, 91, 90, 90, 91, 90, 90, 94, 190, 104, 91, 90, 123, 100, 135, 103, 91, 159, 90, 127, 90, 90, 90, 163, 90]    # 1iO 0move4
recipe = [0, 109, 91, 93, 91, 127, 91, 90, 113, 90, 90, 115, 90, 149, 90, 98, 90, 91, 103, 90, 90, 135, 134, 90, 90, 93, 90]    # -4iO 0move-8
recipe = [0, 109, 90, 93, 91, 91, 90, 90, 100, 90, 90, 146, 96, 90, 90, 99, 165, 90, 90, 91, 91, 90, 91, 90, 90, 91, 90]    # -4xO 7move-13
recipe = [0, 109, 90, 93, 91, 91, 142, 91, 109, 90, 92, 90, 100, 90, 90, 163, 177, 90, 90, 90, 121, 91, 91, 96, 91, 143, 90]    # 0iE 0move-14
recipe = [0, 109, 91, 93, 90, 140, 150, 132, 212, 103, 90, 106, 91, 90, 90, 165, 110, 120, 90, 90, 92, 90, 90, 91, 90, 117, 90]    # 13xE 7move-11
recipe = [0, 109, 91, 93, 91, 174, 90, 91, 91, 90, 90, 91, 120, 91, 90, 157, 90, 101, 91, 91, 119, 90, 90, 90, 90, 90, 90]    # 20iO 0move4
recipe = [0, 124, 126, 91, 90, 90, 91, 90, 90, 164, 193, 91, 90, 90, 124, 95, 91, 156, 90, 90, 126, 90, 90, 109, 90, 117, 90]    # 18iE 0move-6
recipe = [0, 109, 91, 93, 91, 155, 106, 91, 90, 139, 91, 104, 91, 90, 93, 104, 91, 91, 143, 91, 110, 153, 162, 90, 90, 93, 163]    # -8xO 0move-32
recipe = [0, 93, 91, 109, 90, 106, 210, 134, 90, 94, 197, 90, 90, 148, 90, 91, 90, 91, 126, 91, 118, 90, 99, 90, 90, 90, 90]    # -6xE 0move-6
recipe = [0, 109, 91, 94, 91, 91, 92, 90, 143, 90, 91, 156, 90, 104, 164, 109, 91, 94, 91, 91, 92, 90, 143, 90, 91, 158, 90]    # 3iO 0move4
recipe = [0, 109, 91, 93, 91, 92, 90, 97, 91, 116, 91, 106, 90, 90, 99, 91, 146, 96, 90, 90, 153, 91, 92, 90, 113, 95, 90]    # -2iO 0move-18
"""