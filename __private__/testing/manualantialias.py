import PIL, PIL.Image, PIL.ImageDraw, math, time, random

def plot(draw, img, x, y, c, col,steep):
    if steep:
        x,y = y,x
##    if x < img.size[0] and y < img.size[1] and x >= 0 and y >= 0:
        #DROPPED BC POINTLESS TO USE 4 OPS FOR CHECKING IF OUTOFBOUNDS...
        #print "pre",c
        #print "mid",col[3]/255.0
        #c = c * (float(col[3])/255.0)
        #print "post",c
        #p = img.getpixel((x,y))
        #newtransp = int((sum([col[3],p[3]])/2.0)*c)
    #not entirely satisfied with quality yet, does some weird stuff when overlapping
    newtransp = c*255 #int(col[3]*c)
    newcolor = (col[0], col[1], col[2],newtransp)
    #newcolor = (int((p[0]*(1-c)) + col[0]*c), int((p[1]*(1-c)) + col[1]*c), int((p[2]*(1-c)) + col[2]*c),255)
    draw.point((x,y),fill=newcolor)

def iround(x):
    return ipart(x + 0.5)

def ipart(x):
    return math.floor(x)

def fpart(x):
    return x-math.floor(x)

def rfpart(x):
    return 1 - fpart(x)


def drawLine(draw, img, x1, y1, x2, y2, col):
    dx = x2 - x1
    dy = y2 - y1

    steep = abs(dx) < abs(dy)
    if steep:
        x1,y1=y1,x1
        x2,y2=y2,x2
        dx,dy=dy,dx
    if x2 < x1:
        x1,x2=x2,x1
        y1,y2=y2,y1
    gradient = float(dy) / float(dx)

    #handle first endpoint
    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = rfpart(x1 + 0.5)
    xpxl1 = xend    #this will be used in the main loop
    ypxl1 = ipart(yend)
    plot(draw, img, xpxl1, ypxl1, rfpart(yend)*xgap, col, steep)
    plot(draw, img, xpxl1, ypxl1 + 1, fpart(yend)*xgap, col, steep)
    intery = yend + gradient # first y-intersection for the main loop

    #handle second endpoint
    xend = round(x2)
    yend = y2 + gradient * (xend - x2)
    xgap = fpart(x2 + 0.5)
    xpxl2 = xend    # this will be used in the main loop
    ypxl2 = ipart(yend)
    plot(draw, img, xpxl2, ypxl2, rfpart(yend)*xgap, col, steep)
    plot(draw, img, xpxl2, ypxl2 + 1, fpart(yend)*xgap, col, steep)

    #main loop
    for x in xrange(int(xpxl1 + 1), int(xpxl2 )):
        ybase = int(intery)
        ydeci = intery-int(intery)
        plot(draw, img, x, ybase, 1-ydeci, col, steep)
        plot(draw, img, x, ybase+1, ydeci, col, steep)
        intery = intery + gradient

#params
WIDTH, HEIGHT = (500,500)
nrlines = 500
col = (150,0,0,250)

#purepy
img = PIL.Image.new("RGBA",(WIDTH,HEIGHT))
draw = PIL.ImageDraw.ImageDraw(img)
randrange = random.randrange
t = time.clock()
for _ in xrange(nrlines):
    x1, y1, x2, y2 = (randrange(WIDTH),randrange(HEIGHT),randrange(WIDTH),randrange(HEIGHT))
    drawLine(draw, img, x1, y1, x2, y2, col)
print "purepy",time.clock()-t
img.save("C:/Users/BIGKIMO/Desktop/purepy_antialias.png")

#pro comparison
import aggdraw
img = PIL.Image.new("RGBA",(WIDTH,HEIGHT))
draw = aggdraw.Draw(img)
pen = aggdraw.Pen(col,0.5)
randrange = random.randrange
t = time.clock()
for _ in xrange(nrlines):
    x1, y1, x2, y2 = (randrange(WIDTH),randrange(HEIGHT),randrange(WIDTH),randrange(HEIGHT))
    draw.line((x1, y1, x2, y2), pen)
draw.flush()
print "aggdraw",time.clock()-t
img.save("C:/Users/BIGKIMO/Desktop/pro_antialias.png")

#not antialias comparison
img = PIL.Image.new("RGBA",(WIDTH,HEIGHT))
draw = PIL.ImageDraw.ImageDraw(img)
randrange = random.randrange
t = time.clock()
for _ in xrange(nrlines):
    x1, y1, x2, y2 = (randrange(WIDTH),randrange(HEIGHT),randrange(WIDTH),randrange(HEIGHT))
    draw.line((x1, y1, x2, y2), fill=col)
print "PIL (no antialias)",time.clock()-t
img.save("C:/Users/BIGKIMO/Desktop/not_antialias.png")
