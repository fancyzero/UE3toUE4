import sys
import re
class obj:
	pass

def convert_param_to_map ( params ):
	pmap = {}
	for k,v in params:
		pmap[k]=v
	return pmap

if len(sys.argv) < 2:
	print " need file name"
	exit()

f = open(sys.argv[1])
lines = f.read()
lines = lines.split("\r\n")

objects = []

intent = 0
for line in lines:
	if line.strip().startswith("End Object"):
		intent = intent - 1
	if line.strip().startswith("Begin Object"):
		intent = intent + 1
		params = re.findall(r'(\w+)=\"*(\w+)\"*', line)

		params = convert_param_to_map(params)

		obj.name = params.get("Name")
		obj.cls = params.get("Class")
		
		if obj.cls == None:
			print "\t" * intent + "obj_ref: name="+obj.name
		else:
			print "\t" * intent + "obj_def: name="+obj.name+" class="+obj.cls
		

		

	