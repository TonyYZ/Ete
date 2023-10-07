import pyqtree
import ItiParser
from turtle import Turtle, Screen
from svg_turtle import SvgTurtle
import math
import random

random.seed(819)
WIDTH = 10000
HEIGHT = 10000
TURTLE_SIZE = 20
MARGIN = 50
UNIT = 50
SCALE = 5
ROUND = 2
MAGNIFICATION = 20
CHANCES = 5
txt = '''
	Ưrah rơm, izucun. Cunizaṡ, ĩhemõṡũl.
	Itaé gớt, izupun. Punizág, ĩhemõṡũl.
	Ưtar ịtát, íábipaé ghom.
	Ĩrágót, itatư bah ésehomoż. Ưbẽhonós.
	Ưżuṡazailian. Uṡaz:
	- Upun atư bah, édhom éctaupuzużuċ (300010) ul. Éṡb ẻtớtaulupużuzuluċ (9000010) ul, atifẽ hơm ịfusus.
	Ipáde żơt, rarmoż, mơt mơc ịfẽ hơm.
	Ágizud, ĩmabon? Ibe mfiáhailiág? Ibzaé gơc ịpr.
	Hơm ịzásiláṡ, izátilaé dơṡ.
	Bớs échom óv, izaribád, ré cớs ịzaé sơċ, ifẽ hmód ịbẽ ṡớd. 
	Évhom ịzásiláṡ, izátilẻ bơṡ.
	Izulupużuzuluċ (9000010) ul ifaé vehomód, itrfaé vhom.
	Ágé gud ịlár, itrẽ ruput bah.
	Brũt ịbư żágót ưzab ịbaz:
	- Ĩram żớt, tde rớtũy ịbẽ rớtũf. Ĩbz olatditaé dơh óciṡ, ĩmz õtulupużuzuluċ (9000010) ul itatư bah?
'''

quadIndex = pyqtree.Index(bbox=[-WIDTH / 2, -HEIGHT / 2, WIDTH / 2, HEIGHT / 2])
screen = Screen()
width, height = screen.screensize()
screen.screensize(width * MAGNIFICATION, height * MAGNIFICATION)
canvas = screen.getcanvas()
canvas.config(xscrollincrement=str(MAGNIFICATION))
canvas.config(yscrollincrement=str(MAGNIFICATION))

originX = -TURTLE_SIZE / 2 + screen.window_width() / 2 + MARGIN
originY = -screen.window_height() / 2 + TURTLE_SIZE / 2 - 5 * MARGIN
centerMode = True
mazeMode = True
exportMode = True
periodMode = False
rapidMode = False

if centerMode:
    originX = 0
    originY = 0
else:
    originX = -TURTLE_SIZE / 2 + screen.window_width() / 2 - MARGIN
    originY = -screen.window_height() / 2 + TURTLE_SIZE / 2 + MARGIN

if exportMode:
    t = SvgTurtle(WIDTH, HEIGHT)
    if mazeMode:
        trace = SvgTurtle(WIDTH, HEIGHT)
else:
    t = Turtle(shape="classic", visible=False)
    if mazeMode:
        trace = Turtle(shape="classic", visible=False)

angle = 180
traceAngle = 180
dir = 0  # 0 = horizontal, 1 = vertical, 2 = keep the same
dirPre = 0
curDivDir = 0  # current normal direction for keeping track of divergent paths in maze mode
boxLst = []
history = []
undoStepAcc = 0

global firstEndXor
global firstEndYor
global firstEndDir
global firstStartXor
global firstStartYor
global curAlter
global lastIsFuseau
global compInd
global daughter


def exDir(c):
    if c in 'ṡsbdnvrgh':  # passive
        return 0
    elif c in 'żzptmflcċ':  # active
        return 1
    else:
        return 2


def angle2dir(angle):
    angle %= 360
    if 45 < angle < 135 or 225 < angle < 315:
        return 1
    else:
        return 0


def calcDist(c, accent, layer):
    if accent == 0:
        return 0
    if layer in 'iu' or c in 'ṡższvf':
        dist = 2.5
    elif c in 'ywċh':
        dist = 1
    elif c in 'mn':
        dist = 2
    else:
        dist = 1.5
    return dist * UNIT / SCALE


def calcPos(c, accent):  # returns the distance for stepping back
    if accent == 1:
        if c in 'żṡpbmnlrċhyw':
            return UNIT / 2
        elif c in 'zstd':
            return UNIT - UNIT / SCALE
        elif c in 'fvcg':
            return UNIT / SCALE
    elif accent == 2:
        if c in 'żṡpbmnlrċhyw':
            return UNIT * 2 / 3
        elif c in 'zstd':
            return UNIT
        elif c in 'fvcg':
            return UNIT / 3
    else:
        return 0


