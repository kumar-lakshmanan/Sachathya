#For Sachathya
from schLib import schLookups as lookups

class schShowHideCls():
	
	def __init__(self,parent):
		self.tag=self.__class__.__name__.replace('Cls','').upper()
		self.sch=parent
		self.ttls=self.sch.ttls
		self.sch.display("schShowHide is ready!", self.tag)

	def initialize(self):
		self.sch.display("schShowHide initialized!", self.tag)
		if(sch.schGUIObj.isHidden()):
			sch.schGUIObj.setVisible(1)
			sch.schGUIObj.showNormal()
		else:
			sch.schGUIObj.setVisible(0)			

if __name__ == '__main__':
	if(not hasattr(sch, 'schShowHideObj') or sch.devMode):	
		sch.schShowHideObj = schShowHideCls(sch)
	sch.schShowHideObj.initialize()