import pyqtree
import ItiParser
from turtle import Turtle, Screen
from svg_turtle import SvgTurtle
import math
import random

random.seed(819)
WIDTH = 5000
HEIGHT = 5000
TURTLE_SIZE = 20
MARGIN = 50
UNIT = 50
SCALE = 5
ROUND = 2
MAGNIFICATION = 20
CHANCES = 4
txt = '''
Ưrah rơm, izucun. Ucunizaṡ, ĩhemõṡũl. Itaé gớt, izupun. Upunizág, ĩhemõṡũl. Ưtar ịtát, íábipaé ghom. Ĩrágót, itatư bah ésehomoż. Ưbẽhonós. Ưżuṡazailian. Uṡaz: Upun atư bah, édhom éctaupuzużuċul. Éṡb ẻtớtaulupużuzuluċul, atifẽ hơm ịfusus. Ipáde żơt, rarmoż, mơt mơc ịfẽ hơm. Ágizud, ĩmabon? Ibe mfiáhailiág? Ibzaé gơc ịpr. Hơm ịzásiláṡ, izátilaé dơṡ. Bớs échom óv, izaribád, ré cớs ịzaé sơċ, ifẽ hmód ịbẽ ṡớd. Évhom ịzásiláṡ, izátilẻ bơṡ. Izulupużuzuluċul ifaé vehomód, itrfaé vhom. Ágé gud ịlár, itrẽ ruput bah. Brũt ịbư żágót ưzab ịbaz: Ĩram żớt, tde rớtũy ịbẽ rớtũf. Ĩbz olatditaé dơh óciṡ, ĩmz õtulupużuzuluċul itatư bah? Te gơh ịzư faṡot ogitac, mizaripaṡ. Tucututulu izabitẽ rơṡ ịrtuh. Tucużupuċulu izapṡirtufus. Ĩrulõr ĩmz õrz! Rraz ĩlgõ ṡraz, ritig lgõ ṡitig. Ĩmz õrzir? Ẽraremoṡũżuż ịlarzuṡibuh, ẽbrũhug ịlarzudibus, ĩrtigõr. Ưżah ịzubizé gnũmul, użuzutugizud, użuzutugizus; ĩcr ohgzẽ ṡerótũż, ucużupuċuċugizud, ucużupuċuċugizus. Ibrư puzal otrifẽ ṡitig, idabe mơṡ, ĩml ũfu!
	'''
# txt = "e'ezubo'uatíd ẽca'efuro'íg"
txt = "e'e'e'e'e'e'e'e'e'e'etto'to'to'to'to'to'to'to'to'to't e'e'e'e'e'e'e'e'e'e'etto'to'to'to'to'to'to'to'to'to't e'e'e'e'e'e'e'e'e'e'etto'to'to'to'to'to'to'to'to'to't e'e'e'e'e'e'e'e'e'e'etto'to'to'to'to'to'to'to'to'to't".replace('t', 'c')
# txt = "mil"
guideTree = ['parallel', ['series', ['h', 1, 0]], ['series', ['c', 1, 0], ['parallel', ['series', ['h', 0, 0]], ['series', ['c', 0, 0], ['parallel', ['series', ['c', 1, 0]], ['series', ['t', 0, 0]], ['series', ['ṡ', 0, 0]], ['series', ['ṡ', 1, 0]]],
                ['parallel', ['series', ['t', 1, 0]], ['series', ['t', 0, 0]]], ['t', 0, 0]]],
                ['parallel', ['series', ['h', 0, 0]], ['series', ['c', 0, 0],
                  ['parallel', ['series', ['c', 1, 0]], ['series', ['c', 0, 0]]],
                  ['parallel', ['series', ['t', 1, 0]], ['series', ['c', 0, 0]]], ['t', 0, 0]]], ['t', 1, 0]
                                                 ]]
quadIndex = pyqtree.Index(bbox=[-WIDTH / 2, -HEIGHT / 2, WIDTH / 2, HEIGHT / 2])
screen = Screen()
width, height = screen.screensize()
screen.screensize(width * MAGNIFICATION, height * MAGNIFICATION)
canvas = screen.getcanvas()
canvas.config(xscrollincrement=str(MAGNIFICATION))
canvas.config(yscrollincrement=str(MAGNIFICATION))

centerMode = True
mazeMode = True
exportMode = False
periodMode = True
rapidMode = False
drawMode = False

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
divDirPre = 0
sent = []
boxLst = []
history = []
undoStepAcc = 0
nextPeriod = False
innerWidthCode = 0
innerLengthCode = 0
global firstEndXor
global firstEndYor
global firstEndDir
global firstStartXor
global firstStartYor
global curAlter
global lastIsFuseau
global compInd
global daughter
global innerLengths  # lengths of the inner fuseaux. To locate, use (depth, j, k)
global innerWidths  # widths of the inner fuseaux.


def exDir(c):
    if c in 'ṡsbdnvrgh-':  # passive
        return 0
    elif c in 'żzptmflcċ|':  # active
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
    if layer != 0:
        dist = 1.5 + abs(layer)
    elif c in 'ṡższvf':
        dist = 2.5
    elif c in 'yw|-ċh':
        dist = 1
    elif c in 'mn':
        dist = 2
    else:
        dist = 1.5
    return dist * UNIT / SCALE


def calcPos(c, accent):  # returns the distance for stepping back
    if accent == 1:
        if c in 'żṡpbmnlrċhyw|-':
            return UNIT / 2
        elif c in 'zstd':
            return UNIT - UNIT / SCALE
        elif c in 'fvcg':
            return UNIT / SCALE
    elif accent == 2:
        if c in 'żṡpbmnlrċhyw|-':
            return UNIT * 2 / 3
        elif c in 'zstd':
            return UNIT
        elif c in 'fvcg':
            return UNIT / 3
    else:
        return 0


