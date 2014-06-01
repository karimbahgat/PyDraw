# Pydraw submodule
# Coordinate system handler for pixel conversion

REDUCEVECTORS = False

class CoordinateSystem(object):
    def __init__(self, bbox, img):
        """
        A helper class that the user can use to define a coordinate system
        and convert coordinates to pixel space

        - bbox: the bounding box of the coordinate system as a four-tuple (xmin,ymin,xmax,ymax).
        - img: the image instance whose dimensions the coordinate system should use when converting to pixels.
        """
        bbox = [float(each) for each in bbox]
        self.XMIN,self.YMIN,self.XMAX,self.YMAX = bbox
        x2x = (self.XMIN,self.XMAX)
        y2y = (self.YMIN,self.YMAX)
        nw = (-1*min(x2x),max(y2y)) #northwest corner of zoomextent
        self.XWIDTH = x2x[1]-x2x[0]
        self.YHEIGHT = y2y[1]-y2y[0]
        self.XOFFSET = nw[0]
        self.YOFFSET = nw[1]
        self.IMGWIDTH = float(img.width)
        self.IMGHEIGHT = float(img.height)
    def coords2pixels(self, incoords):
        """
        Converts a single list of coordinate pairs to pixel coordinate pairs
        according to the coordinate system and pixel image defined in the class
        """
        outcoords = []
        previous = None
        for point in incoords:
            inx, iny = point
            newx = (self.XOFFSET+inx)/self.XWIDTH*self.IMGWIDTH
            newy = self.IMGHEIGHT-(self.YOFFSET+iny)/self.YHEIGHT*self.IMGHEIGHT
            if REDUCEVECTORS:
                newpoint = (int(newx),int(newy))
                if newpoint != previous:
                    outcoords.extend(newpoint)
                    previous = newpoint
            else:
                newpoint = [newx,newy]
                outcoords.append(newpoint)
        return outcoords
