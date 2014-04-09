import Tkinter as tk
import math,operator,itertools

class Image(object):

    #STARTING
    def new(self,width,height,background=None):
        self.width = width
        self.height = height
        if not background:
            background = (200,200,200)
        horizline = [background for _ in xrange(width)]
        self.imagegrid = [list(horizline) for _ in xrange(height)]
        return self
    def load(self, filepath=None, data=None):
        if data:
            self.width = len(data[0])
            self.height = len(data)
            self.imagegrid = data
        elif filepath:
            tempwin = tk.Tk()
            tempimg = tk.PhotoImage(file=filepath)
            data = [[tuple([int(spec) for spec in tempimg.get(x,y).split()])
                    for x in xrange(tempimg.width())]
                    for y in xrange(tempimg.height())]
            self.width = len(data[0])
            self.height = len(data)
            self.imagegrid = data
        return self

    #TRANSFORM
    def rotate(self):
        self.imagegrid = [list(each) for each in zip(*listoflists)]
        #and update width/height
    def spheremapping(self, sphereradius, xoffset=0, yoffset=0, zdist=0):
        """
        still work in progress
        ...
        map image onto a 3d globe-like sphere
        return a new transformed image instance
        what happens is that the entire output image is like a window looking out on a globe from a given dist and angle, and the original image is like a sheet of paper filling the window and then gets sucked and wrapped from its position directly onto the globe, actually the origpic does not necessarily originate from the window/camera pos
        need to figure out viewopening and viewdirection
        based on http://stackoverflow.com/questions/9604132/how-to-project-a-point-on-to-a-sphere
        altern, use point = centervect + radius*(point-centervect)/(norm(point-centervect))
        """
        #sphereboxwidth,sphereboxheight,sphereboxdepth = (sphereradius*2,sphereradius*2,sphereradius*2)
        midx,midy,midz = (sphereradius+xoffset,sphereradius+yoffset,sphereradius+zdist)
        def pixel2sphere(x,y,z):
            newx,newy,newz = (x-midx,y-midy,z-midz)
            newlen = math.sqrt(newx*newx+newy*newy+newz*newz)
            try:
                scaledx,scaledy,scaledz = [(sphereradius/newlen)*each for each in (newx,newy,newz)]
                newpoint = (scaledx+midx,scaledy+midy,scaledz+midz)
                return newpoint
            except ZeroDivisionError:
                pass
        #below needs to be a function to be called per image pixel, not for every 3d position
        newimg = Image().new(self.width,self.height)
        for y in xrange(len(self.imagegrid)):
            for x in xrange(len(self.imagegrid[0])):
                color = self.get(x,y)
                newpos = pixel2sphere(x,y,z=0)
                if newpos:
                    newx,newy,newz = newpos
                    newimg.put(int(newx),int(newy),color)
        return newimg
    def tilt(self, oldplane, newplane):
        """
        perspective transform.
        oldplane is a list of four old xy coordinate pairs
        that will move to the four points in the newplane
        maybe some hints here: http://www.cs.utexas.edu/~fussell/courses/cs384g/lectures/lecture20-Z_buffer_pipeline.pdf
        """
        #first find the transform coefficients, thanks to http://stackoverflow.com/questions/14177744/how-does-perspective-transformation-work-in-pil
        pb,pa = oldplane,newplane
        grid = []
        for p1,p2 in zip(pa, pb):
            grid.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
            grid.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])
        def transpose(listoflists):
            return [list(each) for each in zip(*listoflists)]
        def flatten(listoflists):
            return [xory for xy in listoflists for xory in xy]
        def sumproduct(listA,multis):
            "aka, dot multiplication"
            outgrid = []
            for y,(row,multi) in enumerate(zip(listA,multis)):
                rowsum = 0
                for x,nr in enumerate(row):
                    rowsum += nr*multi
                outgrid.append(rowsum)
            return outgrid
        def gridmultiply(grid1,grid2):
            "aka, matrix*matrix"
            outgrid = []
            for y in xrange(len(grid1)):
                newrow = []
                for x in xrange(len(grid2)):
                    value = grid1[y][x] * grid2[y][x]
                    newrow.append(value)
                outgrid.append(newrow)
            return outgrid
        def gridinverse(grid):
            outgrid = []
            pos_deriv = 1
            neg_deriv = 1
            for y in xrange(len(grid)):
                horizline = []
                for x in xrange(len(grid[0])):
                    invx=len(grid[0])-1-x
                    invy=len(grid)-1-y
                    nr = grid[y][x]
                    pos_deriv += pos_deriv*nr
                    invnr = grid[invy][invx]*-1
                    horizline.append(invnr)
                    neg_deriv += neg_deriv*invnr
                outgrid.append(horizline)
            derivative = 1/float(pos_deriv-neg_deriv)
            print "deriv",derivative
            outgrid = gridmultiply(outgrid,[[derivative for _ in xrange(len(outgrid[0]))] for _ in xrange(len(outgrid))])
            return outgrid
        
        import numpy
