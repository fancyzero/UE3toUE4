import sys
import PyUObject
import T3DPropertyParser as t3dpp
import re
import pyparsing as pp

# represent structure and intent level when output
intent_str = "   "
intent = 0

def parse_properties(props):
    return t3dpp.parse_properties(props)

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
        if k == "ThumbnailTexture":
            del obj.properties[k]
        if k == "Material":
            obj.properties[k] = "Material'/Engine/EngineMaterials/DefaultParticle.DefaultParticle'"

def extract_params(line):
    params = re.findall(r'(\w+)=\"*(\w+)\"*', line)
    pmap = {}
    for k, v in params:
        pmap[k] = v
    return pmap

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
                pp=parse_properties(line)
                obj.properties.update(  pp[0])

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

def convert_file(filename, output):
    f = open(filename)
    root = read_object(None,f)
    all_obj = get_all_objects(root)
    for obj in all_obj:
        convert(root,obj)

    file_output = open(output,"w")
    root.output_as_t3d( file_output )
    file_output.close()



def main():

    cmd = " ".join(sys.argv)
    cmd_options = {}

    def onOption(line, loc, token):
        cmd_options[token[0]]=token[1]

    option = (pp.Literal("-").suppress() + pp.Word(pp.printables) +pp.Word(pp.printables))
    option.setParseAction(onOption)
    output_expr =  pp.ZeroOrMore(pp.Word(pp.printables,excludeChars="-").suppress() |  option)
    output_expr.parseString(cmd)

    if not cmd_options.has_key("o"):
        print "use -o <filename> to specify output"
        return

    filename = sys.argv[1]
    convert_file(filename,cmd_options["o"])



main()