def drawElem(c, normalDir=0, alter=1, layer='a', accent=0):  # normalDir: 0 = normal, 1 = mirrored, alter:
    # alternative directions
    if exDir(c) == 2:
        checkDir = dir
    else:
        checkDir = exDir(c)
    calibrate(checkDir, normalDir)
    if c in 'ṡż':
        '''
        t.forward(UNIT * (1 - 2 / SCALE) / 2)
        t.right(90)
        t.circle(UNIT / SCALE)
        t.left(90)
        t.penup()
        t.forward(UNIT * 2 / SCALE)
        t.pendown()
        t.forward(UNIT * (1 - 2 / SCALE) / 2)
        '''
        t.forward(UNIT / 2)
        if alter == 1:
            t.left(180)
        t.circle(UNIT / SCALE)
        if alter == 1:
            t.right(180)
        t.forward(UNIT / 2)
    if c in 'sz':
        t.penup()
        t.forward(UNIT / SCALE)
        t.pendown()
        if alter == 1:
            t.left(180)
        t.circle(UNIT / SCALE)
        if alter == 1:
            t.right(180)
        t.forward(UNIT * (1 - 1 / SCALE))
    if c in 'pb':
        t.forward(UNIT * (1 - 1 / SCALE) / 2)
        t.right(90 * alter)
        t.forward(UNIT / SCALE)
        t.left(180)
        t.penup()
        t.forward(UNIT / SCALE)
        t.right(90 * alter)
        t.forward(UNIT / SCALE)
        t.pendown()
        t.right(90 * alter)
        t.forward(UNIT / SCALE)
        t.left(180)
        t.penup()
        t.forward(UNIT / SCALE)
        t.right(90 * alter)
        t.pendown()
        t.forward(UNIT * (1 - 1 / SCALE) / 2)
    if c in 'td':
        t.penup()
        t.forward(UNIT / SCALE)
        t.pendown()
        t.right(90 * alter)
        t.forward(UNIT / SCALE)
        t.left(180)
        t.penup()
        t.forward(UNIT / SCALE)
        t.right(90 * alter)
        t.pendown()
        t.forward(UNIT * (1 - 1 / SCALE))
    if c in 'mn':
        t.forward(UNIT)
        t.penup()
        t.right(180)
        t.forward(UNIT * (1 - 1 / SCALE))
        t.left(90 * alter)
        t.forward(UNIT / SCALE)
        t.left(90 * alter)
        t.pendown()
        t.forward(UNIT * (1 - 2 / SCALE))
        t.left(90 * alter)
        t.penup()
        t.forward(UNIT / SCALE)
        t.right(90 * alter)
        t.forward(UNIT / SCALE)
        t.pendown()
    if c in 'fv':
        t.forward(UNIT * (1 - 1 / SCALE))
        if alter == 1:
            t.left(180)
        t.circle(UNIT / SCALE)
        if alter == 1:
            t.right(180)
        t.penup()
        t.forward(UNIT / SCALE)
        t.pendown()
    if c in 'lr':
        t.forward(UNIT)
        t.left(180)
        t.penup()
        t.forward(UNIT / 2)
        t.left(90 * alter)
        t.forward(UNIT / SCALE)
        t.pendown()
        t.left(180)
        t.forward(UNIT / SCALE)
        t.right(90 * alter)
        t.forward(UNIT / 2)
    if c in 'cg':
        t.forward(UNIT * (1 - 1 / SCALE))
        t.right(90 * alter)
        t.forward(UNIT / SCALE)
        t.left(180)
        t.penup()
        t.forward(UNIT / SCALE)
        t.right(90 * alter)
        t.penup()
        t.forward(UNIT / SCALE)
        t.pendown()
    if c in 'ċh':
        t.forward(UNIT * (0.5 + 0.5 / SCALE))
        t.right(90 * alter)
        t.penup()
        t.forward(UNIT / SCALE)
        t.right(90 * alter)
        t.forward(UNIT / SCALE)
        t.left(180)
        t.pendown()
        t.forward(UNIT * (0.5 + 0.5 / SCALE))
    if c in 'yw':
        t.forward(UNIT)

    dist = calcDist(c, accent, layer)
    pos = calcPos(c, accent)
    if accent == 1:
        t.penup()
        t.forward(-pos)
        t.right(90 * alter)
        t.forward(dist)
        t.pendown()
        t.dot(UNIT / SCALE / 2)
        t.penup()
        t.right(180)
        t.forward(dist)
        t.right(90 * alter)
        t.forward(pos)
        t.pendown()

    if accent == 2:
        t.penup()
        t.forward(-pos)
        t.right(90 * alter)
        t.forward(dist)
        t.pendown()
        t.dot(UNIT / SCALE / 2)
        t.penup()
        t.left(90 * alter)
        t.forward(UNIT / 3)
        t.pendown()
        t.dot(UNIT / SCALE / 2)
        t.penup()
        t.left(90 * alter)
        t.forward(dist)
        t.right(90 * alter)
        t.forward(pos - UNIT / 3)
        t.pendown()

    if layer == 'i':
        t.penup()
        if alter != 1:
            t.forward(-UNIT)
        t.right(90 * alter)
        t.forward(UNIT / SCALE + UNIT / 2)
        t.right(180)
        t.pendown()
        t.circle(UNIT / 2, 180)
        t.penup()
        t.right(180)
        t.forward(UNIT / SCALE + UNIT / 2)
        t.right(90 * alter)
        if alter == 1:
            t.forward(UNIT)
        t.pendown()

    if layer == 'u':
        t.penup()
        if alter == 1:
            t.forward(-UNIT)
        t.right(90 * alter)
        t.forward(UNIT / SCALE)
        t.pendown()
        t.circle(UNIT / 2, 180)
        t.penup()
        t.forward(UNIT / SCALE)
        t.right(90 * alter)
        if alter != 1:
            t.forward(UNIT)
        t.pendown()


def undoRep(n):
    global t
    for i in range(n):
        t.undo()


def countSteps(c, alter=1, accent=0, layer='a'):
    steps = 1  # calibrate
    if c in 'ṡż':
        steps += 3 + int(alter == 1) * 2
    if c in 'sz':
        steps += 5 + int(alter == 1) * 2
    if c in 'pb':
        steps += 17
    if c in 'td':
        steps += 11
    if c in 'mn':
        steps += 15
    if c in 'fv':
        steps += 5 + int(alter == 1) * 2
    if c in 'lr':
        steps += 11
    if c in 'cg':
        steps += 10
    if c in 'ċh':
        steps += 9
    if c in 'yw':
        steps += 1
    if accent == 1:
        steps += 12
    if accent == 2:
        steps += 17
    if layer == 'i':
        steps += 12
    if layer == 'u':
        steps += 10
    return steps


def undoElem(c, alter=1, accent=0, layer='a'):
    global t
    steps = countSteps(c, alter, accent, layer)
    for i in range(steps):
        t.undo()


