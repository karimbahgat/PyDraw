from Tkinter import Tk, Canvas, PhotoImage, mainloop
from math import sin
import random
import time

WIDTH, HEIGHT = 1200, 600

window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#005500")
canvas.pack()
img = PhotoImage(width=WIDTH, height=HEIGHT)
canvasimg = canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")
#window.update()

#params
nrpixels = 100000
randrange = random.randrange

t = time.clock()
#sine example
##for ypos in [-30,-10,10,30]:
##    print ypos
##    for x in xrange(4 * WIDTH):
##        y = int(ypos+HEIGHT/2 + HEIGHT/4 * sin(x/80.0))
##        img.put("#ffffff", (x//4,y))

#random example
##t = time.clock()
##for _ in xrange(nrpixels):
##    xy = (randrange(WIDTH),randrange(HEIGHT))
##    img.put("#ffffff", (xy))
##print "done",time.clock()-t,"seconds"

#random start, then random steps
##xy = [randrange(WIDTH),randrange(HEIGHT)]
##print xy
##for _ in xrange(nrpixels):
##    #rgb = tuple([random.choice([50,100,200,250]) for _ in xrange(3)])
##    rgb = (200,0,0)
##    img.put("#%02x%02x%02x" % rgb, xy)
##    #print xy
##    x = xy[0]+randrange(-1,2)
##    if x < 0:
##        x = 0
##    xy[0] = x
##    y = xy[1]+randrange(-1,2)
##    if y < 0:
##        y = 0
##    xy[1] = y
##print "done"
##img.write("C:/Users/BIGKIMO/Desktop/hhmm.gif", "gif")
###zoomimg = img.zoom(3,3)
###zoomimg.write("C:/Users/BIGKIMO/Desktop/hhmm_zoom.gif", "gif")

#multiple pixels at once exampe
"""
AWESOME HOW TO MAKE FASTER BY PUTTING MULTIPLE PIXELS AT ONCE
http://tkinter.unpythonic.net/wiki/PhotoImage#Fill_Many_Pixels_at_Once
"""
xy = [int(WIDTH/2.0),int(HEIGHT/2.0)] #[randrange(WIDTH),randrange(HEIGHT)]
print xy
horizline = ["#000000" for _ in xrange(WIDTH)] #the 100 at end means transparent
imggrid = [list(horizline) for _ in xrange(HEIGHT)]
print len(imggrid),len(imggrid[0])
t = time.clock()
for _ in xrange(nrpixels):
    #rgb = tuple([random.choice([50,100,200,250]) for _ in xrange(3)])
    rgb = (200,0,0)
    imggrid[xy[1]][xy[0]] = "#%02x%02x%02x" % rgb
    #print xy
    x = xy[0]+randrange(-1,2)
    if x < 0:
        x = 0
    xy[0] = x
    y = xy[1]+randrange(-1,2)
    if y < 0:
        y = 0
    xy[1] = y
imgstring = " ".join(["{"+" ".join(horizline)+"}" for horizline in imggrid])
img.put(imgstring)
img.write("C:/Users/BIGKIMO/Desktop/hhmm_multipixels.gif", "gif")
###zoomimg = img.zoom(3,3)
###zoomimg.write("C:/Users/BIGKIMO/Desktop/hhmm_zoom.gif", "gif")

#PIL comparison
##import PIL,PIL.Image,PIL.ImageDraw,PIL.ImageTk
##img = PIL.Image.new("RGB",(WIDTH,HEIGHT))
##drawer = PIL.ImageDraw.ImageDraw(img)
##xy = [randrange(WIDTH),randrange(HEIGHT)]
##for _ in xrange(nrpixels):
##    rgb = (200,0,0)
##    drawer.point(xy, fill="#%02x%02x%02x" % rgb)
##    x = xy[0]+randrange(-1,2)
##    if x < 0:
##        x = 0
##    xy[0] = x
##    y = xy[1]+randrange(-1,2)
##    if y < 0:
##        y = 0
##    xy[1] = y
##tkimg = PIL.ImageTk.PhotoImage(img)
##canvas.itemconfig(canvasimg, image=tkimg)
##img.save("C:/Users/BIGKIMO/Desktop/hhmm_PIL.gif")
        
print "done",time.clock()-t,"seconds"

mainloop()
