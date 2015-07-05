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
