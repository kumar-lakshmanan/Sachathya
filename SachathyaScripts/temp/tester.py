#For Sachathya

from schLib import schLookups as lookups

class testerCls():

	def __init__(self,parent):
		self.tag=self.__class__.__name__.replace('Cls','').upper()
		self.sch=parent
		self.ttls=self.sch.ttls
		self.sch.display("tester is ready!", self.tag)

	def initialize(self):
		self.sch.display("tester initialized-abc!", self.tag)
        print('nextline')
        print('ok')
        print('dd')
        
        print('ff')
        print('linr2')

if __name__ == '__main__':
	if(not hasattr(sch, 'testerObj') or sch.devMode):	
		sch.testerObj = testerCls(sch)
	sch.testerObj.initialize()