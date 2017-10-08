#For Sachathya
from schLib import schLookups as lookups

class myClassCls():
	
	def __init__(self,parent):
		self.tag=self.__class__.__name__.replace('Cls','').upper()
		self.sch=parent
		self.ttls=self.sch.ttls
		self.sch.display("myClass is ready!", self.tag)

	def initialize(self):
		self.sch.display("myClass initialized!", self.tag)

if __name__ == '__main__':
	if(not hasattr(sch, 'myClassObj') or sch.devMode):	
		sch.myClassObj = myClassCls(sch)
	sch.myClassObj.initialize()
