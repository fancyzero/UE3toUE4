import sys
import PyUObject
import re

# represent structure and intent level when output
intent_str = "   "
intent = 0

def add_intent():
    global intent
    intent += 1

def sub_intent():
    global intent
    intent += -1

def output(str):
    global intent_str
    global intent
    print intent_str * intent + str


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


def extract_params(line):
    params = re.findall(r'(\w+)=\"*(\w+)\"*', line)
    pmap = {}
    for k, v in params:
        pmap[k] = v
    return pmap

def parse_properties(line):
    pos = line.find("=")
    k = line[0:pos]
    v = line[pos+1:]
    starts_with_parenthsis = v.startswith("(")
    have_assign = v.find("=") >= 0
    if starts_with_parenthsis and have_assign:
        v=v[1:-1]
        subparray = re.findall("\w+=\(.*?\)|\w+=\".*?\"|\w+=.*?,|\w+=.*",v)
        v={}

        for subp in subparray:
            if subp.endswith(","):#clean out ending ","
                subp=subp[:-1]
            subk, subv = parse_properties( subp )
            v[subk]=subv
    return k,v


def read_object(obj,f):
    child = None
    while True:
        line = f.readline()
        line = line.strip()
        if line == "":
            return child
        if line.startswith("Begin Object"):
            child = PyUObject.PyUObject()
            params = extract_params(line)
            child.name = params.get("Name")
            child.cls = params.get("Class")
            read_object(child,f)
            child.attach_to(obj)
        elif line.startswith("End Object"):
            return obj
        else:
            if obj != None:
                k,v=parse_properties(line)
                obj.properties[k] = v
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






