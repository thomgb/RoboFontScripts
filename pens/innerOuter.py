def innerOuter(aGlyph,io=False):
    aGlyph.removeOverlap()
    for c in aGlyph.contours:
        if c.clockwise == io:
            pass
        else:
            #print dir(c.naked())
            c.naked().clear()
    return aGlyph