def hollowDot():
    radius = UNIT / SCALE / 2
    t.color("white")
    t.dot(radius * 2)
    t.penup()
    t.right(90)
    t.forward(radius)
    t.left(90)
    t.pendown()
    t.color("black")
    t.circle(radius)
    t.penup()
    t.left(90)
    t.forward(radius)
    t.right(90)
    t.pendown()


def drawRect(x1, y1, x2, y2, color='red'):
    trace.penup()
    trace.setpos(x1, y1)
    calibrate(0, normalDir=1)
    trace.pendown()
    trace.fillcolor(color)
    trace.begin_fill()
    trace.forward(x2 - x1)
    trace.left(90)
    trace.forward(y2 - y1)
    trace.left(90)
    trace.forward(x2 - x1)
    trace.left(90)
    trace.forward(y2 - y1)
    trace.end_fill()
    trace.left(90)


def checkCollision(x1, y1, x2, y2):
    # for (c, x1o, y1o, x2o, y2o) in boxLst:
    #    if x1 < x2o and y1 < y2o and x1o < x2 and y1o < y2:
    #        print("naive collision", c, x1o, y1o, x2o, y2o)
    return quadIndex.intersect(bbox=[x1 + 1, y1 + 1, x2 - 1, y2 - 1])


def calcBox(elem, alter, mirror, preXor, preYor, mirror2=1, side=1):
    global t
    global dir
    if exDir(elem[0]) == 0 or exDir(elem[0]) == 2 and dir == 0:
        checkDir = 1
        postXor = t.xcor()
        postYor = t.ycor() + measure(elem, checkDir) * side * alter * mirror * mirror2 * int(elem[0] not in 'ċh')
    if exDir(elem[0]) == 1 or exDir(elem[0]) == 2 and dir == 1:
        checkDir = 0
        postXor = t.xcor() + measure(elem, checkDir) * side * alter * mirror * mirror2 * int(elem[0] not in 'ċh')
        postYor = t.ycor()
    print("calc box", elem[0], t.ycor(), measure(elem, checkDir) ,side, alter, mirror, mirror2)

    boxes = calcPreciseBox(elem[0], preXor, preYor, postXor, postYor)
    sortedBoxes = []

    for box in boxes:
        x1 = round(min(box[0], box[2]), ROUND)
        x2 = round(max(box[0], box[2]), ROUND)
        y1 = round(min(box[1], box[3]), ROUND)
        y2 = round(max(box[1], box[3]), ROUND)
        sortedBoxes.append((x1, y1, x2, y2))

    return sortedBoxes, postXor, postYor


def calcPreciseBox(c, x1, y1, x2, y2):
    global dir
    offSetX = 0
    offSetY = 0
    if exDir(c) == 0 or exDir(c) == 2 and dir == 0:
        ind = 0
        forward = 2 * int((x2 - x1) >= 0) - 1  # positive -> 1, negative -> -1
        if c in 'td':
            offSetX2 = UNIT / SCALE * forward
            offSetY2 = 0
        elif c in 'cg':
            offSetX2 = UNIT / SCALE * forward
            offSetY2 = y2 - y1
        elif c in 'ċh':
            offSetX = (UNIT / 2 + UNIT / SCALE / 2) * forward  # minimal thickness
        else:
            offSetX = x2 - x1
        offSetY = 2 * (2 * int((y2 - y1) >= 0) - 1)
    if exDir(c) == 1 or exDir(c) == 2 and dir == 1:
        ind = 1
        forward = 2 * int((y2 - y1) >= 0) - 1
        offSetX = 2 * (2 * int((x2 - x1) >= 0) - 1)
        if c in 'td':
            offSetY2 = UNIT / SCALE * forward
            offSetX2 = 0
        elif c in 'cg':
            offSetY2 = UNIT / SCALE * forward
            offSetX2 = x2 - x1
        elif c in 'ċh':
            offSetY = (UNIT / 2 + UNIT / SCALE / 2) * forward
        else:
            offSetY = y2 - y1

    if c in 'td':
        boxes = [(x1 + offSetX2, y1 + offSetY2, x2 + offSetX, y2 + offSetY)]
    elif c in 'cg':
        boxes = [(x1, y1, x2 - offSetX2 + offSetX, y2 - offSetY2 + offSetY)]
    elif c in 'ċh':
        boxes = [(x1, y1, x1 + offSetX, y1 + offSetY), (x2 - offSetX, y2 - offSetY, x2, y2)]
    else:
        boxes = [(x1, y1, x1 + offSetX, y1 + offSetY)]

    print("precise", c, x1, y1, x2, y2)
    rect1 = [x1, y1]
    rect2 = [x2, y2]
    if c in 'ṡż':
        rect1[ind] += (UNIT / 2 - UNIT / SCALE) * forward
        rect2[ind] += (-UNIT / 2 + UNIT / SCALE) * forward
    if c in 'sz':
        rect2[ind] += (-UNIT + 2 * UNIT / SCALE) * forward
    if c in 'pb':
        rect1[ind] += UNIT * (1 - 1 / SCALE) / 2 * forward
        rect2[ind] += -UNIT * (1 - 1 / SCALE) / 2 * forward
    if c in 'td':
        rect1[ind] += UNIT / SCALE * forward
        rect2[ind] += (UNIT / SCALE - UNIT + 2) * forward
    if c in 'mn':
        rect1[ind] += UNIT / SCALE * forward
        rect2[ind] -= UNIT / SCALE * forward
    if c in 'fv':
        rect1[ind] += (UNIT - 2 * UNIT / SCALE) * forward
    if c in 'lr':
        rect1[ind] += UNIT / 2 * forward
        rect2[ind] += (2 - UNIT / 2) * forward
    if c in 'cg':
        rect1[ind] += (UNIT - UNIT / SCALE - 2) * forward
        rect2[ind] -= UNIT / SCALE * forward
    if c in 'ċh':
        rect1[ind] += (UNIT / 2 - UNIT / SCALE / 2) * forward
        rect2[ind] += (UNIT / SCALE / 2 - UNIT / 2) * forward
    if c not in 'yw':  # yw only occupies the line
        boxes.append((rect1[0], rect1[1], rect2[0], rect2[1]))

    return boxes


