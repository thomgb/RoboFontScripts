def outerInner(aGlyph,oi=False):
    aGlyph.removeOverlap()
    for c in aGlyph.contours:
        if c.clockwise == oi:
            pass
        else:
            #print dir(c.naked())
            c.naked().clear()
    return aGlyph


