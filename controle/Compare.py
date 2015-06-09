from robofab import *
from mojo.UI import *
from mojo.events import addObserver, removeObserver
from mojo.drawingTools import *
from vanilla import *
from lib.tools.notifications import PostNotification

event = "drawBackground" 

class Compare(object):
		
	def __init__(self):
		self.w = FloatingWindow((200, 200), "Compare", closable = False)
		
		self.w.sluit = SquareButton((7,-22,-7,-7), "Close", callback=self._close, sizeStyle="mini")
		
		columnDescriptions = [dict(title="", key="checkBox", cell=CheckBoxListCell(), width=15),
								 dict(title="font",width=200-29,editable=False),
								 ]
		self.w.fontList = List(
								(7,7,-7,-30), items=[], 
								columnDescriptions=columnDescriptions,
								doubleClickCallback=self.makeThisFontCurrent,
							   )
							   		
		addObserver(self, "drawfunction", event)
		addObserver(self, "buildOpenFontList", "fontWillOpen")
		addObserver(self, "buildOpenFontList", "fontDidClose")
		
		self.buildOpenFontList(sender=1)
		self.w.open()
		
	
	def buildOpenFontList(self, sender):
		items = []
		height = 7+18+30
		if len(AllFonts()) is not 0:
			for font in AllFonts():
				height += 19
				items.append(dict(
									checkBox = True,
									font = "%s - %s" % (font.info.familyName, font.info.styleName), 
									f = font
									))
		else:
			items.append(dict(
									checkBox = False,
									font = "Open some fonts!", 
									))
			height += 19
		self.w.fontList.set(items)
		
		self.w.resize(200,height)
		
	def makeThisFontCurrent(self,sender):
		f = sender.get()[sender.getSelection()[0]]["f"]
		#AllFonts().getFontsByFamilyNameStyleName(f.info.familyName, f.info.styleName)
		OpenFont(f.path)
		PostNotification('doodle.updateGlyphView')	
	
	def _close(self,sender):
		self.w.hide()
		removeObserver(self, event)
		removeObserver(self, "fontWillOpen")
		removeObserver(self, "fontDidClose")
	
	def drawfunction(self, info):
		g = CurrentGlyph()
		f = CurrentFont()
		currentFont = "%s-%s" % (f.info.familyName,f.info.styleName)
		name = g.name
		
		items = self.w.fontList.get()
		fontList = []
		for item in items:
			if not item["checkBox"]:
				continue
			fontList.append(item['f'])
		
		longestName = 0
		for fontName in fontList:
			if len("%s-%s" % (fontName.info.familyName,fontName.info.styleName)) > longestName:
				longestName = len("%s-%s" % (fontName.info.familyName,fontName.info.styleName))
			
		save()
		margin = info['scale']*40
		translate(g.width+margin, margin)
		fill(0, 0.2, 0.2)
		font("InputMono")
		fontSize(info['scale']*12)
		
		contourCount = len(g)
		
		contourPoints = ""
		pointCount = []
		for c in g.contours:
			contourPoints += str(len(c))
			contourPoints += " "
			pointCount.append(len(c))
		tabs = longestName-len("Current")
		text("Current%s  %s, %s" % (" "*tabs,contourCount,contourPoints), (0,0))
		
		fill(0.2, 0.6, 0.5)
		
		for fontName in fontList:
			famAndStyleName = "%s-%s" % (fontName.info.familyName,fontName.info.styleName)
			if str(famAndStyleName) != str(currentFont):
				translate(0, info['scale']*20)
				contourPoints = ""
				
				for c in fontName[name].contours:
					contourPoints += str(len(c))
					contourPoints += " "
				tabs = longestName-len(famAndStyleName)
				
				if contourCount != len(fontName[name]):
					fill(0.8, 0.0, 0.2)				
				else:
					fill(0.2, 0.55, 0.5)
				text("%s%s  %s, %s" % (famAndStyleName," "*tabs,len(fontName[name]),contourPoints), (0,0))
		
		restore()
		
Compare()