##        matrix = []
##        print pa,pb
##        for p1, p2 in zip(pa, pb):
##            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
##            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

        print grid
        A = numpy.matrix(grid, dtype=numpy.float)
        print "a",A
        B = numpy.array(pb).reshape(8)
        AT = A.T
        print "at",AT
        ATA = AT * A
        print "ata",ATA
        inv = numpy.linalg.inv(ATA)
        invAT = inv * AT
        print "invAT",invAT
        res = numpy.dot(invAT, B)
        print "res",res
        transcoeff = numpy.array(res).reshape(8)

        import PyDraw.advmatrix as mt
        print grid
        A = mt.Matrix(grid)
        print "a",A
        B = mt.Vec(flatten(pb))
        AT = A.tr()
        print "at",AT
        ATA = AT.mmul(A)
        print "ata",ATA
        gridinv = ATA.inverse()
        invAT = gridinv.mmul(AT)
        print "invAT",invAT
        res = invAT.mmul(B)
        print "res",res
        transcoeff = res.flatten()

##        A = grid
##        B = flatten(pb)
##        res = sumproduct(gridinverse(gridmultiply(gridmultiply(transpose(A),A),transpose(A))), B)
##        transcoeff = res

        print "ab",A,B
        print "res",numpy.array(res).reshape(8)
        print transcoeff
        #then calculate new coords, thanks to http://math.stackexchange.com/questions/413860/is-perspective-transform-affine-if-it-is-why-its-impossible-to-perspective-a"
        k = 1
        a,b,c,d,e,f,g,h = transcoeff
        outimg = Image().new(self.width,self.height)
        for y in xrange(len(self.imagegrid)):
            for x in xrange(len(self.imagegrid[0])):
                color = self.get(x,y)
                newx = int(round((a*x+b*y+c)/float(g*x+h*y+k)))
                newy = int(round((d*x+e*y+f)/float(g*x+h*y+k)))
                try:
                    outimg.put(newx,newy,color)
                    #print x,y,newx,newy
                except IndexError:
                    #out of bounds
                    pass
        return outimg

    #DRAWING
    def get(self,x,y):
        rgb = self.imagegrid[y][x]
        return rgb
    def put(self,x,y,color):
        self.imagegrid[y][x] = color
    def floodfill(self,x,y,fillcolor,fuzzythresh=1.0):
        """
        adapted from http://inventwithpython.com/blog/2011/08/11/recursion-explained-with-the-flood-fill-algorithm-and-zombies-and-cats/comment-page-1/
        however, probably should be optimized, bc now checks all neighbours multiple times regardless of whether checked before bc has no memory
        """
        #test and fill all neighbouring cells
        fillcolor = list(fillcolor)
        colortofollow = self.get(x,y)
        sqrt = math.sqrt
        def notexactcolor(x,y):
            if self.get(x,y) != colortofollow:
                return True
        def notfuzzycolor(x,y):
            """based on W3 principles, http://www.had2know.com/technology/color-contrast-calculator-web-design.html
            but doesnt really work yet, super slow, likely due to the if bigger than test operation"""
