#For Sachathya
from schLib import schLookups as lookups

class QuickCls():
	
	def __init__(self,parent):
		self.tag=self.__class__.__name__.replace('Cls','').upper()
		self.sch=parent
		self.ttls=self.sch.ttls
		self.sch.display("Quick is ready!", self.tag)

	def initialize(self):
		self.sch.display("Quick initialized more info added!", self.tag)

if __name__ == '__main__':
	if(not hasattr(sch, 'QuickObj') or sch.devMode):	
		sch.QuickObj = QuickCls(sch)
	sch.QuickObj.initialize()