def drawElem(c, normalDir=0, alter=1, layer=0, accent=0, isElem=False):  # normalDir: 0 = normal, 1 = mirrored, alter:
    # alternative directions
    global dir
    global curDivDir
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
    if c in 'yw|-':
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

    if layer < 0:
        for i in range(abs(layer)):
            t.penup()
            if alter != 1:
                t.forward(-UNIT)
            t.right(90 * alter)
            print("layer count", i)
            t.forward(UNIT / SCALE * (i + 1) + UNIT / 2)
            t.right(180)
            t.pendown()
            t.circle(UNIT / 2, 180)
            t.penup()
            t.right(180)
            t.forward(UNIT / SCALE * (i + 1) + UNIT / 2)
            t.right(90 * alter)
            if alter == 1:
                t.forward(UNIT)
            t.pendown()

    if layer > 0:
        for i in range(abs(layer)):
            t.penup()
            if alter == 1:
                t.forward(-UNIT)
            t.right(90 * alter)
            t.forward(UNIT / SCALE * (i + 1))
            t.pendown()
            t.circle(UNIT / 2, 180)
            t.penup()
            t.forward(UNIT / SCALE * (i + 1))
            t.right(90 * alter)
            if alter != 1:
                t.forward(UNIT)
            t.pendown()

    if isElem:
        if exDir(c) == 2:
            dir = angle2dir(angle)
        else:
            dir = exDir(c)
        calibrate(dir, normalDir=curDivDir)


def undoRep(n):
    global t
    for i in range(n):
        t.undo()


def countSteps(c, alter=1, accent=0, layer=0):
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
    if c in 'yw|-':
        steps += 1
    if accent == 1:
        steps += 12
    if accent == 2:
        steps += 17
    if layer < 0:
        steps += 12 * abs(layer)
    if layer > 0:
        steps += 10 * abs(layer)
    return steps


def undoElem(c, alter=1, accent=0, layer=0):
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
    return quadIndex.intersect(bbox=[x1, y1, x2, y2])


def calcBox(elem, alter, mirror, preXor, preYor, mirror2=1, side=1):
    global t
    global dir
    if exDir(elem[0]) == 0 or exDir(elem[0]) == 2 and dir == 0:
        checkDir = 1
        add = measure(elem, checkDir) * side * alter * mirror * mirror2
        postXor = t.xcor()
        postYor = t.ycor() + add * int(elem[0] not in 'ċh')
    if exDir(elem[0]) == 1 or exDir(elem[0]) == 2 and dir == 1:
        checkDir = 0
        add = measure(elem, checkDir) * side * alter * mirror * mirror2
        postXor = t.xcor() + add * int(elem[0] not in 'ċh')
        postYor = t.ycor()
    print("calc box", elem[0], t.ycor(), measure(elem, checkDir), side, alter, mirror, mirror2)

    boxes = calcPreciseBox(elem[0], preXor, preYor, postXor, postYor,
                           add=add)
    sortedBoxes = []

    for box in boxes:
        x1 = round(min(box[0], box[2]), ROUND)
        x2 = round(max(box[0], box[2]), ROUND)
        y1 = round(min(box[1], box[3]), ROUND)
        y2 = round(max(box[1], box[3]), ROUND)
        sortedBoxes.append((x1 + 1, y1 + 1, x2 - 1, y2 - 1))

    return sortedBoxes, postXor, postYor


def calcPreciseBox(c, x1, y1, x2, y2, add=0):
    global dir
    offSetX = 0
    offSetY = 0
    offSetX2 = 0
    offSetY2 = 0
    offSetX3 = 0
    offSetY3 = 0
    if exDir(c) == 0 or exDir(c) == 2 and dir == 0:
        ind = 0
        forward = 2 * int((x2 - x1) >= 0) - 1  # positive -> 1, negative -> -1
        offSetY = 2 * int((y2 - y1) >= 0) - 1  # minimal thickness
        if c in 'td':
            offSetX2 = UNIT / SCALE * forward
            offSetX3 = x2 - x1
        elif c in 'cg':
            offSetX2 = x2 - x1 - UNIT / SCALE * forward
        elif c in 'ċh':
            offSetX2 = (UNIT / 2 + UNIT / SCALE / 2) * forward
        else:
            offSetX2 = x2 - x1
    if exDir(c) == 1 or exDir(c) == 2 and dir == 1:
        ind = 1
        forward = 2 * int((y2 - y1) >= 0) - 1
        offSetX = 2 * int((x2 - x1) >= 0) - 1  # minimal thickness
        if c in 'td':
            offSetY2 = UNIT / SCALE * forward
            offSetY3 = y2 - y1
        elif c in 'cg':
            offSetY2 = y2 - y1 - UNIT / SCALE * forward
        elif c in 'ċh':
            offSetY2 = (UNIT / 2 + UNIT / SCALE / 2) * forward
        else:
            offSetY2 = y2 - y1

    if c in 'td':
        boxes = [(x1 + offSetX2 - offSetX, y1 + offSetY2 - offSetY,
                  x1 + offSetX3 + offSetX * 2, y1 + offSetY3 + offSetY * 2)]
    elif c in 'cg':
        boxes = [(x1 - offSetX, y1 - offSetY, x1 + offSetX2 + offSetX * 2, y1 + offSetY2 + offSetY * 2)]
    elif c in 'ċh':
        boxes = [(x1 - offSetX, y1 - offSetY, x1 + offSetX2 + offSetX * 2, y1 + offSetY2 + offSetY * 2),
                 (x2 - offSetX2 + offSetX, y2 - offSetY2 + offSetY, x2 - offSetX * 2, y2 - offSetY * 2)]
    else:
        boxes = [(x1 - offSetX, y1 - offSetY, x1 + offSetX2 + offSetX * 2, y1 + offSetY2 + offSetY * 2)]

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
        rect2[ind] += (2 * UNIT / SCALE + 1 - UNIT) * forward
    if c in 'mn':
        rect1[ind] += UNIT / SCALE * forward
        rect2[ind] -= UNIT / SCALE * forward
    if c in 'fv':
        rect1[ind] += (UNIT - 2 * UNIT / SCALE) * forward
    if c in 'lr':
        rect1[ind] += (UNIT / 2 - UNIT / SCALE / 2 - 1) * forward
        rect2[ind] += (UNIT / SCALE / 2 + 1 - UNIT / 2) * forward
    if c in 'cg':
        rect1[ind] += (UNIT - 2 * UNIT / SCALE - 1) * forward
        rect2[ind] -= UNIT / SCALE * forward
    if c in 'ċh':
        rect1[ind] += (UNIT / 2 - UNIT / SCALE / 2) * forward
        rect2[ind] += (UNIT / SCALE / 2 - UNIT / 2) * forward
        rect2[1 - ind] += add
    if c not in 'yw|-':  # yw only occupies the line
        boxes.append((rect1[0], rect1[1], rect2[0], rect2[1]))

    return boxes


