import pyparsing as pp


name = pp.Word(pp.alphas,pp.alphanums+"_")
COMMA,EQ,OPENER,CLOSER=map(pp.Suppress,",=()")

value = pp.Forward()
entry = name+EQ+value
simple_value = (pp.dblQuotedString.copy() | pp.Word( pp.printables,excludeChars=",()") )
nested_struct =  OPENER + pp.Group(pp.OneOrMore(entry)) + pp.ZeroOrMore(COMMA + pp.Group(entry)) + CLOSER
simple_array = OPENER + pp.Group(pp.OneOrMore(value)) + pp.ZeroOrMore(COMMA + pp.Group(value)) + CLOSER
value << (nested_struct | simple_array |simple_value )

pp.Dict
#for debug start
class node:
    def __init__(self):
        self.parsed = False
        self.tokens = []

def on_parse_nested_struct(line,loc,token):
    print "nested struct:", token

def on_parse_array(line,loc,token):
    print "array:", token

def on_parse_action(line,loc,token):
    print "entry:", token
    n = node()
    n.parsed = True
    n.tokens = token



entry.setName("entry")
simple_value.setName("simple_value")
nested_struct.setName("nested_struct")
simple_array.setName("simple_array")
value.setName("value")
#for debug end


target1 = "A=(b=(1,2,3),what=(vector2=(3,4,5),vector2=(3,4,5)),c=(d=(2,2,3)),x=\"9(fd,,,sa)\")"
target2 = "a=((s=1),(s=2),(s=3),(s=4))"
target3 = "C=(I=(x=1))"
target4 = "C=(P=(1,1))"
target5 = "a=((b=1,c=(3)),(b=1,c=4))"
target6 = "a=(b=((1,2,3)))"
target7="C=(P=((O=(X=1,Y=1,Z=1)),(I=1,O=(X=1,Y=1,Z=1))))"

def dump(r,d):
    for i in r:
        if i.__class__ == list:
            print "*"*d +"["
            dump(i, d+1)
            print "*"*d +"]"
        else:
            print "*"*d + i
nested_struct.setParseAction(on_parse_nested_struct)
simple_array.setParseAction(on_parse_array)
entry.setParseAction(on_parse_action)
output = entry.parseString(target6)
print output.asXML()