def measure(elem, checkDir, measureExtra=True):
    c = elem[0]
    accent = elem[1]
    layer = elem[2]
    extra = 0
    if (c in 'ṡsbdnvrgh' and checkDir == 0) or (c in 'żzptmflcċ' and checkDir == 1) \
            or (c in 'yw' and checkDir == dir):  # same
        base = UNIT
    elif (c in 'ṡsbdnvrgh' and checkDir == 1) or (c in 'żzptmflcċ' and checkDir == 0) \
            or (c in 'yw' and checkDir != dir):  # different
        if c in 'ṡsvżzf':
            base = UNIT * 2 / SCALE
        else:
            base = UNIT / SCALE
        if measureExtra:
            extra = max(calcDist(c, accent, layer), int(layer in 'iu') * (UNIT / 2 + UNIT / SCALE))
        if extra != 0:
            # print("extra: " + str(extra))
            return extra  # extra length measured
    return base


def measureMiddle(c):
    if c in 'zsfvtdcgyw':
        return 0
    elif c in 'ṡż':
        return UNIT / SCALE * 2
    else:
        return UNIT / SCALE


def calibrate(checkDir, normalDir=0):
    global angle
    global t
    angleLst = [180, 0, 90, 270]
    if checkDir == 0:
        t.setheading(angleLst[normalDir])
        angle = angleLst[normalDir]
    elif checkDir == 1:
        t.setheading(angleLst[2 + normalDir])
        angle = angleLst[2 + normalDir]
    # print("adjusted to angle " + str(angle))