def measure(elem, checkDir, measureExtra=True):
    c = elem[0]
    accent = elem[1]
    layer = elem[2]
    extra = 0
    if (c in 'ṡsbdnvrgh-' and checkDir == 0) or (c in 'żzptmflcċ|' and checkDir == 1) \
            or (c in 'yw' and checkDir == dir):  # same
        base = UNIT
    elif (c in 'ṡsbdnvrgh-' and checkDir == 1) or (c in 'żzptmflcċ|' and checkDir == 0) \
            or (c in 'yw' and checkDir != dir):  # different
        if c in 'ṡsvżzf':
            base = UNIT * 2 / SCALE
        else:
            base = UNIT / SCALE
        if measureExtra:
            extra = max(calcDist(c, accent, layer), int(layer != 0) * (UNIT / 2 + UNIT / SCALE * abs(layer)))
        if extra != 0:
            # print("extra: " + str(extra))
            return extra  # extra length measured
    return base


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


def drawFuseau(comp, lengths, widths, tmpDir, tmpDivDir, inner=False, depth=0, side=1):
    global angle
    global firstEndXor
    global firstEndYor
    global firstEndDir
    global firstStartXor
    global firstStartYor
    global boxLst
    global drawMode
    global innerLengths
    global innerWidths

    voteLengths = lengths.copy()
    for j in range(len(voteLengths)):
        if isFuseau(comp[j][0]):
            voteLengths[j] = 1  # eliminate fuseaux branch
    maxLength = max(voteLengths)
    maxIndex = voteLengths.index(maxLength)
    print("angle first", angle)
    calibrate(tmpDir, normalDir=tmpDivDir)
    print("angle", angle)
    print("data " + str(tmpDir) + " " + str(dirPre) + " " + str(firstEndDir))
    if not isFuseau(comp):
        print(exDir(comp[maxIndex][0][0]))

    if not inner:
        if (exDir(comp[maxIndex][0][0]) != tmpDir and exDir(comp[maxIndex][0][0]) != 2) and dirPre != tmpDir:
            t.forward(UNIT)
        elif lastIsFuseau and firstEndDir != dirPre and (exDir(comp[maxIndex][0][0]) != dirPre
                                                         and not (dirPre == tmpDir and exDir(comp[maxIndex][0][0]) == 2)):
            calibrate(dirPre)
            t.forward(UNIT)

    firstEndXor = 0  # merely initializing
    firstEndYor = 0
    firstStartXor = t.xcor()
    firstStartYor = t.ycor()  # original x before drawing
    print("firstStartXor", t.xcor(), "firstStartYor", t.ycor())
    # side = 1  # -1 = left, 1 = right
    distSum = 0
    tmpBoxLst = []
    boxNum = 0

    for j in range(len([branch for branch in comp if not isPair(branch)])):
        lastIsInnerFuseau = False
        innerFirstEndDir = -1
        alter = 1
        print("drawing: vote Lengths", voteLengths)
        chosenLength = max(voteLengths)
        chosenIndex = voteLengths.index(chosenLength)
        print("drawing: chosen index", chosenIndex, comp[chosenIndex], "comp", comp, "j", j, 'alter', alter, 'widths', widths)
        if j != 0:  # not the first branch
            lastStep = sum([widths[i] for i in range(j % 2, j + 1, 2)])
            firstElem = comp[chosenIndex][0]
            t.right(90 * side)
            angle -= 90 * side
            t.penup()
            t.forward(lastStep)
            print("sideways step:", lastStep, "angle:", angle, "side:", side)
            t.left(90 * side)
            angle += 90 * side
            hasSame = False
            for elem in comp[chosenIndex]:
                if isPair(elem):
                    continue
                if not isFuseau(elem) and (exDir(elem[0]) == tmpDir or exDir(elem[0]) == 2):
                    hasSame = True
            if hasSame:
                print("overall aligned to middle", comp[j], maxLength, chosenLength)
                t.forward((maxLength - chosenLength) / 2)
            else:
                print("point aligned to middle", comp[j], maxLength)
                t.forward(maxLength / 2)
            if isFuseau(firstElem):
                if hasSame:
                    add = sum([innerWidths[firstElem[-1][1]][i] for i in
                               range(1, len(innerWidths[firstElem[-1][1]]), 2)])
                    t.forward(add)
                    # adjust the starting point
                    print("added", add)
                    print("adjusted the chosen component")
            else:
                if exDir(firstElem[0]) != tmpDir and exDir(firstElem[0]) != 2 and hasSame:
                    t.forward(measure(firstElem, tmpDir))  # adjust the starting point
                    print("adjusted the chosen component")
            maxFirst = comp[maxIndex][0]  # the stem component's first element
            if isFuseau(maxFirst):
                t.forward(-sum([innerWidths[maxFirst[-1][1]][i] for i in
                                range(1, len(innerWidths[maxFirst[-1][1]]), 2)]))
                # adjust the starting point
                print("aligned to the stem component")
            elif exDir(maxFirst[0]) != tmpDir and exDir(maxFirst[0]) != 2:
                t.forward(-measure(maxFirst, tmpDir))  # adjust the starting point
                print("aligned to the stem component")
            print('(' + str(maxLength) + '-' + str(chosenLength) + ')/2=' + str((maxLength - chosenLength) / 2))

            t.pendown()

        for k, elem in enumerate(comp[chosenIndex]):
            if isPair(elem):
                continue
            print("now vote", voteLengths, k, elem)
            if isFuseau(elem):
                tmpAngle = angle
                tmpFirstEndXor = firstEndXor
                tmpFirstEndYor = firstEndYor
                tmpFirstEndDir = firstEndDir
                tmpFirstStartXor = firstStartXor
                tmpFirstStartYor = firstStartYor
                print("fus Length", innerLengths, "comp", comp, j, k, side)
                mirror2 = [1, -1][tmpDivDir]  # mirror for divergent paths in maze mode
                if tmpDir == 0 and side == -1 or tmpDir == 1 and side == 1:
                    mirror = -1
                else:
                    mirror = 1
                if mirror * mirror2 == -1:
                    normalDir = 1  # mirror (i.e. 1) * mirror2
                else:
                    normalDir = 0
                result = drawFuseau(elem, innerLengths[elem[-1][0]], innerWidths[elem[-1][1]],
                           1 - tmpDir, normalDir, inner=True, depth=depth + 1, side=side)
                if result == -1:
                    return -1
                else:
                    distSum += result[0]
                    tmpBoxLst += result[1]
                    boxNum += result[2]
                angle = tmpAngle
                firstEndXor = tmpFirstEndXor
                firstEndYor = tmpFirstEndYor
                innerFirstEndDir = firstEndDir
                firstEndDir = tmpFirstEndDir
                firstStartXor = tmpFirstStartXor
                firstStartYor = tmpFirstStartYor
                lastIsInnerFuseau = True
            else:
                print('lastIsInnerFuseau', lastIsInnerFuseau, 'innerFirstEndDir', innerFirstEndDir, '1 - tmpDir', 1 - tmpDir, 'elem', elem[0])
                if lastIsInnerFuseau and innerFirstEndDir != -1 and innerFirstEndDir != 1 - tmpDir\
                        and innerFirstEndDir != 2 and exDir(elem[0]) != 1 - tmpDir and exDir(elem[0]) != 2:
                    # avoid ambiguity between the inside and the outside of the inner fuseau
                    print("need to extend")
                    calibrate(tmpDir, int(side != 1))
                    t.forward(UNIT)
                    if j + 2 < len(widths):
                        widths[j + 2] += UNIT
                    calibrate(tmpDir, int(side != 1))
                    lastIsInnerFuseau = False
                    innerFirstEndDir = -1
                print("elem name", elem[0], "alter state", alter, "side state", side)
                preXor = t.xcor()
                preYor = t.ycor()
                mirror2 = [1, -1][tmpDivDir]  # mirror for divergent paths in maze mode
                if (exDir(elem[0]) == 1 and tmpDir == 0 and side == -1) or \
                        (exDir(elem[0]) == 0 and tmpDir == 1 and side == 1):
                    mirror = -1
                else:
                    mirror = 1
                if mirror * mirror2 == -1:
                    normalDir = 1  # mirror (i.e. 1) * mirror2
                else:
                    normalDir = 0
                drawElem(elem[0], normalDir, alter=side * alter, accent=elem[1], layer=elem[2])

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
                            if drawMode:
                                drawRect(x1, y1, x2, y2, color='green')
                            print(x1, y1, x2, y2, alter, mirror)
                            print("---------\n", collided)
                            if drawMode:
                                for (c, x1o, y1o, x2o, y2o) in boxLst:
                                    print(c, x1o, y1o, x2o, y2o)
                                    drawRect(x1o, y1o, x2o, y2o, color='red')
                            print("collided")
                            return -1
                    distSum += math.sqrt((postXor - originX) ** 2 + (postYor - originY) ** 2)
            alter *= -1

        if j == 0:
            firstEndXor = t.xcor()
            firstEndYor = t.ycor()
            if isFuseau(comp[chosenIndex][-1]):
                firstEndDir = 1 - tmpDir
            else:
                firstEndDir = exDir(comp[chosenIndex][-1][0])
            print("first end dir: " + str(firstEndDir) + " dir: " + str(tmpDir))
        side *= -1
        t.penup()
        t.setpos(firstStartXor, firstStartYor)
        t.pendown()
        print("angle last", angle)
        calibrate(tmpDir, normalDir=tmpDivDir)
        print("angle", angle)
        voteLengths[chosenIndex] = 0
        print("erased vote lengths", voteLengths)
    t.penup()
    t.setpos(firstEndXor, firstEndYor)
    t.pendown()
    return distSum, tmpBoxLst, boxNum


