def removeOverlap(aGlyph):
    aGlyph.decompose()
    aGlyph.removeOverlap()
    return aGlyph