def drawFuseau(comp, spaces, divDir):
    global angle
    global firstEndXor
    global firstEndYor
    global firstEndDir
    global curDivDir
    global firstStartXor
    global firstStartYor
    global dirPre
    global boxLst
    stepAcc = 0
    maxSpace = max(spaces)
    maxIndex = spaces.index(maxSpace)
    print("angle first", angle)
    calibrate(dir, normalDir=divDir)
    stepAcc += 1
    print("angle", angle)
    print("data " + str(dir) + " " + str(dirPre) + " " + str(firstEndDir) + " " + str(
        exDir(comp[maxIndex][0][0])))
    if exDir(comp[maxIndex][0][0]) != dir and dirPre != dir:
        t.forward(UNIT)
        stepAcc += 1
    elif lastIsFuseau and firstEndDir != dirPre and exDir(comp[maxIndex][0][0]) != dirPre:
        calibrate(dirPre)
        t.forward(UNIT)
        stepAcc += 2
    firstStartXor = t.xcor()
    print("firstStartXor", t.xcor(), "firstStartYor", t.ycor())
    firstStartYor = t.ycor()  # original x before drawing
    first = True  # first branch
    side = 1  # -1 = left, 1 = right
    lastStep = [0, 0]  # left, right
    distSum = 0
    tmpBoxLst = []
    boxNum = 0
    for j in range(len(comp)):
        alter = 1
        chosenSpace = max(spaces)
        chosenIndex = spaces.index(chosenSpace)
        print(comp[chosenIndex])
        if not first:
            firstElem = comp[chosenIndex][0]
            t.right(90 * side)
            angle -= 90 * side
            t.penup()
            t.forward(lastStep[int(side == 1)])
            stepAcc += 3
            print("side: " + str(side) + " s:" + str(lastStep[int(side == 1)]) + " lastStep: " + str(
                lastStep))
            if exDir(firstElem[0]) == dir or exDir(firstElem[0]) == 2:
                t.forward(UNIT / SCALE)
                stepAcc += 1
                print("sideways step " + str(UNIT / SCALE * 1.5) + " angle: " + str(angle))
                lastStep[int(side == 1)] += UNIT / SCALE * 1.5
            t.left(90 * side)
            stepAcc += 1
            angle += 90 * side
            hasSame = False
            for elem in comp[chosenIndex]:
                if exDir(elem[0]) == dir or exDir(elem[0]) == 2:
                    hasSame = True
            if hasSame:
                print("overall aligned to middle")
                t.forward((maxSpace - chosenSpace) / 2)
            else:
                print("point aligned to middle")
                t.forward(maxSpace / 2)
            stepAcc += 1
            if exDir(firstElem[0]) != dir and exDir(firstElem[0]) != 2 and hasSame:
                t.forward(measure(firstElem, dir))  # adjust the starting point
                stepAcc += 1
                print("adjusted the chosen component")
            maxFirst = comp[maxIndex][0]  # the stem component's first element
            if exDir(maxFirst[0]) != dir and exDir(maxFirst[0]) != 2:
                t.forward(-measure(maxFirst, dir))  # adjust the starting point
                stepAcc += 1
                print("aligned to the stem component")
            print('(' + str(maxSpace) + '-' + str(chosenSpace) + ')/2=' + str((maxSpace - chosenSpace) / 2))

            t.pendown()
            stepAcc += 1
        offMax = 0  # the widest offset until we meet an element with the incorrect direction
        lastSame = -1  # the start index of the last sequence of elements with the correct direction
        sameCombo = False  # there is a sequence with the correct direction
        # (see if it is still true at the end)
        firstDif = -1  # the index of the first element with the incorrect direction
        hasDif = False
        offMaxBack = 0  # serves for the stem's back
        for k, elem in enumerate(comp[chosenIndex]):
            if not hasDif and (exDir(elem[0]) != dir and exDir(elem[0]) != 2):
                firstDif = k
                hasDif = True
            if exDir(elem[0]) == dir or exDir(elem[0]) == 2:
                if not sameCombo:
                    lastSame = k
                    sameCombo = True
            else:
                sameCombo = False

        print(
            "lastSame: " + str(lastSame) + " sameCombo: " + str(sameCombo) + " firstDif: " + str(firstDif))

        for k, elem in enumerate(comp[chosenIndex]):
            preXor = t.xcor()
            preYor = t.ycor()
            mirror2 = [1, -1][divDir]  # mirror for divergent paths in maze mode
            if (exDir(elem[0]) == 1 and dir == 0 and side == -1) or \
                    (exDir(elem[0]) == 0 and dir == 1 and side == 1):
                mirror = -1
                if mirror * mirror2 == -1:  # mirror (i.e. -1) * mirror2
                    normalDir = 1
                else:
                    normalDir = 0
                drawElem(elem[0], normalDir, alter=side * alter, accent=elem[1], layer=elem[2])
            else:
                mirror = 1
                if mirror * mirror2 == -1:
                    normalDir = 1  # mirror (i.e. 1) * mirror2
                else:
                    normalDir = 0
                drawElem(elem[0], normalDir, alter=side * alter, accent=elem[1], layer=elem[2])
            stepAcc += countSteps(elem[0], alter=side * alter, accent=elem[1], layer=elem[2])

            if mazeMode:
                bx = calcBox(elem, alter, mirror, preXor, preYor, side=side, mirror2=mirror2)
                postXor = bx[1]
                postYor = bx[2]
                for box in bx[0]:
                    x1 = box[0]
                    y1 = box[1]
                    x2 = box[2]
                    y2 = box[3]

                    collided = checkCollision(x1, y1, x2, y2)
                    print("quad collision", collided)
                    if not collided:
                        tmpBoxLst.append((elem[0], x1, y1, x2, y2))
                        boxNum += 1
                    else:
                        # drawRect(x1 + 1, y1 + 1, x2 - 1, y2 - 1, color='green')
                        print(x1 + 1, y1 + 1, x2 - 1, y2 - 1, alter, mirror)
                        print("---------\n", collided)
                        # for (c, x1o, y1o, x2o, y2o) in boxLst:
                          # print(c, x1o, y1o, x2o, y2o)
                          # drawRect(x1o, y1o, x2o, y2o, color='red')
                        print("collided")
                        return -1
                distSum += math.sqrt((postXor - originX) ** 2 + (postYor - originY) ** 2)

            if exDir(elem[0]) == dir or exDir(elem[0]) == 2:
                newOffMax = measure(elem, 1 - dir) \
                    # + int(elem[0] in 'ċh') * UNIT / SCALE
                if newOffMax > offMax and \
                        (alter != -1 and (alter != 1 or sameCombo and k >= lastSame)):
                    offMax = newOffMax
                    print("update " + elem[0] + " " + str(k) + " " + str(offMax))

                newOffMaxBack = measure(elem, 1 - dir) \
                    # + int(elem[0] in 'ċh') * UNIT / SCALE
                if first and newOffMaxBack > offMaxBack and alter == -1 and \
                        (k < firstDif or firstDif == -1):
                    offMaxBack = newOffMaxBack
            else:
                if offMax > 0:
                    print("added offMax " + str(offMax))
                lastStep[int(side == 1)] += offMax
                offMax = 0
                print("added " + elem[0] + " " + str(measure(elem, 1 - dir)))
                lastStep[int(side == 1)] += measure(elem, 1 - dir)
            alter *= -1
        if offMax > 0:
            print("added offMax " + str(offMax))
        lastStep[int(side == 1)] += offMax
        if first:
            print("offMaxBack " + str(offMaxBack))
            lastStep[1 - int(side == 1)] = offMaxBack
            firstEndXor = t.xcor()
            firstEndYor = t.ycor()
            firstEndDir = exDir(comp[chosenIndex][-1][0])
            print("first end dir: " + str(firstEndDir) + " dir: " + str(dir))
            first = False
        side = -side
        t.penup()
        t.setpos(firstStartXor, firstStartYor)
        t.pendown()
        stepAcc += 3
        print("angle last", angle)
        calibrate(dir, normalDir=divDir)
        stepAcc += 1
        print("angle", angle)
        spaces[chosenIndex] = 0

    return distSum, tmpBoxLst, boxNum, stepAcc


def retrace():
    global compInd
    global dir
    global curDivDir
    global curAlter
    global lastIsFuseau
    global daughter
    global periodMode
    global firstEndDir
    global dirPre
    global undoStepAcc
    undoRep(t.undobufferentries() - undoStepAcc)
    if daughter[0] == [-1, -1, 0, -1, False, 1, 'a', 1, 0, 2, 'd']:
        print(t.undobufferentries())
        steps = [31]
        print("sum:", sum(steps))
        t.save_as("./examples2/example init2.svg")
        for k, step in enumerate(steps):
            undoRep(step)
            daughter = daughter[3]  # retrace to the mother layer
            t.save_as("./examples2/example" + str(k) + "2.svg")
            print(k, t.undobufferentries())
        # t.save_as("./examples2/example final.svg")
        visited = True
        # drawElem(daughter[0][0], normalDir=daughter[0][2], alter=daughter[0][3], layer=daughter[0][6], accent=daughter[0][5])
        drawElem('l', normalDir=daughter[0][2], alter=daughter[0][3], layer='a', accent=0)
        # drawFuseau([[['c', 1, 'a']], [['h', 0, 'a']], [['m', 0, 'a']]], [50, 20.0, 50], 1)
        t.save_as("./examples2/example final2.svg")
        exit()

    k = compInd
    retraceDir = -1
    retraceTried = [True, True]
    print("entries", t.undobufferentries())
    print(daughter[0])
    while retraceDir == -1 or retraceTried == [True, True]:  # non-divergent or exhausted
        if k <= 0:
            print("There is no solution!")
            print(daughter)
            exit()
        # go back until encounters a non -1 explorable component
        daughter = daughter[3]  # retrace to the mother layer
        print("retrace back to", daughter[0][10], "stepAcc", daughter[0][0])
        retraceDir = daughter[0][1]
        retraceTried = [daughter[1][0], daughter[2][0]]
        undoRep(daughter[0][0])
        if daughter[0][10] == -1:  # the component is a fuseau
            for i in range(daughter[0][9]):
                quadIndex.remove(boxLst[-1], bbox=[boxLst[-1][1], boxLst[-1][2], boxLst[-1][3], boxLst[-1][4]])
                del boxLst[-1]
        else:
            quadIndex.remove(boxLst[-1], bbox=[boxLst[-1][1], boxLst[-1][2], boxLst[-1][3], boxLst[-1][4]])
            del boxLst[-1]
        k -= 1

    if periodMode:
        print("undo", compInd - k, "periods")
        undoRep(14 * (compInd - k))

    undoStepAcc = t.undobufferentries()
    compInd = k
    calibrate(daughter[0][1], normalDir=daughter[0][2])
    dir = daughter[0][1]
    curDivDir = daughter[0][2]
    curAlter = daughter[0][3]
    lastIsFuseau = daughter[0][4]
    firstEndDir = daughter[0][7]
    dirPre = daughter[0][8]
    # [[stepAcc, dir, curDivDir, alter, lastIsFuseau, accent, layer, firstEndDir, dirPre, boxNum, c],
    if rapidMode:
        screen.update()


