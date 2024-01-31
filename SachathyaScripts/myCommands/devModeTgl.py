#For Sachathya
from schLib import schLookups as lookups

class devModeTglCls():
	
	def __init__(self,parent):
		self.tag=self.__class__.__name__.replace('Cls','').upper()
		self.sch=parent
		self.ttls=self.sch.ttls
		self.sch.display("devModeTgl is ready!", self.tag)

	def initialize(self):
		title = sch.schGUIObj.windowTitle()
		if(sch.devMode):
			sch.schGUIObj.setWindowTitle(title.replace(' - DevMode',''))
			sch.devMode = 0
			self.sch.display("Developer Mode - Off", self.tag)
		else:
			sch.schGUIObj.setWindowTitle(title + ' - DevMode')
			sch.devMode = 1
			self.sch.display("Developer Mode - On", self.tag)
		
if __name__ == '__main__':
	if(not hasattr(sch, 'devModeTglObj') or sch.devMode):	
		sch.devModeTglObj = devModeTglCls(sch)
	sch.devModeTglObj.initialize()