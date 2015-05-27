# coding=utf-8>
"""
Closer/Further

Bring different parts of the contour closer together or further away.
If a segment is selected, it will be treated as a single element.

Thom Janssen 2015
"""
from vanilla import *
from math import *

g = CurrentGlyph()

class CloserFurther(object):
	def __init__(self):
		self.w = FloatingWindow((100, 77), "C/F", closable = True)
				
		self.w.closer = SquareButton((7,7,40,30), u"Closer", callback=self.closerFurther, sizeStyle="mini")
		self.w.further = SquareButton((51,7,-7,30), u"Further", callback=self.closerFurther, sizeStyle="mini")
		self.w.value = EditText((7,43,-7,26),"10")
		self.w.open()
		
		
	def _close(self,sender):
		self.w.hide()

	
	def closerFurther(self, sender):
		g = CurrentGlyph()
		
		selections = []
		for c in g.contours:
			cSel = []
			for bPoint in c.bPoints:
				if bPoint.selected:
					cSel.append(bPoint)
			selections.append(cSel)
		selections = [x for x in selections if x != []]
		
		if len(selections) == 1: # points
			xCentroid=0
			yCentroid=0
			for p in selections[0]:
				xCentroid += p.anchor[0] #x
				yCentroid += p.anchor[1] #y
			xCentroid /= len(selections[0])
			yCentroid /= len(selections[0])
		
			g.prepareUndo()
		
			for p in selections[0]:
				anchor = p.anchor
				bcpIn =  p.bcpIn
				bcpOut = p.bcpOut
				 
				angle =  atan2(xCentroid - anchor[0], anchor[1] - yCentroid)
				if sender.getTitle() == "Closer":
					p.anchor =  anchor[0] - sin(-angle)*int(self.w.value.get()), anchor[1] - cos(-angle)*int(self.w.value.get())
					if bcpIn != (0,0):
						p.bcpIn = bcpIn
					if bcpOut != (0,0):
						p.bcpOut = bcpOut
				if sender.getTitle() == "Further":
					p.anchor =  anchor[0] + sin(-angle)*int(self.w.value.get()), anchor[1] + cos(-angle)*int(self.w.value.get())
					if bcpIn != (0,0):
						p.bcpIn = bcpIn
					if bcpOut != (0,0):
						p.bcpOut = bcpOut

				
		if len(selections) > 1: # segments
			xCentroid=0
			yCentroid=0
			# centroids of segments
			centers = {}
			nr = 0
			for seg in selections:
				centers[nr] = []
				xSegCentroid = 0
				ySegCentroid = 0
				for p in seg:
					xSegCentroid += p.anchor[0]
					ySegCentroid += p.anchor[1]
				xSegCentroid /= len(seg)
				ySegCentroid /= len(seg)
				centers[nr] = [xSegCentroid,ySegCentroid]
				nr+=1
			for c in centers:
				xCentroid += centers[c][0]
				yCentroid += centers[c][1]
			xCentroid /= len(centers)
			yCentroid /= len(centers)
			
			for c in range(len(centers)):
				angle =  atan2(xCentroid - centers[c][0], centers[c][1] - yCentroid)
				for p in selections[c]:
					anchor = p.anchor
					bcpIn =  p.bcpIn
					bcpOut = p.bcpOut

					if sender.getTitle() == "Closer":
						p.anchor =  anchor[0] - sin(-angle)*int(self.w.value.get()), anchor[1] - cos(-angle)*int(self.w.value.get())
						if bcpIn != (0,0):
							p.bcpIn = bcpIn
						if bcpOut != (0,0):
							p.bcpOut = bcpOut
					if sender.getTitle() == "Further":
						p.anchor =  anchor[0] + sin(-angle)*int(self.w.value.get()), anchor[1] + cos(-angle)*int(self.w.value.get())
						if bcpIn != (0,0):
							p.bcpIn = bcpIn
						if bcpOut != (0,0):
							p.bcpOut = bcpOut
		g.round()
		g.update()
		g.performUndo()

CloserFurther()