def explore(comp, lst, spaces=-1, isFuseau=False):  # explore a lower level
    global curDivDir
    global curAlter
    global daughter
    global boxLst
    global undoStepAcc
    if isFuseau:
        tmpBoxLst = lst
        drawFuseau(comp, spaces, curDivDir)
        print("tmpBoxLst", tmpBoxLst)
        for box in tmpBoxLst:
            quadIndex.insert(box, bbox=[box[1], box[2], box[3], box[4]])
        boxLst += tmpBoxLst
    else:
        for box in lst:
            x1 = box[0]
            y1 = box[1]
            x2 = box[2]
            y2 = box[3]
            quadIndex.insert((comp[0], x1, y1, x2, y2), bbox=[x1, y1, x2, y2])
            boxLst.append((comp[0], x1, y1, x2, y2))
        drawElem(comp[0], normalDir=curDivDir, alter=curAlter, accent=comp[1], layer=comp[2])

    print("compare", t.undobufferentries(), undoStepAcc, t.undobufferentries() - undoStepAcc)
    daughter[0][0] = t.undobufferentries() - undoStepAcc
    undoStepAcc = t.undobufferentries()
    mother = daughter  # record the mother for retracing
    daughter[curDivDir + 1][0] = True  # mark as explored
    daughter = daughter[curDivDir + 1][1]  # become the structure nested inside (enter the deeper level)
    if not daughter:
        daughter += [-1, [False, []], [False, []], mother]  # create the deeper structure of history


