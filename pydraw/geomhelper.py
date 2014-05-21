#GEOMETRY HELPER CLASSES
import math

class _Line:
    def __init__(self, x1,y1,x2,y2):
        self.x1,self.y1,self.x2,self.y2 = x1,y1,x2,y2
        self.xdiff = x2-x1
        self.ydiff = y2-y1
        try:
            self.slope = self.ydiff/float(self.xdiff)
            self.zero_y = self.slope*(0-x1)+y1
        except ZeroDivisionError:
            self.slope = None
            self.zero_y = None
    def __str__(self):
        return str(self.tolist())
    def tolist(self):
        return ((self.x1,self.y1),(self.x2,self.y2))
    def intersect(self, otherline, infinite=False):
        """
        Input must be another line instance
        Finds real or imaginary intersect assuming lines go forever, regardless of real intersect
        Infinite is based on http://stackoverflow.com/questions/20677795/find-the-point-of-intersecting-lines
        Real is based on http://stackoverflow.com/questions/18234049/determine-if-two-lines-intersect
        """
        if infinite:
            D  = -self.ydiff * otherline.xdiff - self.xdiff * -otherline.ydiff
            Dx = self._selfprod() * otherline.xdiff - self.xdiff * otherline._selfprod()
            Dy = -self.ydiff * otherline._selfprod() - self._selfprod() * -otherline.ydiff
            if D != 0:
                x = Dx / D
                y = Dy / D
                return x,y
            else:
                return False
        else:
            # MANUAL APPROACH
            # http://stackoverflow.com/questions/18234049/determine-if-two-lines-intersect
            if self.slope == None:
                if otherline.slope == None:
                    return False
                ix = self.x1
                iy = ix*otherline.slope+otherline.zero_y
            elif otherline.slope == None:
                ix = otherline.x1
                iy = ix*self.slope+self.zero_y
            else:
                try:
                    ix = (otherline.zero_y-self.zero_y) / (self.slope-otherline.slope)
                except ZeroDivisionError:
                    #slopes are exactly the same so never intersect
                    return False
                iy = ix*self.slope+self.zero_y

            #check that intsec happens within bbox of both lines
            if ix >= min(self.x1,self.x2) and ix >= min(otherline.x1,otherline.x2)\
            and ix <= max(self.x1,self.x2) and ix <= max(otherline.x1,otherline.x2)\
            and iy >= min(self.y1,self.y2) and iy >= min(otherline.y1,otherline.y2)\
            and iy <= max(self.y1,self.y2) and iy <= max(otherline.y1,otherline.y2):
                return ix,iy
            else:
                return False
    def getlength(self):
        return math.hypot(self.xdiff,self.ydiff)
    def getangle(self):
        try:
            angle = math.degrees(math.atan(self.ydiff/float(self.xdiff)))
            if self.xdiff < 0:
                angle = 180 - angle
            else:
                angle *= -1
        except ZeroDivisionError:
            if self.ydiff < 0:
                angle = 90
            elif self.ydiff > 0:
                angle = -90
            else:
                raise TypeError("error: the vector isnt moving anywhere, so has no angle")
        return angle
    def getbuffersides(self, linebuffer):
        x1,y1,x2,y2 = self.x1,self.y1,self.x2,self.y2
        midline = _Line(x1,y1,x2,y2)
        angl = midline.getangle()
        perpangl_rad = math.radians(angl-90) #perpendicular angle in radians
        xbuff = linebuffer * math.cos(perpangl_rad)
        ybuff = linebuffer * math.sin(perpangl_rad)
        #xs
        leftx1 = (x1-xbuff)
        leftx2 = (x2-xbuff)
        rightx1 = (x1+xbuff)
        rightx2 = (x2+xbuff)
        #ys
        lefty1 = (y1+ybuff)
        lefty2 = (y2+ybuff)
        righty1 = (y1-ybuff)
        righty2 = (y2-ybuff)
        #return lines
        leftline = _Line(leftx1,lefty1,leftx2,lefty2)
        rightline = _Line(rightx1,righty1,rightx2,righty2)
        return leftline,rightline
    def anglebetween_rel(self, otherline):
        angl1 = self.getangle()
        angl2 = otherline.getangle()
        bwangl_rel = angl1-angl2 # - is left turn, + is right turn
        return bwangl_rel
    def anglebetween_abs(self, otherline):
        bwangl_rel = self.anglebetween_rel(otherline)
        angl1 = self.getangle()
        bwangl = angl1+bwangl_rel
        return bwangl
    def anglebetween_inv(self, otherline):
        bwangl = self.anglebetween_abs(otherline)
        if bwangl < 0:
            normangl = (180 + bwangl)/-2.0
        else:
            normangl = (180 - bwangl)/-2.0
        normangl = (180 + bwangl)/-2.0
        return normangl
    
    #INTERNAL USE ONLY
    def _selfprod(self):
        """
        Used by the line intersect method
        """
        return -(self.x1*self.y2 - self.x2*self.y1)
    
class _Bezier:
    def __init__(self, xypoints, intervals=100):
        # xys should be a sequence of 2-tuples (Bezier control points)
        def pascal_row(n):
            # This returns the nth row of Pascal's Triangle
            result = [1]
            x, numerator = 1, n
            for denominator in range(1, n//2+1):
                # print(numerator,denominator,x)
                x *= numerator
                x /= denominator
                result.append(x)
                numerator -= 1
            if n&1 == 0:
                # n is even
                result.extend(reversed(result[:-1]))
            else:
                result.extend(reversed(result)) 
            return result
        n = len(xypoints)
        combinations = pascal_row(n-1)
        ts = (t/float(intervals) for t in xrange(intervals+1))
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xypoints)))
        self.coords = result
