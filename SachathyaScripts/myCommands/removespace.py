#For Sachathya
from schLib import schLookups as lookups

class removespaceCls():
	
	def __init__(self,parent):
		self.tag=self.__class__.__name__.replace('Cls','').upper()
		self.sch=parent
		self.ttls=self.sch.ttls
		self.sch.display("removespace is ready!", self.tag)

	def initialize(self):
		self.path = self.doGetClipboard()
		self.path = self.path.replace(' ','')
		print(self.path)
		self.doSetClipboard(self.path)

		self.sch.schGUIObj.show()

	def doSetClipboard(self, text):
		cb = self.sch.schQtApp.clipboard()
		cb.clear(mode=cb.Clipboard)
		cb.setText(text, mode=cb.Clipboard)	

	def doGetClipboard(self):
		cb = self.sch.schQtApp.clipboard()
		return str(cb.text(mode=cb.Clipboard))

if __name__ == '__main__':
	if(not hasattr(sch, 'removespaceObj') or sch.devMode):	
		sch.removespaceObj = removespaceCls(sch)
	sch.removespaceObj.initialize()