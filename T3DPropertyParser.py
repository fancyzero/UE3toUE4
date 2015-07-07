import pyparsing as pp
import sys
name = pp.Word(pp.alphas,pp.alphanums+"()_")
COMMA,EQ,OPENER,CLOSER=map(pp.Suppress,",=()")

value = pp.Forward()
entry = name+EQ+value
simple_value = (pp.dblQuotedString.copy() | pp.Word( pp.printables,excludeChars=",()") )
nested_struct =  OPENER + pp.Group(entry + pp.ZeroOrMore(COMMA + entry)) + CLOSER
simple_array = OPENER + pp.Group(value + pp.ZeroOrMore(COMMA + value)) + CLOSER
value << pp.Optional(nested_struct | simple_array |simple_value , default="")

def on_parse_action(line,loc,token):
    #print "onparse:",line, loc
    assert (len(token) == 2)
    assert token[0].__class__ == str
    k = token[0]
    if token[1].__class__ == pp.ParseResults:
        v = token[1].asList()
    else:
        v = token[1]
    return {k:v}

entry.setParseAction(on_parse_action)


def get_value(r, name):
    if r.__class__ == str:
        return None
    for k,v in r.iteritems():
        if k == name:
            return v
        if v.__class__ == list:
            for i in v:
                ret = get_value(i,name)
                if ret != None:
                    return ret

output_device = sys.stdout

def dump(r):
    ret = ""
    if r.__class__ == list:
        ret += "("
        if len(r) ==1:
            ret += dump(r[0])
        else:
            for i in r[:-1]:
                ret += dump(i) +","
            ret += dump(r[-1])
        ret += ")"
    elif r.__class__ == str:
        ret = r
    else:
        for k,v in r.iteritems():
            ret += k +"="+  dump(v)
    return ret

def parse_properties(line):
    return entry.parseString(line)

#debug begin
entry.setName("entry")
simple_value.setName("simple_value")
nested_struct.setName("nested_struct")
simple_array.setName("simple_array")
value.setName("value")
#debug end



#test case
if __name__ == "__main__":
    print "test:"
    testcases=\
    [
        "A=(b=(1,2,3),what=(vector2=(3,4,5),vector2=(3,4,5)),c=(d=(2,2,3)),x=\"9(fd,,,sa)\")",
        "a=((s=1),(s=2),(s=3),(s=4))",
        "C=(I=(x=(1,2,3)))",
        "C=(P=(1,1))",
        "a=((b=1,c=(3)),(b=1,c=4))",
        "P=(,(a=1))",
        "P=((a=1))",
        "RequiredModule=ParticleModuleRequired'ParticleModuleRequired_3'"
    ]

    for case in testcases:
        print "parsing: "
        print case
        output = entry.parseString(case)
        print output
        print dump(output[0])

