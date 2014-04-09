# Documentation for PyDraw
v0.1

## Introduction
PyDraw is a pure-Python drawing library.
The reason for making this library was to experiment with new drawing features to
merge with the pure-Python "Pymaging" library. But since Pymaging still hasn't 
been released in a working-version aimed for end-users, I'm just releasing this as a separate 
package until it can hopefully be incorporated into the Pymaging library later on.
PyDraw might also be interesting in itself since it incredibly lightweight,
straightforward to use, and provides not only basic drawing but also some
advanced features. One of the joys of it being pure-Python is that it becomes
fairly easy and way more accessible for even novice Python programmers to
experiment with and extend its drawing functionality and routines. 
Main features include:

- uses similar drawing commands to those used in PIL and Aggdraw
- the user can draw on a new empty image, open an existing one, and save the image to file
- draws various graphical primitives:
  - lines
  - circles
  - multilines
  - polygons
  - bezier curves
- drawings uses antialising (smooth sub-pixel precision)
- offers exact and fuzzy floodfill coloring of large areas (however, fuzzy floodfill is currently way too slow to be used)
- can also transform images
  - perspective transform, ie 3d tilting of an image
  - sphere/stereographic transform, ie 3d globe effect (partially working, partially not)

The main backdraws currently are:

- only support for reading/writing gif images, and if you use to many colors the gif image won't save
- while transparent gif images can be read, transparency will not be saved (becomes black)
- not as fast as C-based libraries (on average 10x slower)
- not a stable version yet, so several lacking features and errors (see Status below)

## Basic Usage
A typical example of how to use it would be:

```
import pydraw
img = pydraw.Image().new(width=500,height=500)
img.drawbezier([(22,22),(88,88),(188,22),(333,88)], fillcolor=(222,0,0))
img.drawcircle(333,111,fillsize=55,outlinecolor=(222,222,0))
img.drawline(0,250,499,250, fillcolor=(222,222,222))
img.floodfill(444,444,fillcolor=(0,222,0))
img.floodfill(222,222,fillcolor=(0,0,222))
img.view()
```

## Requires:
No dependencies; everything is written with the standard builtin Python library.
This is mainly thanks to the basic read-write capabilities of the Tkinter PhotoImage class.
Also tested to work on both Python 2.x and 3.x. 

## Status:
Main features are working okay so should be able to be used by end-users.
However, still in its most basic alpha-version, which means there may be many bugs. 
But most importantly it is lacking a few crucial drawing features,
which will be added in the future, such as:

- None of the primitives are being filled correctly (so drawing is limited to outlines)
- Thick multilines and thick polygon outlines appear choppy, need to add smooth join rules
- Lines need to be capped at their ends, with option for rounded caps
- Need more basic image transforms, such as rotate and flip
- Support for saving transparency, and drawing partially transparent colors
- Support for various color formats besides RGB (such as hex or colornames)
- And most importantly, more image formats

## License:
This code is free to share, use, reuse, and modify according to the MIT license, see license.txt

## Credits:
Karim Bahgat (2014)
Several Stackoverflow posts have been helpful for adding certain features,
and in some cases the code has been taken directly from the posts.
In other cases help and code has been found on websites.
In all such cases, the appropriate credit is given in the code.

## Contributors
I welcome any efforts to contribute code, particularly for:

- optimizing for speed, particularly the floodfill algorithm and its fuzzy variant
- adding/improving/correcting any rendering algorithms
- improve the quality of antialiasing, is currently still somewhat choppy
- fixing why image transform results in weird ripples and holes in the images
- adding new features (see Status above)


## Contents