def draw(lst):
    global angle
    global traceAngle
    global dir
    global curDivDir
    global t
    global firstEndXor
    global firstEndYor
    global firstEndDir
    global firstStartXor
    global firstStartYor
    global dirPre
    global curAlter
    global lastIsFuseau
    global history
    global daughter
    global boxLst
    global compInd
    global undoStepAcc
    if periodMode:  # initialize them only at the beginning if in period mode
        curAlter = 1
        lastIsFuseau = False
        firstEndDir = dir
    i = 0
    tmpLst = []
    if mazeMode:
        for sent in lst:
            tmpLst += sent
        lst = [tmpLst]
        history = [[-1, -1, -1, 1, False, -1, -1, -1, -1, -1, -1], [False, []], [False, []], []]
        # [[stepAcc, dir, curDivDir, alter, lastIsFuseau, accent, layer, firstEndDir, dirPre, boxNum, c],
        #  [tried?, daughter], [tried?, daughter], mother] (a quasi-binary tree)
        daughter = history  # current layer of daughter in the history
    while i < len(lst):
        sent = lst[i]
        row = i // 5
        compInd = 0
        if not periodMode:
            curAlter = 1
            lastIsFuseau = False
            firstEndDir = dir
        while compInd < len(sent):
            comp = sent[compInd]
            print("firstEndDir", firstEndDir)

            if isinstance(comp[0], list):  # identified as fuseau
                hasSame = 0
                spaces = [0] * len(comp)  # the space that would be occupied by each branch (its length)
                for branch in comp:
                    if exDir(branch[0][0]) == dir or exDir(branch[0][0]) == 2:
                        hasSame += 1  # continue in the same direction and measure based on this
                if hasSame < len(comp) / 2:
                    dir = 1 - dir  # swap back

                for j, branch in enumerate(comp):
                    offMax = 0  # the widest offset until we meet an element with the correct direction
                    alter = 1  # the alter in fuseaux is independent from simple elements
                    lastDif = -1  # the start index of the last sequence of elements with the incorrect direction
                    difCombo = False  # there is a sequence with the incorrect direction
                    # (see if it is still true at the end)
                    firstSame = -1  # the index of the first element with the incorrect direction (-1 = no correct)
                    hasSame = False

                    for k, elem in enumerate(branch):
                        if not hasSame and (exDir(elem[0]) == dir or exDir(elem[0]) == 2):
                            firstSame = k
                            hasSame = True
                        if exDir(elem[0]) != dir and exDir(elem[0]) != 2:
                            if not difCombo:
                                lastDif = k
                                difCombo = True
                        else:
                            difCombo = False
                    print("elem: " + elem[0] +
                          " lastDif: " + str(lastDif) + " difCombo: " + str(difCombo) + " firstSame: " + str(
                        firstSame))

                    for k, elem in enumerate(branch):
                        if exDir(elem[0]) != dir and exDir(elem[0]) != 2:  # incorrect direction
                            # print(elem[0]+" "+str(k)+" "+str(len(branch) -1) + " "+str(offMax))
                            newOffMax = measure(elem, dir) + int(elem[0] in 'ċh') * UNIT / SCALE
                            if newOffMax > offMax and (alter != 1 or k < firstSame or firstSame == -1) \
                                    and (alter != -1 or difCombo and k >= lastDif):
                                offMax = newOffMax
                        else:
                            if offMax > 0:
                                print(str(j) + " added offMax " + str(offMax))
                            spaces[j] += offMax
                            offMax = 0
                            spaces[j] += measure(elem, dir)
                        alter *= -1
                    if offMax > 0:
                        print(str(j) + " added offMax " + str(offMax))
                    spaces[j] += offMax

                print(spaces)
                print("dir: " + str(dir))
                print("len: " + str(len(comp)))

                if mazeMode:
                    tmpFirstStartXor = t.xcor()
                    tmpFirstStartYor = t.ycor()
                    print("tmpcoordy", t.xcor(), t.ycor())
                    tmpFirstEndDir = firstEndDir
                    tmpT = t
                    t = trace
                    t.color("gray")
                    traceAngle = angle
                    tmpAngle = angle
                    tmpCurDivDir = curDivDir
                    angle = traceAngle
                    tryChances = CHANCES
                    if dir != dirPre:
                        while tryChances > 0:
                            curDivDir = random.choice([0, 1])
                            shortestDist = -1  # distance from the starting point (originX, originY)
                            result = [[-1, []], [-1, []]]
                            tried = [daughter[1][0], daughter[2][0]]
                            exploreOpts = []
                            for k in [0, 1]:
                                if not tried[k]:
                                    exploreOpts.append(k)
                            for divDir in exploreOpts:
                                t.hideturtle()
                                t.penup()
                                t.setpos(tmpFirstStartXor, tmpFirstStartYor)
                                firstEndDir = tmpFirstEndDir  # prevent influence from already drawn divergent path
                                # (the stem's end direction does not belong to it!)
                                t.showturtle()
                                t.pendown()
                                calibrate(dirPre, normalDir=tmpCurDivDir)
                                print("calibrated to", angle, dirPre, curDivDir)
                                t.forward(UNIT / 2 * (CHANCES - tryChances))  # try to space out
                                result[divDir] = drawFuseau(comp, spaces.copy(), divDir)
                                if result[divDir] == -1:
                                    tried[divDir] = True  # collided -> mark as explored
                                    continue
                                dist = round(result[divDir][0], ROUND)
                                print("div dir: " + str(divDir) + " dist: " + str(dist))
                                if shortestDist == -1 or shortestDist != -1 and dist < shortestDist:
                                    shortestDist = dist
                                    curDivDir = divDir
                                    tmpBoxLst = result[divDir][1]
                                    tmpBoxNum = result[divDir][2]
                                    tmpStepAcc = result[divDir][3]
                            t.clear()
                            t.hideturtle()
                            if result[0] == -1 and result[1] == -1:
                                tryChances -= 1
                            else:
                                break

                        t = tmpT
                        angle = tmpAngle
                        firstEndDir = tmpFirstEndDir

                        calibrate(dirPre, normalDir=tmpCurDivDir)
                        t.forward(UNIT / 2 * (CHANCES - tryChances))

                        daughter[0] = [-1, dir, curDivDir, curAlter, lastIsFuseau,
                                       -1, -1, firstEndDir, dirPre, tmpBoxNum, -1]

                        for k in [0, 1]:
                            daughter[k + 1][0] = tried[k]
                        if result[0] == -1 and result[1] == -1:
                            retrace()
                            continue
                        else:
                            explore(comp, tmpBoxLst, spaces=spaces, isFuseau=True)
                    else:
                        result = -1
                        while tryChances >= 0:  # try chances = 0 means we just used the last chance
                            if result != -1:  # did not collide
                                print("finished", tryChances)
                                t.clear()
                                t.hideturtle()
                                t = tmpT
                                angle = tmpAngle
                                firstEndDir = tmpFirstEndDir
                                calibrate(dir, normalDir=curDivDir)
                                t.forward(UNIT / 2 * (CHANCES - tryChances - 1))
                                tmpBoxLst = result[1]
                                tmpBoxNum = result[2]
                                tmpStepAcc = result[3] + 2

                                daughter[0] = [-1, -1, curDivDir, curAlter,
                                               lastIsFuseau, -1, -1, firstEndDir, dirPre, tmpBoxNum, -1]

                                explore(comp, tmpBoxLst, spaces=spaces, isFuseau=True)
                                break
                            else:
                                if tryChances == 0:
                                    break  # you have lost all your chances, then get out!
                                t.clear()
                                t.hideturtle()
                                t.penup()
                                t.setpos(tmpFirstStartXor, tmpFirstStartYor)
                                firstEndDir = tmpFirstEndDir
                                t.showturtle()
                                t.pendown()
                                print("still trying", t.xcor())
                                calibrate(dir, normalDir=curDivDir)
                                t.forward(UNIT / 2 * (CHANCES - tryChances))  # try to space out
                                print("still trying", t.xcor())
                                result = drawFuseau(comp, spaces.copy(), curDivDir)
                                print("result", result)
                            tryChances -= 1
                        if result == -1 and tryChances == 0:  # used up all the chances
                            t.clear()
                            t.hideturtle()
                            t = tmpT
                            angle = tmpAngle

                            daughter[0] = [-1, dir, curDivDir, curAlter,
                                           lastIsFuseau, -1, -1, firstEndDir, dirPre, tmpBoxNum, -1]

                            daughter[curDivDir + 1][0] = True
                            retrace()
                            continue
                else:
                    drawFuseau(comp, spaces, curDivDir)
