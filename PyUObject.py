import sys
intenter = "   "
intent_str = "   "

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
            output_device.write(intent_str * depth )
            self.output_properties_recursiv(k, v, depth)
            output_device.write("\r\n")

    def output_properties_recursiv(self, key, value, depth):
        if value.__class__ == dict:
            output_device.write( key + "=(")
            need_comma = False
            for k,v in value.iteritems():
                if need_comma:
                    output_device.write(",")
                else:
                    need_comma = True
                self.output_properties_recursiv(k,v,depth)
            output_device.write(")")
        else:
            output_device.write(  key + "=" + value )



    #output
    def output_declare(self, depth):
        intent = intent_str * depth
        str = intent + "Begin Object"
        if self.name:
            str += " Name=" + self.name
        if self.cls:
            str += " CLass=" + self.cls
        output_device.write( str+"\r\n")
        for child in self.children:
            child.output_declare(depth + 1)
        output_device.write( intent + "End Object\r\n")

    def output_detail(self, depth):
        intent = intent_str * depth
        str = intent + "Begin Object"
        if self.name:
            str += " Name=" + self.name
        if self.cls:
            str += " CLass=" + self.cls
        output_device.write( str+"\r\n")
        self.output_properties(depth + 1)
        for child in self.children:
            child.output_detail(depth + 1)
        output_device.write( intent + "End Object\r\n")

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
