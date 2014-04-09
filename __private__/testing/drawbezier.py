def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n-1)
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier

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

##import Image,ImageTk
##import Tkinter as tk
##import ImageDraw
import sys
sys.path.append(r"C:\Users\BIGKIMO\Dropbox\Work\Research\Software\Various Python Libraries")
import PyDraw

if __name__ == '__main__':
##    im = Image.new('RGB', (100, 100), (0, 0, 0, 0)) 
##    draw = ImageDraw.Draw(im)
##    ts = [t/100.0 for t in range(101)]

    xys = [(0, 50), (40, 20), (60,20), (80, 50)]
    #bezier = make_bezier(xys)
    #points = bezier(ts)
    pyimg = PyDraw.Image().new(100,100)
    red=(222,0,0)
    yellow=(222,222,0)
    blue=(0,0,222)
    pyimg.drawline(66,50,88,88,fillcolor=red, fillsize=5)
    pyimg.drawmultiline(xys,fillcolor=red, fillsize=5)
    pyimg.drawpolygon(xys, fillcolor=yellow,outlinecolor=blue)
    pyimg.drawbezier(xys, fillcolor=red, outlinecolor=None, fillsize=5)
    pyimg.drawcircle(44,44,fillsize=7)
    #pyimg.save("C:/Users/BIGKIMO/Desktop/wahtevs.gif")
    pyimg.view()
    print ("woot")

##    xys = [(100, 50), (100, 0), (50, 0), (50, 35)]
##    bezier = make_bezier(xys)
##    points.extend(bezier(ts))

##    xys = [(50, 35), (50, 0), (0, 0), (0, 50)]
##    bezier = make_bezier(xys)
##    points.extend(bezier(ts))
##
##    xys = [(0, 50), (20, 80), (50, 100)]
##    bezier = make_bezier(xys)
##    points.extend(bezier(ts))

##    draw.polygon(points, fill = 'red')
##    win = tk.Tk()
##    tkimg = ImageTk.PhotoImage(im)
##    lbl=tk.Label(image=tkimg)
##    lbl.pack()
##    win.mainloop()
