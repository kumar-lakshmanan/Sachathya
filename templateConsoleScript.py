'''
#For Sachathya
'''
from schLib import schLookups as lookups

class myClassCls():
	
	def __init__(self,parent):
		self.tag="myClass"
		self.sch=parent
		self.ttls=self.sch.ttls
		self.sch.display("myClassCls is ready!", self.tag)

	def initialize(self):
		self.sch.display("myClassCls initialized!", self.tag)

if __name__ == '__main__':
	dev.myClassClsObj = myClassCls(dev)
	dev.myClassClsObj.initialize()
