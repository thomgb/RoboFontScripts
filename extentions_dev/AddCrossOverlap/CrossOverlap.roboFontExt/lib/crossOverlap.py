"""
Add overlap to crossbars (EFHKT etc.)
Select two points -in the same contour- where the overlap is required. And run.

TODO:
	-Support addOverlap with multiple contours (ABPR etc.)
	-Make a staightLineCheck. When a glyph is skewed, the original points in 
	 the stem do not get removed by removeOverlap.


Thom Janssen 2015
"""

from AppKit import NSImage
from lib.UI.toolbarGlyphTools import ToolbarGlyphTools
from mojo.events import addObserver
import os
from math import atan2, sin, cos


class CrossOverlapTool(object):
		
	base_path = os.path.dirname(__file__)
	
	def __init__(self):
		
		addObserver(self, "crossOverlapToolbar", "glyphWindowDidOpen")

	def crossOverlapToolbar(self, info):
		window = info['window']
		if window is None:
			return
		
		label = 'Cross Overlap'
		identifier = 'crossOverlap'
		filename = 'toolbarCrossOverlap.pdf'
		callback = self.crossOverlap
		#index = len( window.getToolbarItems() )-1
		index = -2

		toolbarItems = window.getToolbarItems()
		vanillaWindow = window.window()
		displayMode = vanillaWindow._window.toolbar().displayMode()
		imagePath = os.path.join(self.base_path, 'resources', filename)
		image = NSImage.alloc().initByReferencingFile_(imagePath)
		
		view = ToolbarGlyphTools(
			(25, 25), 
			[dict(image=image, toolTip=label)], 
			trackingMode="one",
			)
		
		newItem = dict(itemIdentifier=identifier,
			label = label,
			callback = callback,
			view = view
		)
		
		toolbarItems.insert(index, newItem)
		vanillaWindow.addToolbar(
			toolbarIdentifier="toolbar-%s" % identifier, 
			toolbarItems=toolbarItems, 
			addStandardItems=False,
			)
		vanillaWindow._window.toolbar().setDisplayMode_(displayMode)
	
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
		else:
			return False

	def crossOverlap(self, sender):
	
		overlap = 20

		g = CurrentGlyph()
		
		if not self.selectionInOneContour(g):
			return

		g.prepareUndo()

		## select 2 points
		selection = []
		for p in g.naked().selection.getSelectionObjects():
			selection.append( (p.x, p.y) )

		g.naked().selection.breakContour()

		## create seperate contours
		for i in range(len(g)):
			#print i
			# every new contour become the first contour...
			clockwise = g[0].clockwise
			g[0].selected = True
			g.naked().selection.joinContours()
			g[0].selected = True
			g.naked().selection.removeOverlap()
			g[0].clockwise = clockwise

		## aftermath
		g.autoContourOrder()

		for c in g.contours:
			for p in c.points:
				if (p.x, p.y) in selection:
					hit = True
				else: hit = False
			if hit == True:
				## perform overlap
				## first point always good?
				first = len(c)-1	
				angle = atan2(c[first][0].x - c[0][0].x, c[0][0].y - c[first][0].y)
				c[first][0].x -= sin(-angle)*overlap
				c[first][0].y -= cos(-angle)*overlap
				
				##
				last = len(c)-2
				angle = atan2(c[last][0].x - c[last-1][0].x, c[last-1][0].y - c[last-0][0].y)
				c[last][0].x -= sin(-angle)*overlap
				c[last][0].y -= cos(-angle)*overlap

		g.performUndo()

		g.update()

CrossOverlapTool()







"""
from mojo.UI import *

w = CurrentGlyphWindow()

print len(w.window().getToolbarItems())
print (w.window().getToolbarItems())
"""