### PyDraw.Image(...) --> class object
  - no documentation for this class

  - #### .drawbezier(...):
    Draws a bezier curve given a list of coordinate control point pairs.
    Mostly taken directly from a stackoverflow post...
    
    | **option** | **description**
    | --- | --- 
    | xypoints | list of coordinate point pairs, at least 3. The first and last points are the endpoints, and the ones in between are control points used to inform the curvature.
    | **other | also accepts various color and size arguments, see the docstring for drawline.
    | *intervals | how finegrained/often the curve should be bent, default is 100, ie curves every one percent of the line.

  - #### .drawcircle(...):
    Draws a circle at specified centerpoint.
    
    | **option** | **description**
    | --- | --- 
    | x/y | the integer x/y position to be the midpoint of the circle.
    | fillsize | required to specify the fillsize of the circle, as pixel integers
    | **other | also accepts various color and size arguments, see the docstring for drawline.

  - #### .drawline(...):
    Draws a single line.
    
    | **option** | **description**
    | --- | --- 
    | x1,y1,x2,y2 | start and end coordinates of the line, integers
    | *fillcolor | RGB color tuple to fill the body of the line with (currently not working)
    | *outlinecolor | RGB color tuple to fill the outline of the line with, default is no outline
    | *fillsize | the thickness of the main line, as pixel integers
    | *outlinewidth | the width of the outlines, as pixel integers

  - #### .drawmultiline(...):
    Draws multiple lines between a list of coordinates, useful for making them connect together.
    
    | **option** | **description**
    | --- | --- 
    | coords | list of coordinate point pairs to be connected by lines
    | **other | also accepts various color and size arguments, see the docstring for drawline.

  - #### .drawpolygon(...):
    Draws a polygon based on input coordinates.
    Note: as with other primitives, fillcolor does not work properly.
    
    | **option** | **description**
    | --- | --- 
    | coords | list of coordinate point pairs that make up the polygon. Automatically detects whether to enclose the polygon.
    | **other | also accepts various color and size arguments, see the docstring for drawline.

  - #### .floodfill(...):
    Fill a large area of similarly colored neighboring pixels to the color at the origin point.
    Adapted from http://inventwithpython.com/blog/2011/08/11/recursion-explained-with-the-flood-fill-algorithm-and-zombies-and-cats/comment-page-1/
    Note: needs to be optimized, bc now checks all neighbours multiple times regardless of whether checked before bc has no memory.
    Also, lowering the fuzzythreshhold is not a good idea as it is incredibly slow.
    
    | **option** | **description**
    | --- | --- 
    | x/t | the xy coordinate integers of where to begin the floodfill.
    | fillcolor | the new RGB color tuple to replace the old colors with

  - #### .get(...):
    Get the color of pixel at specified xy position.
    Note: mostly used internally, but may sometimes be useful for end-user too.
    
    | **option** | **description**
    | --- | --- 
    | x/y | width/height position of the pixel to retrieve, with 0,0 being in topleft corner

  - #### .load(...):
    Loads an existing image, either from a file,
    or from a list of lists containing RGB color tuples.
    If both are provided, the filepath will be used.
    
    | **option** | **description**
    | --- | --- 
    | *filepath | the string path of the image file to load, with extension
    | *data | a list of lists containing RGB color tuples

  - #### .new(...):
    Creates and returns a new image instance.
    
    | **option** | **description**
    | --- | --- 
    | width | the width of the image in pixels, integer
    | height | the height of the image in pixels, integer
    | *background | an RGB color tuple to use as the background for the image, default is white/grayish.

  - #### .put(...):
    Set the color of a pixel at specified xy position.
    Note: mostly used internally, but may sometimes be useful for end-user too.
    
    | **option** | **description**
    | --- | --- 
    | x/y | width/height position of the pixel to set, with 0,0 being in topleft corner
    | color | RGB color tuple to set to the pixel

  - #### .save(...):
    Saves the image to the given filepath.
    
    | **option** | **description**
    | --- | --- 
    | filepath | the string path location to save the image. Extension must be given and can only be ".gif".

  - #### .spheremapping(...):
    Map the image onto a 3d globe-like sphere.
    Return a new transformed image instance.
    Note: still work in progress, not fully correct.
    
    | **option** | **description**
    | --- | --- 
    | sphereradius | the radius of the sphere to wrap the image around in pixel integers
    | xoffset/yoffset/zdist | don't use, not working properly

  - #### .tilt(...):
    Performs a perspective transform, ie tilts it, and returns the transformed image.
    Note: it is not very obvious how to set the oldplane and newplane arguments
    in order to tilt an image the way one wants. Need to make the arguments more
    user-friendly and handle the oldplane/newplane behind the scenes.
    Some hints on how to do that at http://www.cs.utexas.edu/~fussell/courses/cs384g/lectures/lecture20-Z_buffer_pipeline.pdf
    
    | **option** | **description**
    | --- | --- 
    | oldplane | a list of four old xy coordinate pairs
    | newplane | four points in the new plane corresponding to the old points

  - #### .view(...):
    Pops up a Tkinter window in which to view the image