def retrace():
    global compInd
    global dir
    global dirPre
    global curDivDir
    global divDirPre
    global curAlter
    global lastIsFuseau
    global daughter
    global firstEndDir
    global undoStepAcc
    global sent
    retraceDir = -1
    retraceTried = [True, True]
    entries = t.undobufferentries()
    print("entries", entries, undoStepAcc, compInd)
    print(daughter[0])
    undoRep(entries - undoStepAcc)
    k = compInd
    while retraceDir == -1 or retraceTried == [True, True]:  # non-divergent or exhausted
        k -= 1
        if sent[k][0] == '.':
            k -= 1

        if k <= 0:
            print("There is no solution!")
            print(daughter)
            exit()
        # go back until encounters a non -1 explorable component

        daughter = daughter[3]  # retrace to the mother layer
        print(daughter[0], daughter[1][0], daughter[2][0], k)
        retraceDir = daughter[0][1]
        retraceTried = [daughter[1][0], daughter[2][0]]
        print("retrace back to", daughter[0][10], "stepAcc", daughter[0][0])
        undoRep(daughter[0][0])
        for i in range(daughter[0][9]):
            quadIndex.remove(boxLst[-1], bbox=[boxLst[-1][1], boxLst[-1][2], boxLst[-1][3], boxLst[-1][4]])
            del boxLst[-1]

    print(daughter[0], daughter[1][0], daughter[2][0], k)
    undoStepAcc = t.undobufferentries()
    compInd = k
    calibrate(daughter[0][1], normalDir=daughter[0][2])
    dir = daughter[0][1]
    curDivDir = daughter[0][2]
    divDirPre = daughter[0][11]
    curAlter = daughter[0][3]
    lastIsFuseau = daughter[0][4]
    firstEndDir = daughter[0][7]
    dirPre = daughter[0][8]
    # [[stepAcc, dir, curDivDir, alter, lastIsFuseau, accent, layer, firstEndDir, dirPre, boxNum, c, divDirPre],
    if rapidMode:
        screen.update()


