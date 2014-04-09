#IMPORTS
import sys
sys.path.append(r"C:\Users\BIGKIMO\Dropbox\Work\Research\Software\Various Python Libraries")
import PyDraw
import math

#USER INPUT
sphereradius = 200

#run
img = PyDraw.Image().load("spheretexture.gif")
print ("done loading",img.width,img.height)
img = img.spheremapping(sphereradius)#,xoffset=100,yoffset=0)#,zdist=500)
print ("done mapping",img.width,img.height)
img.save("mappedsphere.gif")

