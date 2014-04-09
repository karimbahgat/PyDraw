#IMPORTS
import sys
sys.path.append(r"C:\Users\BIGKIMO\Dropbox\Work\Research\Software\Various Python Libraries")
import PyDraw
import math



#USER INPUT
imgdims = (300,300)
linecoords = (50,50,250,250)
#linecoords = list(reversed(linecoords))
buff = 10.0

def drawbufferedline(imgdims,linecoords,buff,savename):
    #orig line
    img = PyDraw.Image().new(*imgdims)
    color = (200,0,0)
    img.drawline(*linecoords,col=color)
    #get orig params
    x1,y1,x2,y2 = linecoords
    xchange = x2-x1
    ychange = y2-y1
    origslope = ychange/float(xchange)
    angl = math.degrees(math.atan(origslope))
    color = (0,0,200)
    #leftline
    leftangl = angl-90
    leftybuff = buff * math.sin(math.radians(leftangl))
    leftxbuff = buff * math.cos(math.radians(leftangl))
    leftx1,leftx2 = (x1-leftxbuff,x2-leftxbuff)
    lefty1,lefty2 = (y1-leftybuff,y2-leftybuff)
    leftlinecoords = (leftx1,lefty1,leftx2,lefty2)
    img.drawline(*leftlinecoords,col=color)
    #rightline
    rightangl = angl-90
    rightybuff = buff * math.sin(math.radians(rightangl))
    rightxbuff = buff * math.cos(math.radians(rightangl))
    rightx1,rightx2 = (x1+rightxbuff,x2+rightxbuff)
    righty1,righty2 = (y1+rightybuff,y2+rightybuff)
    rightlinecoords = (rightx1,righty1,rightx2,righty2)
    img.drawline(*rightlinecoords,col=color)
    #view
    img.view()

drawbufferedline(imgdims,linecoords,buff,"")


##allvars = dir()
##for var in allvars:
##    if not var.startswith("__"):
##        val = eval(var)
##        print ("%s = %s"%(var,val))