def explore(comp, lst, lengths=None, widths=None, isFuseau=False):  # explore a lower level
    global dir
    global curDivDir
    global curAlter
    global daughter
    global boxLst
    global undoStepAcc
    global periodMode
    global nextPeriod
    if isFuseau:
        tmpBoxLst = lst
        drawFuseau(comp, lengths, widths, dir, curDivDir)
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
        drawElem(comp[0], normalDir=curDivDir, alter=curAlter, accent=comp[1], layer=comp[2], isElem=True)
    if periodMode and nextPeriod:
        hollowDot()
        nextPeriod = False
    entries = t.undobufferentries()
    print("compare", entries, undoStepAcc, entries - undoStepAcc)
    daughter[0][0] = entries - undoStepAcc
    undoStepAcc = entries
    mother = daughter  # record the mother for retracing
    daughter[curDivDir + 1][0] = True  # mark as explored
    print("explored", daughter[0], daughter[1][0], daughter[2][0], compInd)
    daughter = daughter[curDivDir + 1][1]  # become the structure nested inside (enter the deeper level)
    if not daughter:
        daughter += [-1, [False, []], [False, []], mother]  # create the deeper structure of history


def isFuseau(comp):
    return isinstance(comp[0], list) and isinstance(comp[0][0], list)  # branch and elem


def allocWidth(comp, tmpDir, lengths, depth=0):
    global innerWidths

    voteLengths = lengths.copy()
    for j in range(len(voteLengths)):
        if isFuseau(comp[j][0]):
            voteLengths[j] = 1  # eliminate branches starting with a fuseau
    widths = [0]
    side = 1

    for j in range(len([branch for branch in comp if not isPair(branch)])):
        alter = 1
        print("vote Lengths", voteLengths)
        chosenLength = max(voteLengths)
        chosenIndex = voteLengths.index(chosenLength)
        print("chosen index", chosenIndex, comp[chosenIndex], widths, side)

        offMax = 0  # the widest offset until we meet an element with the incorrect direction
        offMaxBack = 0  # serves for the stem's back
        curWidth = 0
        if j > 0:
            firstElem = comp[chosenIndex][0]

            if not isFuseau(firstElem) and (exDir(firstElem[0]) == tmpDir or exDir(firstElem[0]) == 2):
                # widths[j] += UNIT / SCALE * 1.5
                widths[j] += UNIT / SCALE
                print("adding equal interval", curWidth, firstElem, j, curWidth, widths)

        lastSame = -1  # the start index of the last sequence of elements with the correct direction
        sameCombo = False  # there is a sequence with the correct direction
        # (see if it is still true at the end)
        firstDif = -1  # the index of the first element with the incorrect direction
        hasDif = False

        for k, elem in enumerate(comp[chosenIndex]):
            if isPair(elem):
                continue
            if not hasDif and (isFuseau(elem) or exDir(elem[0]) != tmpDir and exDir(elem[0]) != 2):
                firstDif = k
                hasDif = True
            if not isFuseau(elem) and (exDir(elem[0]) == tmpDir or exDir(elem[0]) == 2):
                if not sameCombo:
                    lastSame = k
                    sameCombo = True
            else:
                sameCombo = False

        print(
            "lastSame: " + str(lastSame) + " sameCombo: " + str(sameCombo) + " firstDif: " + str(firstDif))

        for k, elem in enumerate(comp[chosenIndex]):
            if isPair(elem):
                continue
            # notice that we replace j with chosenIndex, mapping widths (not innerWidths) directly to the order of votes
            if not isFuseau(elem) and (exDir(elem[0]) == tmpDir or exDir(elem[0]) == 2):
                newOffMax = measure(elem, 1 - tmpDir) \
                    # + int(elem[0] in 'ċh') * UNIT / SCALE
                if newOffMax > offMax and \
                        (alter != -1 and (alter != 1 or sameCombo and k >= lastSame)):
                    offMax = newOffMax
                    print("update " + elem[0] + " " + str(k) + " " + str(offMax))

                newOffMaxBack = measure(elem, 1 - tmpDir) \
                    # + int(elem[0] in 'ċh') * UNIT / SCALE
                print("new off max back", newOffMaxBack, 'tmpdir', tmpDir, "alter", alter, "k", k, "firstDir", firstDif)
                if j == 0 and newOffMaxBack > offMaxBack and alter == -1 and \
                        (k < firstDif or firstDif == -1) and elem[0] not in '|-':
                    offMaxBack = newOffMaxBack
            else:
                if offMax > 0:
                    print("added offMax " + str(offMax))
                curWidth += offMax
                offMax = 0

                if isFuseau(elem):
                    curWidth += max(innerLengths[elem[-1][0]])
                    print("added fuseau", max(innerLengths[elem[-1][0]]))
                else:
                    curWidth += measure(elem, 1 - tmpDir)
                    print("added " + elem[0] + " " + str(measure(elem, 1 - tmpDir)))
            alter *= -1

        if offMax > 0:
            print("added offMax (the rest) " + str(offMax))
        curWidth += offMax
        if j == 0:
            print("curWidth", curWidth, "offMaxBack ", offMaxBack)
            widths.append(offMaxBack)
            widths.append(curWidth)
        else:
            print("curWidth", curWidth)
            widths.append(curWidth)
        voteLengths[chosenIndex] = 0
        side *= -1
        print("widths", widths)
    return widths[:len([branch for branch in comp if not isPair(branch)])]

def isPair(lst):
    return isinstance(lst, list) and len(lst) == 2 and isinstance(lst[0], int) and isinstance(lst[1], int)


