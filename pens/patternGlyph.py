"""
aGlyph > Pattern > PatternedGlyph
"""

def patternedGlyph(aGlyph, x=10, space=10):
    insides = []
    y=x
    aGlyph.round()
    for h in range(aGlyph.box[0], aGlyph.box[2], int(x+space)):
        for v in range(aGlyph.box[1], aGlyph.box[3], int(y+space)):
            if aGlyph.pointInside((h,v)):
                insides.append((h,v))
    aGlyph.clear()
    for p in insides:
        px,py = p[0],p[1]
        radius = x
        pen = aGlyph.getPen()
        r=x/1.8
        pen.moveTo((px,py-radius))
        pen.curveTo((px+r,py-radius),(px+radius,py-r),(px+radius,py)) #1
        pen.curveTo((px+radius,py+r),(px+r,py+radius),(px,py+radius)) #2
        pen.curveTo((px-r,py+radius),(px-radius,py+r),(px-radius,py)) #3
        pen.curveTo((px-radius,py-r),(px-r,py-radius),(px,py-radius)) #4
        pen.closePath()
    return aGlyph