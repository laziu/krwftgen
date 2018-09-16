#!/usr/bin/env python3
import subprocess, traceback
from tools import *

class path:
  assets = "./assets"
  css    = "./public/css"
  subset = "./public/fonts"
  dest = "/fonts"
  reference = "sample.css"


fonts = [
#  FontInfo("KoPub Batang", 300,
#           "KOPUB_OTF_FONTS/KoPub Batang_Pro Light.otf", 
#           "KOPUB_TTF_FONTS/KoPub Batang Light.ttf"),
#  FontInfo("KoPub Batang", 700, 
#           "KOPUB_OTF_FONTS/KoPub Batang_Pro Bold.otf",
#           "KOPUB_TTF_FONTS/KoPub Batang Bold.ttf")
]


try:
  unicodes = get_unicode_range_from_css(readlines(path.reference))
  cmd = Command(path.assets, path.subset)
  generate_path(path.css)
  for font in fonts:
    cmd.setFont(font)
    generate_path("%s/%s-%d/" % (path.subset, font.name, font.size))
    with open("%s/%s-%d.css" % (path.css, font.name, font.size), "w") as f:
      css_file = FontCssFile(font, f, path.dest)
      for i, uni_range in enumerate(unicodes):
        cmd.setRangeWithIndex(uni_range, i)
        css_file.write(i, uni_range)
        print('processing %s-%d.%02d' % (font.name, font.size, i))
        
        subprocess.check_call(cmd.setFontType('woff2').get())
        subprocess.check_call(cmd.setFontType('woff').get())
        if font.ttf is not None:
          subprocess.check_call(cmd.setFontType('ttf').get())

except Exception as ex:
  print('\033[93m', traceback.format_exc(), '\033[0m')
  print('\033[91m', ex, '\033[0m')
