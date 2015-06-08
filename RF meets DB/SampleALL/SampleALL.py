"""
Create an image/sample of every UFO in the root folder + sub folders.

If a sample already excist then the image will be refreshed if the UFO is changed.
A seperate file (statsfile) keeps track of the modification dates of the UFOs.

Thom Janssen 2015
TODO:
    - mark png files with no ufo any more, now only prints out the rough ones
"""

import os
from drawBot import *
from robofab.world import OpenFont
from time import gmtime, strftime
# print strftime("%d %b %Y %H:%M")
user = os.getlogin()


page = (1000, 750)

rootdir ='/Users/%s/your/path/to/ufos' % user

sample = "abcdefghijklmnopqrstuvwxyz"
regel2 = sample.upper()


def drawGlyph(glyph):
    from fontTools.pens.cocoaPen import CocoaPen
    pen = CocoaPen(glyph.getParent())
    glyph.draw(pen)
    drawPath(pen.path)

## Stats file
statfile = "/Users/%s/path/to/sample.stats.txt" % user
stats = open(statfile,'r').read().split("\n")
# print stats
newStats = """"""
knownUfos = []

for ufo, dirs, files in os.walk(rootdir):
    if ufo.endswith('.ufo'):
            knownUfos.append(ufo.split("/")[-1][:-4])

            #print ufo
            ## get modified date
            ufoModDate = os.stat(ufo).st_mtime
            newStats += "%s\n" % ufoModDate
            
            if str(ufoModDate) not in stats:
                f = OpenFont(ufo)
                fam = f.info.familyName
                style = f.info.styleName
                if fam == None:
                    fam = "NONAME"
                if style == None:
                    style = "NONAME"
                print ufo.split("/")[-1][:-4]
                newPage(*page)
                text("%s %s-%s  %s" % (strftime("%d %b %Y %H:%M"), fam ,style,ufo.split("/")[-1]),(10,10))
                translate(50,500)
                scale(.25)
                save()
                for l in sample:
                    try:
                        drawGlyph(f[l])
                        translate(f[l].width)
                    except:
                        pass
                restore()
                save()
                translate(0,-1000)
                for l in regel2:
                    try:
                        drawGlyph(f[l])
                        translate(f[l].width)
                    except:
                        pass
                restore()
                save()
                translate(0,-1300)
                scale(.2)
                for l in sample:
                    try:
                        drawGlyph(f[l])
                        translate(f[l].width)
                    except:
                        pass
                restore()
                save()
                translate(0,-1500)
                scale(.2)
                for l in regel2:
                    try:
                        drawGlyph(f[l])
                        translate(f[l].width)
                    except:
                        pass
                restore()
                saveImage(rootdir+'/Specimens/'+fam+" "+style+"__"+ufo.split("/")[-1][:-4]+'.png')

# Print Rough PNGS
for root, dirs, files in os.walk(rootdir+"/Specimens/"):
    for png in files:
        if png.endswith('.png'):
            if png.split("__")[1][:-4] not in knownUfos:
                print png, "NO UFO"
# update to stats
sf = open(statfile,'w')
sf.write(newStats)
sf.close()

print 'done'