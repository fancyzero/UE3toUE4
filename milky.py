import sys
import re
class Object:
	def __init__(self):
		self.cls = ""
		self.name = ""
		self.children = []
		self.data=[]

def convert_param_to_map ( params ):
	pmap = {}
	for k,v in params:
		pmap[k]=v
	return pmap

def read_object(obj,f):
	if obj != None:
		print "reading :", obj.name
	line = f.readline()
	child = None
	while(line!=""):
		if line.strip().startswith("Begin Object"):
			child = Object()
			params = re.findall(r'(\w+)=\"*(\w+)\"*', line)
			params = convert_param_to_map(params)
			child.name = params.get("Name")
			child.cls = params.get("Class")

			if obj != None:
				obj.children.append(child)
			read_object(child,f)

		elif line.strip().startswith("End Object"):
			return obj
		else:
			obj.data.append(line)
		line = f.readline()
	return child

def main():
	if len(sys.argv) < 2:
		print " need file name"
		exit()

	f = open(sys.argv[1])

	

	struct_map={}
	module_param_map={}

	root = read_object(None,f)
	print root
	show_object(root,0)

def show_object(obj, depth):
	if depth > 2:
		return
	print "\t" * depth + obj.name + " " + obj.cls		
	for line in obj.data:
		print "\t" * depth + line
	for child in obj.children:
		show_object(child, depth+1)
#		if obj.cls == None:
#			print "\t" * intent + "obj_ref: name="+obj.name
#		else:
#			print "\t" * intent + "obj_def: name="+obj.name+" class="+obj.cls

main()


		

		

	