def outer(aGlyph):
    aGlyph.removeOverlap()
    for c in aGlyph.contours:
        if c.clockwise == False:
            pass
        else:
            #print dir(c.naked())
            c.naked().clear()
    return aGlyph
    
# g = CurrentGlyph()
# g.prepareUndo()
# outer(g)
# g.performUndo()