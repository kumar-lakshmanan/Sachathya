'''
#For DevConsole
'''

class myClassCls():
	
	def __init__(self,parent):
		self.parent=parent
		self.tools=self.parent.ttls		
		self.qtTools=self.parent.qtTools
		self.parent.pylib.say("myClassCls is ready!")

	def initialize(self):
		#insert your initialization and code logic here
		
		self.parent.pylib.say("myClassCls initialized!")

if __name__ == '__main__':
	dev.myClassClsObj = myClassCls(dev)
	dev.myClassClsObj.initialize()
