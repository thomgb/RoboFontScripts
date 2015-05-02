def dots(aGlyph, cube=10, radius=40):
    
    points = []
    for c in aGlyph.contours:
        for p in c.points:
            points.append((p.x,p.y))
    aGlyph.clear()
    for p in points:
        x,y = p[0], p[1]
        pen = aGlyph.getPen()
        ## CUBE
        # pen.moveTo((p[0],p[1]))
        # pen.lineTo((p[0]+cube,p[1]))
        # pen.lineTo((p[0]+cube,p[1]+cube))
        # pen.lineTo((p[0],p[1]+cube))
        
        ## OVAL
        r=radius/1.8
        pen.moveTo((x,y-radius))
        pen.curveTo((x+r,y-radius),(x+radius,y-r),(x+radius,y)) #1
        pen.curveTo((x+radius,y+r),(x+r,y+radius),(x,y+radius)) #2
        pen.curveTo((x-r,y+radius),(x-radius,y+r),(x-radius,y)) #3
        pen.curveTo((x-radius,y-r),(x-r,y-radius),(x,y-radius)) #4
        
        pen.closePath()
        #pen.oval(p[0]-radius, p[1]-radius, 2*radius, 2*radius)
    return aGlyph
#dots(CurrentGlyph())

# pen.moveTo((x-size, y-size))
# 		pen.lineTo((x+size, y-size))
# 		pen.lineTo((x+size, y+size))
# 		pen.lineTo((x-size, y+size))
# 		pen.lineTo((x-size, y-size))
# 		pen.closePath()