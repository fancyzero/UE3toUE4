import sys
import T3DPropertyParser as t3dpp
intenter = "   "
intent_str = "   "
EOL = "\n"
output_device=sys.stdout
class PyUObject:

    def __init__(self):
        self.cls = ""
        self.name = ""
        self.children = []
        self.properties = {}
        self.parent = None

    def attach_to(self, new_parent):
        if self == new_parent:
            return
        self.detach_from_parent()
        if new_parent != None:
            new_parent.children.append(self)
        self.parent = new_parent

    def detach_from_parent(self):
        if self.parent != None:
            self.parent.children.remove(self)
        self.parent = None

    def output_properties(self, depth):
        for k,v in self.properties.iteritems():
            output_device.write(intent_str * depth +k+"=" +t3dpp.dump(v)+EOL)


    #output
    def output_begin_object(self, depth, output_class=True):
        intent = intent_str * depth
        str = intent + "Begin Object"
        if self.cls and output_class:
            str += " Class=" + self.cls
        if self.name:
            str += " Name=\"" + self.name+"\""
        output_device.write( str+EOL)

    def output_end_object(self,depth):
        intent = intent_str * depth
        output_device.write( intent + "End Object"+EOL)

    def output_as_t3d(self):
        depth = 0
        self.output_begin_object(0,output_class=True)
        for child in self.children:
            child.output_declare(depth + 1)
        for child in self.children:
            child.output_detail(depth + 1)
        self.output_properties(depth + 1)
        self.output_end_object(0)

    def output_declare(self, depth):
        self.output_begin_object(depth,output_class=True)
        for child in self.children:
            child.output_declare(depth + 1)
        self.output_end_object(depth)

    def output_detail(self, depth):
        self.output_begin_object(depth,output_class=False)
        self.output_properties(depth + 1)
        for child in self.children:
            child.output_detail(depth + 1)
        self.output_end_object(depth)

    # for debugging
    def debug_list_child(self):
        for child in self.children:
            output_device.write( child.name)

    def debug_output_struct(self, depth):
        str = intenter * depth;
        if self.name:
            str += "name: " + self.name
        if self.cls:
            str += "<" + self.cls + ">"
        output_device.write( str)
        for child in self.children:
            child.output_struct(depth + 1)
