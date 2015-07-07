import pyparsing as pp


name = pp.Word(pp.alphas,pp.alphanums+"_")
EQ,OPENER,CLOSER=map(pp.Suppress,"=()")
#this is telling pyparsing the value is recursive
value = pp.Forward()
class node:
    def __init__(self):
        self.parsed = False
        self.tokens = []

def on_parse_action(line,loc,token):
    print "entry:", token
    n = node()
    n.parsed = True
    n.tokens = token
    return n



#the name=value pairs
entry = name+EQ+value
#the recursive structure
struct = pp.Group( entry+pp.ZeroOrMore( entry + pp.Suppress( "," ))  )
simple_value = pp.dblQuotedString.copy() | pp.Word( pp.printables,excludeChars="()")
value << (struct | simple_value)


nested_struct = pp.nestedExpr(content=simple_value,ignoreExpr=pp.dblQuotedString.copy())
nested_struct.setParseAction(on_parse_action)

target5 = "(a=((b=1,c=(3)),(b=1,c=4)))"
target = "A=(b=(1,2,3),what=(vector2=(3,4,5),vector2=(3,4,5))c=(d=(2,2,3)),x=\"9(fd,,,sa)\")"
target2 = "a=(1,2,3,(s=4))"
target3 ="C=(I=(x=1))"
target4="C=(P=(1,1))"

def parse_complex(token):
    pass

output = nested_struct.parseString(target5)

print output

