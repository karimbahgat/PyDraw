# -*- coding: utf-8 -*-
"""
make_font.py - module for constructing simple BMP graphics files

 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so, subject to
 the following conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
__version__ = "0.1"
__about =  "make_font, version %s, written by Margus Laak, October, 2009" % __version__ 

import sys, Image, ImageDraw, ImageFont
from optparse import OptionParser
import os

def help():
    print 'make_font.py -f font file -s font size'
    print ''
    exit()

cmd_parser = OptionParser()

# add command line options
cmd_parser.add_option("-f", "--font", action="store", type="string", dest="font_file")
cmd_parser.add_option("-s", "--size", action="store", type="int", dest="font_size")
# parse
(options, args) = cmd_parser.parse_args()

font_file = getattr(options, 'font_file')
font_size = getattr(options, 'font_size')

if not font_file:
    help()

if not font_size:
    help()

font = ImageFont.truetype(font_file, font_size)

canvas_size = font_size * 3
canvas_qeometry = (canvas_size, canvas_size)

file_content = "font_data = {}\n"
for char_number in range(0, 255):
    character = chr(char_number)
    ret = []

    img = Image.new('1', canvas_qeometry)

    draw = ImageDraw.Draw(img)
    draw.text((10,10), ' %s ' % character, font=font, fill='#ffffff')
    data = img.getdata()
    #img.save('%s.png' % char_number, 'PNG')

    offset = 0
    row = ''
    first_pixel = None
    for d in data:
        if d != 0:
            row = row + '1'
        else:
            row = row + '0'

        # end of line check
        if len(row) == canvas_size:
            row = row.rstrip('0')
            
            pixel_pos = row.find('1')
            if pixel_pos > 0 and (first_pixel == None or first_pixel > pixel_pos):
                first_pixel = pixel_pos
            
            if row != '':
                if len(ret) == 0:
                    ret.append(offset-10)
                ret.append(row)
            else:
                if len(ret) > 0:
                    ret.append('')
                offset += 1
            
            # reset
            row = ''
    
    pixel_line = []
    for rx in ret:
        if type(rx) == type(''):
            pixel_line.append(rx[first_pixel:])
        else:
            pixel_line.append(rx)

    if len(pixel_line) == 0:
        # empty space
        pixel_line.append(0)
        pixel_line.append('00')

    del draw
    del img
    file_content += "font_data[%s] = %s\n" % (char_number, pixel_line)

font_name = os.path.basename(font_file)
if font_name.find('.') > 0:
    font_name = font_name[:font_name.find('.')]

fp = open("bmpfont_%s_%s.py" % (font_name, font_size), "wt")
fp.write(file_content)
fp.close()

