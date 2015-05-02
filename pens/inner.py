def inner(aGlyph):
    aGlyph.removeOverlap()
    for c in aGlyph.contours:
        if c.clockwise == True:
            pass
        else:
            #print dir(c.naked())
            c.naked().clear()
    return aGlyph
    
# g = CurrentGlyph()
# g.prepareUndo()
# inner(g)
# g.performUndo()