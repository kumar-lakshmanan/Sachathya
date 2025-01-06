#For Sachathya
from schLib import schLookups as lookups
from Qt import QtWidgets
from NodeGraphQt import NodeGraph, BaseNode


# create a node class object inherited from BaseNode.
class FooNode(BaseNode):

    # unique node identifier domain.
    __identifier__ = 'io.github.jchanvfx'

    # initial default node name.
    NODE_NAME = 'Foo Node'

    def __init__(self):
        super(FooNode, self).__init__()

        # create an input port.
        self.add_input('in1', color=(180, 80, 0))
        self.add_input('in2', color=(180, 80, 0))

        # create an output port.
        self.add_output('out1')
        self.add_output('out2')

class pygraphCls():
    
    def __init__(self,parent):
        self.tag=self.__class__.__name__.replace('Cls','').upper()
        self.sch=parent
        self.ttls=self.sch.ttls
        self.sch.display("pygrssssssaph is ready!", self.tag)

    def initialize(self):
        
        graph = NodeGraph()

        # register the FooNode node class.
        graph.register_node(FooNode)

        # show the node graph widget.
        graph_widget = graph.widget
        graph_widget.show()

        # create two nodes.
        node_a = graph.create_node('io.github.jchanvfx.FooNode', name='node A')
        node_b = graph.create_node('io.github.jchanvfx.FooNode', name='node B', pos=(300, 50))
        node_c = graph.create_node('io.github.jchanvfx.FooNode', name='node C', pos=(200, 50))

        # connect node_a to node_b
        node_a.set_output(0, node_b.input(0))        
        self.sch.display("pygraph initialized!", self.tag)

if __name__ == '__main__':
    if(not hasattr(sch, 'pygraphObj') or sch.devMode):    
        sch.pygraphObj = pygraphCls(sch)
    sch.pygraphObj.initialize()