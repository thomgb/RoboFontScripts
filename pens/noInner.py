def outer(aGlyph):
    aGlyph.removeOverlap()
    for c in aGlyph.contours:
        c.clockwise = True
    return aGlyph
    
