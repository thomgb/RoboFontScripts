def patternedGlyph(aGlyph,):
    insides = []
    copy.removeOverlap()
    for c in copy.contours:
        c.clockwise = True
    return aGlyph
    
    
g = CurrentGlyph()
g.prepareUndo()
print (g.contours[1].clockwise)

copy = g.copy()
copy.naked().setParent(g.naked().getParent())
drawGlyph(patternedGlyph(copy))
g.performUndo()