##            r,g,b = self.get(x,y)
##            checkbrightness = ( 299*r + 587*g + 114*b )/1000
##            r,g,b = colortofollow
##            comparebrightness = ( 299*r + 587*g + 114*b )/1000
##            brightnessdiff = float(str((checkbrightness-comparebrightness)/255.0).replace("-",""))#sqrt(((checkbrightness-comparebrightness)/255.0)**2)
            main = self.get(x,y)
            compare = colortofollow
            colordiff = sum([spec[0]-spec[1] for spec in zip(main,compare)])/255.0
            if colordiff > fuzzythresh:
                return True
        if fuzzythresh == 1.0: reachedboundary = notexactcolor
        else: reachedboundary = notfuzzycolor
        theStack = [ (x, y) ]
        while len(theStack) > 0:
            x, y = theStack.pop()
            try:
                if reachedboundary(x,y):
                    continue
            except IndexError:
                continue
            self.put(x,y,fillcolor)
            theStack.append( (x + 1, y) )  # right
            theStack.append( (x - 1, y) )  # left
            theStack.append( (x, y + 1) )  # down
            theStack.append( (x, y - 1) )  # up
    def drawline(self, x1, y1, x2, y2, col):
        def plot(x, y, c, col,steep):
            if steep:
                x,y = y,x
            #not entirely satisfied with quality yet, does some weird stuff when overlapping
            p = self.get(int(x),int(y))
            newtransp = c*255 #int(col[3]*c)
            #newcolor = (col[0], col[1], col[2],newtransp)
            newcolor = (int((p[0]*(1-c)) + col[0]*c), int((p[1]*(1-c)) + col[1]*c), int((p[2]*(1-c)) + col[2]*c))
            self.put(int(x),int(y),newcolor)

        def iround(x):
            return ipart(x + 0.5)

        def ipart(x):
            return math.floor(x)

        def fpart(x):
            return x-math.floor(x)

        def rfpart(x):
            return 1 - fpart(x)
        
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
        plot(xpxl1, ypxl1, rfpart(yend)*xgap, col, steep)
        plot(xpxl1, ypxl1 + 1, fpart(yend)*xgap, col, steep)
        intery = yend + gradient # first y-intersection for the main loop

        #handle second endpoint
        xend = round(x2)
        yend = y2 + gradient * (xend - x2)
        xgap = fpart(x2 + 0.5)
        xpxl2 = xend    # this will be used in the main loop
        ypxl2 = ipart(yend)
        plot(xpxl2, ypxl2, rfpart(yend)*xgap, col, steep)
        plot(xpxl2, ypxl2 + 1, fpart(yend)*xgap, col, steep)

        #main loop
        for x in xrange(int(xpxl1 + 1), int(xpxl2 )):
            ybase = int(intery)
            ydeci = intery-int(intery)
            plot(x, ybase, 1-ydeci, col, steep)
            plot(x, ybase+1, ydeci, col, steep)
            intery = intery + gradient
            
    def drawpolygon(self, coords, fillcolor, outlinecolor=(255,255,255)):
        #first draw lines
        if coords[-1] != coords[0]:
            coords.append(coords[0])
        for index in xrange(len(coords)-1):
            start,end = coords[index],coords[index+1]
            linecoords = list(start)
            linecoords.extend(list(end))
            self.drawline(*linecoords, col=outlinecolor)
        #then find one inside point
        #...
        insidepoint = (coords[0][0]+1,coords[0][1]+1)
        #then floodfill (but should be in a virtual clean space)
        self.floodfill(*insidepoint, fillcolor=fillcolor, fuzzythresh=1.0)

    def drawcircle(self):
        #use bezier circle path
        c = 0.55191502449*size #0.55191502449 http://spencermortensen.com/articles/bezier-circle/ #alternative nr: 0.551784 http://www.tinaja.com/glib/ellipse4.pdf
        controlpoints = [0,size,c,size,size,c,
                 size,0,size,-c,c,-size,
                 0,-size,-c,-size,-size,-c,
                 -size,0,-size,c,-c,size,0,size]
        pathstring = "M"+",".join([str(each) for each in controlpoints[:2]])
        controlpoints = controlpoints[2:] #forget about first two cus already used
        index = 0
        while index in xrange(len(controlpoints)):
            i1,i2,i3,i4,i5,i6 = controlpoints[index:index+6]
            pathstring += " C"+",".join([str(each) for each in (i1,i2,i3,i4,i5,i6)])
            index += 6
        #then plot...
        #...

    #AFTERMATH
    def view(self):
        window = tk.Tk()
        canvas = tk.Canvas(window, width=self.width, height=self.height)
        canvas.create_text((self.width/2, self.height/2), text="error\nviewing\nimage")
        tkimg = self._tkimage()
        canvas.create_image((self.width/2, self.height/2), image=tkimg, state="normal")
        canvas.pack()
        tk.mainloop()
    def save(self, savepath):
        tempwin = tk.Tk() #only so dont get "too early to create image" error
        tkimg = self._tkimage()
        tkimg.write(savepath, "gif")
        tempwin.destroy()
        
    #INTERNAL USE ONLY
    def _tkimage(self):
        tkimg = tk.PhotoImage(width=self.width, height=self.height)
        imgstring = " ".join(["{"+" ".join(["#%02x%02x%02x" %tuple(rgb) for rgb in horizline])+"}" for horizline in self.imagegrid])
        tkimg.put(imgstring)
        return tkimg


