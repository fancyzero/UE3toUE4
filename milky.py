import sys
import re

# repsent struct and intent level
global intent
global intent_str

intent_str = "   "
intent = 0

def add_intent():
	intent = intent + 1

def sub_intent():
	intent = intent - 1

def output(str):
	print intent_str * intent + str

class Object:
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
		
	def output_propertier(self,depth):
		for k,v in self.properties.iteritems():
			print intent_str * depth + k+"=" + v

	def output_declare(self,depth):
		intent = intent_str*depth
		str = intent +  "Begin Object"
		if self.name:
			str += " Name="+self.name
		if self.cls:
			str += " CLass="+self.cls
		print str
		for child in self.children:
			child.output_declare(depth+1)
		print intent + "End Object"
		
	def output_detail(self,depth):
		intent = intent_str*depth
		str = intent +  "Begin Object"
		if self.name:
			str += " Name="+self.name
		if self.cls:
			str += " CLass="+self.cls
		print str
		self.print_propertier(depth+1)
		for child in self.children:
			child.output_detail(depth+1)

		print intent + "End Object"

#for debugging		
	def debug_list_child(self):
		for child in self.children:
			print child.name
			
	def debug_output_struct(self, depth):
		str = intenter * depth;
		if self.name:
			str += "name: " + self.name 
		if self.cls:
			str  += "<"+self.cls+">"
		print str
		for child in self.children:
			child.output_struct(depth+1)

		
def find_obj_by_class(root, class_name):
	if root == None:
		return None
	if root.cls == class_name:
		return root
	for child in root.children:
		ret = find_obj_by_class(child, class_name)
		if ret != None:
			return ret

#Reposition object in UE3 tree , to match UE4 partten
def reposition_obj( root, obj ):
	# rule 1 move all module under ParticleSystem Node 
	if obj.cls.startswith("ParticleModule"):
		new_parent = find_obj_by_class(root, "ParticleSystem")
		obj.attach_to(new_parent)

def fix_properties(obj):
	for k in obj.properties.keys():
		if k == "ObjectArchetype":
			del obj.properties[k]
		if k == "Name":
			del obj.properties[k]

def extract_params ( line ):
	params = re.findall(r'(\w+)=\"*(\w+)\"*', line)
	pmap = {}
	for k,v in params:
		pmap[k]=v
	return pmap

def read_object(obj,f):
	child = None
	while True:
		line = f.readline()
		line = line.strip()
		if line == "":
			return child
		if line.startswith("Begin Object"):
			child = Object()
			params = extract_params(line)
			child.name = params.get("Name")
			child.cls = params.get("Class")
			read_object(child,f)
			child.attach_to(obj)
		elif line.startswith("End Object"):
			return obj
		else:
			if obj != None:
				pos = line.find("=")
				obj.properties[line[0:pos]] = line[pos+1:]
	return child

def convert(root, obj):
	reposition_obj(root, obj)
	fix_properties(obj)

def get_all_objects(root):
	ret = []
	ret.append(root)
	for child in root.children:
		ret = ret + get_all_objects(child)
	return ret

def list_struct(filename):
	f = open(filename)
	root = read_object(None,f)
	root.output_struct(0)

def convert_file(filename):
	f = open(filename)
	root = read_object(None,f)
	all_obj = get_all_objects(root)
	for obj in all_obj:
		convert(root,obj)
	root.output_declare(0)
	root.output_detail(0)

def main():
	if len(sys.argv) < 2:
		print " need file name"
		exit()
	filename = sys.argv[1]
	convert_file(filename)

main()


		

		

	