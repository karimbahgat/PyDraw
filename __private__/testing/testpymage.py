import sys,random
import pymaging, pymaging.shapes, pymaging.tests, pymaging.tests.test_affine, pymaging_png
sys.path.append(r"C:\Users\BIGKIMO\Dropbox\Work\Research\Software\Various Python Libraries")
import PyDraw

#draw and transform with pymaging
img = pymaging.image.Image.new(pymaging.colors.RGB, 100,100, pymaging.colors.Color(222,22,222))
"img = img.rotate(45,resize_canvas=False)"
def drawpolygon(img, coords, outlinecolor):
    "polygon based on pymaging lines"
    if coords[-1] != coords[0]:
        coords.append(coords[0])
    for index in xrange(len(coords)-1):
        start,end = coords[index],coords[index+1]
        linecoords = list(start)
        linecoords.extend(list(end))
        line = pymaging.shapes.Line(*linecoords)
        img.draw(line, outlinecolor)
polycoords = [(5,4),(64,22),(73,77),(2,55)]
drawpolygon(img, polycoords, pymaging.colors.Color(0,222,0))
img = img.affine(transform=pymaging.affine.AffineTransform(), resample_algorithm=pymaging.resample.nearest)

#then use my own tkrenderer
data = [[img._pixelarray.get(x,y) for x in xrange(img.width)] for y in xrange(img.height)]
tkimg = PyDraw.Image().load(data=data)
#tkimg.drawline(5,4,64,22, (177,11,133))
tkimg.drawpolygon(polycoords, fillcolor=(9,11,233))
tkimg.floodfill(1,1,(22,222,9))

#tkimg.view()
tkimg.save("normal.gif")

#numpytest and PIL test
##import numpy,PIL,PIL.Image
##matrix = []
##img = PIL.Image.open("3dscene.png")
##width,height = 500,500
##oldplane = [(0,0),(width,0),(width,height),(0,height)]
##newplane = [(0,0),(width,0),(width/2.0,height),(0,height/2.0)]
##pb,pa = oldplane,newplane
##for p1, p2 in zip(pa, pb):
##    matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
##    matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])
##A = numpy.matrix(matrix, dtype=numpy.float)
##B = numpy.array(pb).reshape(8)
##print "ab",A,B
##res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
##print "res",numpy.array(res).reshape(8)
##transcoeff = numpy.array(res).reshape(8)
##img = img.transform((width, height), PIL.Image.PERSPECTIVE, transcoeff, PIL.Image.BICUBIC)
##img.save("pilnumpy.png")

#then try perspective
#transcoeff = [82,75,55,32,13,83,4,2,1]
oldplane = [(0,0),(tkimg.width,0),(tkimg.width,tkimg.height),(0,tkimg.height)]
newplane = [(0,0),(tkimg.width,0),(tkimg.width/2.0,tkimg.height),(0,tkimg.height/2.0)]
tilted = tkimg.tilt(oldplane,newplane)
tilted.view()
tilted.save("tilted.gif")


