import sys
import re
class Object:
	def __init__(self):
		self.cls = ""
		self.name = ""
		self.children = []
		self.data = []
		self.parent = None
	def list_child(self):
		for child in self.children:
			print child.name
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
		if line == "":
			return child
		if line.strip().startswith("Begin Object"):
			child = Object()
			params = extract_params(line)
			child.name = params.get("Name")
			child.cls = params.get("Class")
			read_object(child,f)
			child.attach_to(obj)
		elif line.strip().startswith("End Object"):
			return obj
		else:
			if obj != None:
				obj.data.append(line)
	return child

def convert(root, obj):
	reposition_obj(root, obj)
	for child in obj.children:
		convert(root, child)

def do_get_all_objects(ret, current):
	if current == None:
		return
	for child in current.children:
		ret.append(child)
		do_get_all_objects(ret, child)

def get_all_objects(root):
	ret = []
	do_get_all_objects(ret, root)
	return ret

def convert_to_ue4(root):
	all_obj = get_all_objects(root)
	for obj in all_obj:
		convert(root,obj)

def list_struct(filename):
	f = open(filename)
	root = read_object(None,f)
	show_object(root,0)

def convert_file(filename):
	f = open(filename)
	struct_map={}
	module_param_map={}

	root = read_object(None,f)

	convert_to_ue4(root)
	show_object(root,0)

def main():
	if len(sys.argv) < 2:
		print " need file name"
		exit()

	convert_file(sys.argv[1])



def show_object(obj, depth):
	str = "\t" * depth;
	if obj.name:
		str += "name: " + obj.name 
	if obj.cls:
		str  += "<"+obj.cls+">"
	print str
	#for line in obj.data:
	#	print "\t" * depth + line
	for child in obj.children:
		show_object(child, depth+1)
#		if obj.cls == None:
#			print "\t" * intent + "obj_ref: name="+obj.name
#		else:
#			print "\t" * intent + "obj_def: name="+obj.name+" class="+obj.cls

main()


		

		

	