\
                if periodMode:
                    hollowDot()
                lastIsFuseau = True  # for the next fuseau's reference
                print("firstEndDir", firstEndDir)
            else:
                print("data " + str(dir) + " " + str(firstEndDir) + " " + str(exDir(comp[0])))
                if lastIsFuseau and firstEndDir != dir and exDir(comp[0]) != dir:
                    t.forward(UNIT)

                if mazeMode:
                    preXor = t.xcor()
                    preYor = t.ycor()
                    tmpT = t
                    t = trace
                    t.color("gray")
                    traceAngle = angle
                    tmpAngle = angle
                    angle = traceAngle
                    if exDir(comp[0]) != dir and exDir(comp[0]) != 2:
                        shortestDist = -1  # distance from the starting point (originX, originY)
                        curDivDir = random.choice([0, 1])
                        collided = [[], []]
                        tried = [daughter[1][0], daughter[2][0]]
                        exploreOpts = []
                        for k in [0, 1]:
                            if not tried[k]:
                                exploreOpts.append(k)
                        for divDir in exploreOpts:
                            mirror = [1, -1][divDir]
                            print("mirror: " + str(mirror) + " alter: " + str(curAlter))
                            t.hideturtle()
                            t.penup()
                            t.setpos(preXor, preYor)
                            t.showturtle()
                            t.pendown()

                            drawElem(comp[0], normalDir=divDir, alter=curAlter, accent=comp[1], layer=comp[2])
                            print("drawing", comp[0])

                            bx = calcBox(comp, curAlter, mirror, preXor, preYor)
                            for box in bx[0]:
                                collided[divDir] += checkCollision(box[0], box[1], box[2], box[3])

                            if not collided[divDir]:
                                dist = round(math.sqrt((t.xcor() - originX) ** 2 + (t.ycor() - originY) ** 2),
                                             ROUND)
                                print("div dir: " + str(divDir) + " dist: " + str(dist))
                                print("origin", originX, originY, "this", t.xcor(), t.ycor())
                                if shortestDist == -1 or shortestDist != -1 and dist < shortestDist:
                                    shortestDist = dist
                                    curDivDir = divDir
                                    bestBoxes = bx[0]
                            else:
                                for box in bx[0]:
                                    #drawRect(box[0] + 1, box[1] + 1, box[2] - 1, box[3] - 1, color="green")
                                    print(box[0] + 1, box[1] + 1, box[2] - 1, box[3] - 1, curAlter, mirror)
                                    print("---------\n", collided[divDir])
                                # for (c, x1o, y1o, x2o, y2o) in boxLst:
                                    # print(c, x1o, y1o, x2o, y2o)
                                    # drawRect(x1o, y1o, x2o, y2o, color="red")
                                tried[divDir] = True  # mark as explored
                        print("curDivDir: " + str(curDivDir))
                        t.clear()
                        t.hideturtle()
                        t = tmpT
                        angle = tmpAngle

                        daughter[0] = [-1, dir, curDivDir, curAlter, lastIsFuseau,
                                       comp[1], comp[2], firstEndDir, dirPre, len(bx[0]), comp[0]]

                        for k in [0, 1]:
                            daughter[k + 1][0] = tried[k]
                        if tried[0] and tried[1]:  # either collided in both cases or collided in the vacant
                            # direction during retracing
                            print("stop!")
                            retrace()
                            continue
                        else:
                            explore(comp, bestBoxes)
                    else:
                        t.hideturtle()
                        t.penup()
                        t.setpos(preXor, preYor)
                        t.showturtle()
                        t.pendown()
                        print('drawing', comp[0])
                        drawElem(comp[0], normalDir=curDivDir, alter=curAlter, accent=comp[1], layer=comp[2])
                        mirror = [1, -1][curDivDir]
                        collided = []
                        bx = calcBox(comp, curAlter, mirror, preXor, preYor)
                        for box in bx[0]:
                            collided += checkCollision(box[0], box[1], box[2], box[3])

                        t.clear()
                        t.hideturtle()
                        t = tmpT
                        angle = tmpAngle

                        daughter[0] = [-1, -1, curDivDir, curAlter, lastIsFuseau,
                                       comp[1], comp[2], firstEndDir, dirPre, len(bx[0]), comp[0]]
                        # -1 records that this component is not a divergent node

                        daughter[curDivDir + 1][0] = True

                        if collided:
                            print("stoppy", exDir(comp[0]), dir)
                            retrace()
                            continue
                        else:
                            explore(comp, bx[0])
                else:
                    drawElem(comp[0], normalDir=curDivDir, alter=curAlter, accent=comp[1], layer=comp[2])
                if periodMode:
                    hollowDot()
                if exDir(comp[0]) == 2:
                    dir = angle2dir(angle)
                else:
                    dir = exDir(comp[0])
                calibrate(dir, normalDir=curDivDir)
                curAlter *= -1
                lastIsFuseau = False
                print("dir before new element", dir, comp[0])
            dirPre = dir  # the direction of the element directly preceding the component (element/fuseau)
            compInd += 1
        t.penup()
        if not periodMode:
            t.forward(UNIT)
        # t.setpos(t.xcor() - UNIT, - screen.window_height() / 2 + TURTLE_SIZE / 2 + MARGIN)
        t.pendown()
        i += 1


def main():
    readResult = ItiParser.read(txt)
    passageLst = readResult[0]
    compNum = readResult[1]
    print(passageLst)
    print(compNum)
    # t.screensize(WIDTH, HEIGHT)
    t.speed(0)
    if rapidMode:
        screen.tracer(0, 0)
    t.setundobuffer(100000000)
    t.penup()
    t.goto(originX, originY)
    # t.goto(WIDTH / 2 - MARGIN, -HEIGHT / 2)
    t.pendown()
    t.left(180)
    t.showturtle()
    if mazeMode:
        trace.speed(0)
        trace.left(180)
        trace.hideturtle()
    draw(passageLst)
    if exportMode:
        t.save_as("./example2.svg")
        print("successfully generated the image")
    screen.mainloop()


main()
