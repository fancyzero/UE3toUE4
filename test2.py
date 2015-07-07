import pyparsing as pp

#define the elements of pattern
#unreal naming convention
name = pp.Word(pp.alphas,pp.alphanums+"_")
EQ,OPENER,CLOSER=map(pp.Suppress,"=()")
#this is telling pyparsing the value is recursive
value = pp.Forward()


def on_parse_action_entry_in_array(line,loc,token):
    print "entry_in_array:", token
def on_parse_action_value_group(line,loc,token):
    print "value_group:", token
def on_parse_action_entry(line,loc,token):
    print "entry:", token
def on_parse_action_array(line,loc,token):
    print "array:",token
def on_parse_action_simple_value(line,loc,token):
    print "value:",token
def on_parse_action_struct(line,loc,token):
    print "struct:",token

#the name=value pairs
entry = name+EQ+value
#the recursive structure
struct = entry+pp.ZeroOrMore( entry + pp.Suppress( "," ))

nested = pp.nestedExpr(content=struct,ignoreExpr=pp.dblQuotedString.copy())
#unreal use comma delimited list for all key value pairs
#my_commasepitem = pp.Combine(pp.OneOrMore( name+EQ+value ).streamline())
#MycommaSeparatedList = pp.delimitedList( pp.Optional( pp.sglQuotedString.copy() | my_commasepitem, default=""))

#some are simple key=value the value can also be an entry(recursively)
simple_value = pp.sglQuotedString.copy() | pp.Word( pp.printables,excludeChars="(,)")

entry_in_array = ((OPENER+entry+CLOSER) | simple_value)
#some value are array (x,x,x,x)
array = OPENER + entry_in_array + pp.ZeroOrMore( entry_in_array + pp.Suppress( "," )) + CLOSER
#for debug
entry_in_array.setParseAction(on_parse_action_entry_in_array)
entry.setParseAction(on_parse_action_entry)
array.setParseAction(on_parse_action_array)
simple_value.setParseAction(on_parse_action_simple_value)
struct.setParseAction(on_parse_action_struct)

#insert all pattern into forward defined value
value << pp.Group(nested |array | simple_value ).setParseAction(on_parse_action_value_group)

target = "A=(b=(1,2,3),what=(vector2=(3,4,5),vector2=(3,4,5))c=(d=(2,2,3)),x=\"9(fd,,,sa)\")"
target2 = "a=(1,2,3,(s=4))"
target3 ="C=(I=(x=1))"
target4="C=(P=(1,1))"
#target4="C=(P=((O=(X=1,Y=1,Z=1)),(I=1,O=(X=1,Y=1,Z=1))))"
output = pp.OneOrMore(entry).parseString(target4)

output.items()

def dump(r,d):
    for i in r:
        if i.__class__ == list:
            print "*"*d +"["
            dump(i, d+1)
            print "*"*d +"]"
        else:
            print "*"*d + i

dump(output.asList(),0)






