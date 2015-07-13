import sys
import T3DPropertyParser as t3dpp
intenter = "   "
intent_str = "   "
EOL = "\n"

class PyUObject:

    def __init__(self):
        self.cls = ""
        self.name = ""
        self.children = []
        self.properties = {}
        self.parent = None


    def merge(self, other):
        print "merge with :"
        for k,v in other.properties.iteritems():
            print k,v
            print v.__class__
            if self.properties[k].__class__ == str:
                if not self.properties.has_key(k):
                    self.properties[k] = v
            if self.properties[k].__class__ == dict:
                print "merge dict", self.properties[k]
                if not self.properties.has_key(k):
                    self.properties[k] = v
                else:
                    self.properties[k].update(v)
            self.children = other.children




    def add_child(self, new_child):
        for i in self.children:
            if i.name == new_child.name:
                #if there is already a object with same name ,
                # just append new properties, but don't replace properties that already have
                # the children property will be merged
                i.merge(new_child)
                return
        self.children.append(new_child)

    def attach_to(self, new_parent):
        if self == new_parent:
            return
        self.detach_from_parent()
        if new_parent != None:
            new_parent.add_child(self)
        self.parent = new_parent

    def detach_from_parent(self):
        if self.parent != None:
            self.parent.children.remove(self)
        self.parent = None

    def output_properties(self, depth,output_device):
        for k,v in self.properties.iteritems():
            output_device.write(intent_str * depth +k+"=" +t3dpp.dump(v)+EOL)


    #output
    def output_begin_object(self, depth, output_device, output_class=True):
        intent = intent_str * depth
        str = intent + "Begin Object"
        if self.cls and output_class:
            str += " Class=" + self.cls
        if self.name:
            str += " Name=\"" + self.name+"\""
        output_device.write( str+EOL)

    def output_end_object(self,depth,output_device):
        intent = intent_str * depth
        output_device.write( intent + "End Object"+EOL)

    def output_as_t3d(self, output_device):
        depth = 0
        self.output_begin_object(0,output_device,output_class=True)
        for child in self.children:
            child.output_declare(depth + 1,output_device)
        for child in self.children:
            child.output_detail(depth + 1,output_device)
        self.output_properties(depth + 1,output_device)
        self.output_end_object(0,output_device)

    def output_declare(self, depth,output_device):
        self.output_begin_object(depth,output_device,output_class=True)
        for child in self.children:
            child.output_declare(depth + 1,output_device)
        self.output_end_object(depth,output_device)

    def output_detail(self, depth,output_device):
        self.output_begin_object(depth,output_device,output_class=False)
        self.output_properties(depth + 1,output_device)
        for child in self.children:
            child.output_detail(depth + 1,output_device)
        self.output_end_object(depth,output_device)

    # for debugging
    def debug_list_child(self):
        for child in self.children:
            print ( child.name)

    def debug_output_struct(self, depth):
        str = intenter * depth
        if self.name:
            str += "name: " + self.name
        if self.cls:
            str += "<" + self.cls + ">"
        print ( str)
        for child in self.children:
            child.output_struct(depth + 1)