def allocLength(comp, tmpDir, depth=0):
    global angle
    global traceAngle
    global dirPre
    global curDivDir
    global divDirPre
    global t
    global firstEndDir
    global curAlter
    global lastIsFuseau
    global history
    global daughter
    global boxLst
    global compInd
    global undoStepAcc
    global periodMode
    global drawMode
    global nextPeriod
    global innerLengths
    global innerWidths
    global innerWidthCode
    global innerLengthCode

    lengths = [0] * len([branch for branch in comp if not isPair(branch)])  # the space that would be occupied by each branch (its length)
    hasFuseauBranches = []
    for j, branch in enumerate(comp):
        offMax = 0  # the widest offset until we meet an element with the correct direction
        alter = 1  # the alter in fuseaux is independent from simple elements
        lastDif = -1  # the start index of the last sequence of elements with the incorrect direction
        difCombo = False  # there is a sequence with the incorrect direction
        # (see if it is still true at the end)
        firstSame = -1  # the index of the first element with the incorrect direction (-1 = no correct)
        hasSame = False

        for k, elem in enumerate(branch):
            if isPair(elem):
                continue

            if isFuseau(elem):
                hasFuseauBranches.append(j)
                inLength, comp[j][k] = allocLength(elem, 1 - tmpDir, depth + 1)
                maxLength = max(inLength)
                dominateGoal = int(maxLength // UNIT + 1)
                print("max length", maxLength, "dominate goal", dominateGoal)
                hasStem = False
                for subBranch in elem:
                    if not isFuseau(subBranch[0]) and exDir(subBranch[0][0]) != tmpDir and exDir(subBranch[0][0]) != 2:
                        hasStem = True
                        print("I have stem")
                if not hasStem:
                    if tmpDir == 0:
                        elem.append([['|', 0, 0]] * dominateGoal)
                    else:
                        elem.append([['-', 0, 0]] * dominateGoal)
                    print("after ext", elem, depth, j, k, inLength)
                    inLength.append(dominateGoal * UNIT)
                innerLengthCode += 1
                if not isPair(elem[-1]):
                    comp[j][k].append([0, 0])
                comp[j][k][-1][0] = innerLengthCode
                innerLengths[innerLengthCode] = inLength
            elif not hasSame and (exDir(elem[0]) == tmpDir or exDir(elem[0]) == 2):
                firstSame = k
                hasSame = True

            if isFuseau(elem) or exDir(elem[0]) != tmpDir and exDir(elem[0]) != 2:
                if not difCombo:
                    lastDif = k
                    difCombo = True
            else:
                difCombo = False

        print("lastDif: " + str(lastDif) + " difCombo: " + str(difCombo) + " firstSame: " + str(
            firstSame))

        for k, elem in enumerate(branch):
            if isPair(elem):
                continue
            print("cur elem", elem)
            if isFuseau(elem):
                innerWidthCode += 1
                if not isPair(elem[-1]):
                    comp[j][k].append([0, 0])
                comp[j][k][-1][1] = innerWidthCode
                innerWidths[innerWidthCode] = allocWidth(elem, 1 - tmpDir, innerLengths[elem[-1][0]], depth + 1)
                print("new inner width", innerWidthCode, innerWidths[innerWidthCode], 1 - tmpDir, elem)
                newOffMax = 0
                if alter != 1 or k < firstSame or firstSame == -1:
                    newOffMax += sum(
                        [innerWidths[elem[-1][1]][i] for i in range(1, len(innerWidths[elem[-1][1]]), 2)])
                if alter != -1 or difCombo and k >= lastDif:
                    newOffMax += sum(
                        [innerWidths[elem[-1][1]][i] for i in range(0, len(innerWidths[elem[-1][1]]), 2)])

                if newOffMax > offMax:
                    print("new off Max", newOffMax, "old off max", offMax)
                    offMax = newOffMax

            elif exDir(elem[0]) != tmpDir and exDir(elem[0]) != 2:  # incorrect direction
                # print(elem[0]+" "+str(k)+" "+str(len(branch) -1) + " "+str(offMax))
                newOffMax = measure(elem, tmpDir) + int(elem[0] in 'ċh') * UNIT / SCALE
                if newOffMax > offMax and (alter != 1 or k < firstSame or firstSame == -1) \
                        and (alter != -1 or difCombo and k >= lastDif):
                    offMax = newOffMax
            else:
                print("j", j, "k", k, "elem", elem, " added offMax", offMax, "tmpDir", tmpDir, "measure", measure(elem, tmpDir))
                lengths[j] += offMax
                offMax = 0
                lengths[j] += measure(elem, tmpDir)
            alter *= -1
        if offMax > 0:
            print(str(j) + " added offMax " + str(offMax))
        lengths[j] += offMax

    if hasFuseauBranches:
        hasFuseauMaxLength = max([lengths[j] for j in hasFuseauBranches])
        dominateGoal = hasFuseauMaxLength

        notFuseauBranchesLengths = [lengths[j] for j in range(len(lengths)) if j not in hasFuseauBranches]
        if not notFuseauBranchesLengths:
            lengths.append(UNIT)
            print("now added", lengths)
            notFuseauBranchesLengths = [UNIT]
            if tmpDir == 0:
                comp.append([['-', 0, 0]])
            else:
                comp.append([['|', 0, 0]])
        maxLength = max(notFuseauBranchesLengths)
        willAddStem = True  # make sure that there will be no stem added afterward if we extend this time
        for j, branch in enumerate(comp):
            if not isFuseau(branch[0]) and (exDir(branch[0][0]) == tmpDir or exDir(branch[0][0]) == 2):
                willAddStem = False
        if dominateGoal > maxLength and (not willAddStem or depth == 0):  # needs to dominate!
            maxLengthInd = lengths.index(maxLength)  # main stem index
            extension = (dominateGoal - maxLength) // UNIT + 1
            tmpComp = comp[maxLengthInd]
            comp[maxLengthInd] = []
            print("ext", extension, tmpComp, dominateGoal, maxLength, tmpDir)
            print(lengths, [lengths[j] for j in range(len(lengths)) if j not in hasFuseauBranches])
            if tmpDir == 0:
                if round(extension / 2 - 0.1) > 0:
                    comp[maxLengthInd] = [['-', 0, 0]] * round(extension / 2 - 0.1)
                comp[maxLengthInd] += tmpComp + [['-', 0, 0]] * round(extension / 2 + 0.1)
            else:
                if round(extension / 2 - 0.1) > 0:
                    comp[maxLengthInd] = [['|', 0, 0]] * round(extension / 2 - 0.1)
                comp[maxLengthInd] += tmpComp + [['|', 0, 0]] * round(extension / 2 + 0.1)
            lengths[maxLengthInd] += extension * UNIT
    print('lengths', lengths, 'comp', comp)
    print("tmpDir: " + str(tmpDir))
    print("len: " + str(len(comp)))
    return lengths, comp


def draw(lst):
    global angle
    global traceAngle
    global dir
    global dirPre
    global curDivDir
    global divDirPre
    global t
    global firstEndXor
    global firstEndYor
    global firstEndDir
    global firstStartXor
    global firstStartYor
    global curAlter
    global lastIsFuseau
    global history
    global daughter
    global boxLst
    global compInd
    global undoStepAcc
    global periodMode
    global drawMode
    global nextPeriod
    global sent
    global innerLengths
    global innerWidths
    if periodMode:  # initialize them only at the beginning if in period mode
        curAlter = 1
        lastIsFuseau = False
        firstEndDir = dir
    i = 0
    tmpLst = []
    sentNum = 0
    if mazeMode:
        for sent in lst:
            sent = sent[:-1] + ["."] + [sent[-1]]
            sentNum += 1
            tmpLst += sent
        lst = [tmpLst]
        history = [[-1, -1, -1, -1, False, -1, -1, -1, -1, -1, -1, -1], [False, []], [False, []], []]
        # [[stepAcc, dir, curDivDir, alter, lastIsFuseau, accent, layer, firstEndDir, dirPre, boxNum, c, divDirPre],
        #  [tried?, daughter], [tried?, daughter], mother] (a quasi-binary tree)
        daughter = history  # current layer of daughter in the history
        print(lst)
        fuseauNum = 0
        branchNum = 0
        for comp in lst[0]:
            if isinstance(comp[0], list):
                fuseauNum += 1
                for _ in comp:
                    branchNum += 1
                branchNum -= 1
        print(fuseauNum)
        print(branchNum)
        print(sentNum)
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
            print("compInd", compInd)
            print("firstEndDir", firstEndDir)
            if comp[0] == '.':
                nextPeriod = True
            elif isinstance(comp[0], list):  # identified as fuseau
                hasSame = 0
                legitCompLen = 0
                for branch in comp:
                    if isFuseau(branch[0]):
                        continue  # inner fuseau can't be the main stem and thus can't participate in the direction vote
                    else:
                        legitCompLen += 1
                    if exDir(branch[0][0]) == dir or exDir(branch[0][0]) == 2:
                        hasSame += 1  # continue in the same direction and measure based on this
                if hasSame < legitCompLen / 2:
                    dir = 1 - dir  # swap back
                innerLengths = {}
                innerWidths = {}
                lengths, comp = allocLength(comp, dir, depth=0)
                print("updated comp", comp)
                widths = allocWidth(comp, dir, lengths, depth=0)
                print("outer dicts", lengths, widths)
                print("inner dicts", innerLengths, innerWidths)
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
                    angle = traceAngle
                    tryChances = CHANCES
                    if dir != dirPre:
                        while tryChances > 0:
                            curDivDir = random.choice([0, 1])
                            shortestDist = -1  # distance from the starting point (originX, originY)
                            result = [-1, -1]
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
                                calibrate(dirPre, normalDir=divDirPre)
                                print("calibrated to", angle, dirPre, curDivDir)
                                t.forward(UNIT / 2 * (CHANCES - tryChances))  # try to space out
                                result[divDir] = drawFuseau(comp, lengths.copy(), widths.copy(), dir, divDir)
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
                            t.clear()
                            t.hideturtle()
                            if result[0] == -1 and result[1] == -1:
                                tryChances -= 1
                            else:
                                break

                        t = tmpT
                        angle = tmpAngle
                        firstEndDir = tmpFirstEndDir

                        calibrate(dirPre, normalDir=divDirPre)
                        if CHANCES - tryChances > 0:
                            t.color("red")
                            t.forward(UNIT / 2 * (CHANCES - tryChances))
                            t.color("black")

                        daughter[0] = [-1, dir, curDivDir, curAlter, lastIsFuseau,
                                       -1, -1, firstEndDir, dirPre, tmpBoxNum, -1, divDirPre]

                        for k in [0, 1]:
                            daughter[k + 1][0] = tried[k]
                        if result[0] == -1 and result[1] == -1:
                            retrace()
                            continue
                        else:
                            explore(comp, tmpBoxLst, lengths=lengths, widths=widths, isFuseau=True)
                    else:
                        result = -1
                        while tryChances >= 0:  # try chances = 0 means we just used the last chance
                            if result == -1:  # collided
                                if tryChances == 0:
                                    print("breaking")
                                    break  # you have lost all your chances, then get out!
                                t.clear()
                                t.hideturtle()
                                t.penup()
                                t.setpos(tmpFirstStartXor, tmpFirstStartYor)
                                firstEndDir = tmpFirstEndDir
                                t.showturtle()
                                t.pendown()
                                print("still trying", t.xcor())
                                calibrate(dirPre, normalDir=divDirPre)
                                t.forward(UNIT / 2 * (CHANCES - tryChances))  # try to space out
                                print("still trying", t.xcor())
                                result = drawFuseau(comp, lengths.copy(), widths.copy(), dir, curDivDir)
                                print("result", result)
                            else:
                                break
                            tryChances -= 1
                            print(tryChances, result)
                        print("finished", tryChances)
                        t.clear()
                        t.hideturtle()
                        t = tmpT
                        angle = tmpAngle
                        if result != -1:
                            firstEndDir = tmpFirstEndDir
                            calibrate(dirPre, normalDir=divDirPre)
                            if CHANCES - tryChances - 1 > 0:
                                t.color("red")
                                t.forward(UNIT / 2 * (CHANCES - tryChances - 1))
                                t.color("black")
                            tmpBoxLst = result[1]
                            tmpBoxNum = result[2]

                            daughter[0] = [-1, -1, curDivDir, curAlter,
                                           lastIsFuseau, -1, -1, firstEndDir, dirPre, tmpBoxNum, -1, divDirPre]

                            explore(comp, tmpBoxLst, lengths=lengths, widths=widths, isFuseau=True)
                        else:  # used up all the chances
                            daughter[0] = [-1, -1, curDivDir, curAlter,
                                           lastIsFuseau, -1, -1, firstEndDir, dirPre, tmpBoxNum, -1, divDirPre]
                            print("wow", tmpBoxNum)
                            daughter[curDivDir + 1][0] = True
                            retrace()
                            continue
                else:
                    drawFuseau(comp, lengths.copy(), widths.copy(), dir, curDivDir)
                #  if periodMode:
                #  hollowDot()
                lastIsFuseau = True  # for the next fuseau's reference
                print("firstEndDir", firstEndDir)
            else:
                print("data " + str(dir) + " " + str(firstEndDir) + " " + str(exDir(comp[0])))
                if lastIsFuseau and firstEndDir != dir and firstEndDir != 2 \
                        and exDir(comp[0]) != dir and exDir(comp[0]) != 2:
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
                    tryChances = CHANCES
                    if exDir(comp[0]) != dirPre and exDir(comp[0]) != 2:
                        while tryChances > 0:
                            curDivDir = random.choice([0, 1])
                            shortestDist = -1  # distance from the starting point (originX, originY)
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
                                calibrate(dirPre, normalDir=divDirPre)
                                print("calibrated to", angle, dirPre, curDivDir)
                                t.forward(UNIT / 2 * (CHANCES - tryChances))  # try to space out
                                movedPreXor = t.xcor()
                                movedPreYor = t.ycor()
                                drawElem(comp[0], normalDir=divDir, alter=curAlter, accent=comp[1], layer=comp[2])

                                bx = calcBox(comp, curAlter, mirror, movedPreXor, movedPreYor)
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
                                        if drawMode:
                                            drawRect(box[0], box[1], box[2], box[3], color="green")
                                        print(box[0], box[1], box[2], box[3], curAlter, mirror)
                                        print("---------\n", collided[divDir])
                                    if drawMode:
                                        for (c, x1o, y1o, x2o, y2o) in boxLst:
                                            print(c, x1o, y1o, x2o, y2o)
                                            drawRect(x1o, y1o, x2o, y2o, color="red")
                                    tried[divDir] = True  # mark as explored
                            print("curDivDir: " + str(curDivDir))
                            t.clear()
                            t.hideturtle()
                            if collided[0] and collided[1]:
                                tryChances -= 1
                            else:
                                break

                        t = tmpT
                        angle = tmpAngle

                        calibrate(dirPre, normalDir=divDirPre)
                        if CHANCES - tryChances > 0:
                            t.color("red")
                            t.forward(UNIT / 2 * (CHANCES - tryChances))
                            t.color("black")

                        daughter[0] = [-1, dir, curDivDir, curAlter, lastIsFuseau,
                                       comp[1], comp[2], firstEndDir, dirPre, len(bx[0]), comp[0], divDirPre]

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
                        collided = []
                        while tryChances >= 0:
                            if collided or tryChances == CHANCES:
                                if tryChances == 0:
                                    break
                                t.clear()
                                t.hideturtle()
                                t.penup()
                                t.setpos(preXor, preYor)
                                t.showturtle()
                                t.pendown()
                                calibrate(dirPre, normalDir=divDirPre)
                                t.forward(UNIT / 2 * (CHANCES - tryChances))  # try to space out
                                movedPreXor = t.xcor()
                                movedPreYor = t.ycor()
                                print('drawing', comp[0])
                                drawElem(comp[0], normalDir=curDivDir, alter=curAlter, accent=comp[1], layer=comp[2])
                                mirror = [1, -1][curDivDir]
                                bx = calcBox(comp, curAlter, mirror, movedPreXor, movedPreYor)
                                collided = []
                                for box in bx[0]:
                                    collided += checkCollision(box[0], box[1], box[2], box[3])
                                    if drawMode and collided:
                                        drawRect(box[0], box[1], box[2], box[3], color="green")
                                if drawMode and collided:
                                    for (c, x1o, y1o, x2o, y2o) in boxLst:
                                        print(c, x1o, y1o, x2o, y2o)
                                        drawRect(x1o, y1o, x2o, y2o, color="red")
                                print("still trying", collided, tryChances)
                            else:
                                break
                            tryChances -= 1
                        print("finished", tryChances)
                        t.clear()
                        t.hideturtle()
                        t = tmpT
                        angle = tmpAngle

                        daughter[0] = [-1, -1, curDivDir, curAlter, lastIsFuseau,
                                       comp[1], comp[2], firstEndDir, dirPre, len(bx[0]), comp[0], divDirPre]
                        # -1 records that this component is not a divergent node

                        if collided:
                            daughter[curDivDir + 1][0] = True
                            print("stoppy", exDir(comp[0]), dir)
                            retrace()
                            continue
                        else:
                            calibrate(dirPre, normalDir=divDirPre)
                            if CHANCES - tryChances - 1 > 0:
                                t.color("red")
                                t.forward(UNIT / 2 * (CHANCES - tryChances - 1))
                                t.color("black")
                            explore(comp, bx[0])
                else:
                    drawElem(comp[0], normalDir=curDivDir, alter=curAlter, accent=comp[1], layer=comp[2], isElem=True)
                #  if periodMode:
                #  hollowDot()

                curAlter *= -1
                lastIsFuseau = False
                print("dir before new element", dir, comp[0])
            dirPre = dir  # the direction of the element directly preceding the component (element/fuseau)
            divDirPre = curDivDir
            compInd += 1
        t.penup()
        if periodMode and not mazeMode:
            hollowDot()
        else:
            t.forward(UNIT)
        # t.setpos(t.xcor() - UNIT, - screen.window_height() / 2 + TURTLE_SIZE / 2 + MARGIN)
        t.pendown()
        i += 1


def main():
    readResult = ItiParser.read(txt)
    passageLst = readResult[0]
    #compNum = readResult[1]
    # passageLst = [[ItiParser.convert2Tree(guideTree)]]

    print('Passage List:', passageLst)
    #print('Component Number:', compNum)
    # t.screensize(WIDTH, HEIGHT)
    t.speed(0)
    screen.delay(0)
    if rapidMode:
        screen.tracer(0, 0)
    t.setundobuffer(50000)
    t.penup()
    t.goto(originX, originY)
    # t.goto(WIDTH / 2 - MARGIN, -HEIGHT / 2)
    t.pendown()
    t.left(180)
    t.showturtle()
    if mazeMode:
        trace.speed(1)
        trace.left(180)
        trace.hideturtle()
    draw(passageLst)
    if exportMode:
        t.save_as("./example2.svg")
        print("successfully generated the image")
    screen.mainloop()

if __name__ == "__main__":
    main()
