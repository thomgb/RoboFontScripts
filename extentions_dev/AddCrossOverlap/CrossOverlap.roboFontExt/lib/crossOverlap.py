"""
Add overlap to crossbars (EFHKT etc.)
Select two points -in the same contour- where the overlap is required. And run.

Thom Janssen 2015
v0.4
"""

from AppKit import NSImage
from lib.UI.toolbarGlyphTools import ToolbarGlyphTools
from mojo.events import addObserver
import os
from math import *

#from eventTools.eventManager import getEventsToolbarItem, publishEvent
#:)

class CrossOverlapTool(object):
		
	base_path = os.path.dirname(__file__)
	
	def __init__(self):
		
		addObserver(self, "crossOverlapToolbarItem", "glyphWindowWillShowToolbarItems")

	def crossOverlapToolbarItem(self, info):
		
		toolbarItems = info['toolbarItems']
		
		label = 'Cross Overlap'
		identifier = 'crossOverlap'
		filename = 'toolbarCrossOverlap.pdf'
		callback = self.crossOverlap
		index=-2
		
		imagePath = os.path.join(self.base_path, 'resources', filename)
		image = NSImage.alloc().initByReferencingFile_(imagePath)
		
		view = ToolbarGlyphTools((30, 25), 
			[dict(image=image, toolTip=label)], trackingMode="one")
		
		newItem = dict(itemIdentifier=identifier,
			label = label,
			callback = callback,
			view = view
		)
		
		toolbarItems.insert(index, newItem)
	
	def selectionInOneContour(self, g):
		# please tell me this can be easier...
		sel= g.selection
		if len(sel) != 2:
			return
		for c in g:
			one = False
			two = False
			for s in c.segments:
				if sel[0] in s:
					one = True
			for s in c.segments:
				if sel[1] in s:
					two = True
			if one and two:
				return True
		

	def getStartPoint(self, g):
		for c in g.contours:
			for p in c.points:
				if p.selected:
					return(c[-1][-1])

	def setStartPoint(self, g, startPoint):
		startx, starty = (startPoint.x,startPoint.y)
		for c in g.contours:
			n=-1
			for p in c.points:
				n+=1
				if (p.x, p.y) == (startx, starty):
					c.naked().setStartPoint(n)



	def calculateAngle(self, start, end):
		b = end[0] - start[0]
		a = end[1] - start[1]
		c = sqrt(a ** 2 + b ** 2)
		if c == 0:
			return None
		cosAngle = b / c
		sinAngle = a / c
		cosAngle = degrees(acos(cosAngle))
		sinAgnle = degrees(asin(sinAngle))
		if sinAngle < 0:
			#cosAngle = 360 - cosAngle
			pass
		return cosAngle

	
	def checkStraightLines(self, g, selection, tolerance=2,):
		for contour in g.contours:
			l = len(contour.points)
			for i in range(0, l, 1):
				prev = contour.points[i-1]
				cur = contour.points[i]
				next = contour.points[(i+1)%l]
				if (cur.x, cur.y) in selection:
					angle1 = self.calculateAngle((prev.x,prev.y),(cur.x,cur.y))
					angle2 = self.calculateAngle((cur.x,cur.y),(next.x,next.y))
					if abs(angle1 - angle2) < tolerance:
						cur.name = "unnecessaryPoint"
		for contour in g.contours:
			for point in contour.points:
				if point.name ==  "unnecessaryPoint":
					point.getParent().removePoint(point)
		g.update()


	def crossOverlap(self, sender):
	
		overlap = 20

		g = CurrentGlyph()
		
		if not self.selectionInOneContour(g):
			# multiple contours not yet supported
			return

		g.prepareUndo()

		## select 2 points
		startPoint = self.getStartPoint(g)
		
		selection = []
		
		for p in g.naked().selection.getSelectionObjects():
			selection.append( (p.x, p.y) )

		g.naked().selection.breakContour()

		## create seperate contours
		for i in range(len(g)):
			#print i
			# every new contour become the first contour...
			g[0].selected = True
			g.naked().selection.joinContours()
			g[0].selected = True
			g.naked().selection.removeOverlap()

			self.checkStraightLines(g, selection)


		## aftermath
		g.autoContourOrder()

		for c in g.contours:
			for p in c.points:
				if (p.x, p.y) in selection:
					hit = True
				else: hit = False
			if hit == True:
				## perform overlap
				first = len(c)-1	
				angle = atan2(c[first][0].x - c[0][0].x, c[0][0].y - c[first][0].y)
				c[first][0].x -= sin(-angle)*overlap
				c[first][0].y -= cos(-angle)*overlap
				
				##
				last = len(c)-2
				if c[last].type == 'curve':
					i = 2
					angle = atan2(c[last][2].x - c[last][1].x, c[last][1].y - c[last-0][2].y)
					c[last][2].x -= sin(-angle)*overlap
					c[last][2].y -= cos(-angle)*overlap
				else:
					angle = atan2(c[last][0].x - c[last-1][0].x, c[last-1][0].y - c[last-0][0].y)
					c[last][0].x -= sin(-angle)*overlap
					c[last][0].y -= cos(-angle)*overlap
		
		self.setStartPoint(g, startPoint)

		g.performUndo()

		g.update()

CrossOverlapTool()







"""
from mojo.UI import *

w = CurrentGlyphWindow()

print len(w.window().getToolbarItems())
print (w.window().getToolbarItems())
"""


