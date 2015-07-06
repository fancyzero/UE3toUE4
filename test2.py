import pyparsing as pp


#define the elements of pattern

#unreal naming convention
name = pp.Word(pp.alphas,pp.alphanums+"_")

EQ,OPENER,CLOSER=map(pp.Suppress,"=()")
#this is telling pyparsing the value is recursive
value = pp.Forward()

#the name=value pair
my_commasepitem = pp.Combine(pp.OneOrMore(pp.Word(pp.printables, excludeChars='(),') +
                                  pp.Optional( pp.Word(" \t") +
                                            ~pp.Literal(",") + ~pp.LineEnd() ) ) ).streamline().setName("MycommaItem")
MycommaSeparatedList = pp.delimitedList( pp.Optional( pp.quotedString.copy() | my_commasepitem, default=""),combine=False ).setName("MycommaSeparatedList")



entry = pp.Group(name+EQ+value)+pp.ZeroOrMore( pp.Suppress( "," ))
struct = pp.Dict(OPENER + pp.ZeroOrMore(entry)  + CLOSER)

array = OPENER + MycommaSeparatedList + CLOSER

simple_value = pp.quotedString.copy() | pp.Word( pp.printables,excludeChars="()")

value << ( struct |array |simple_value )


target = "A=(b=(1,2,3),c=(d=(2,2,3)),x=\"9(fd,,,sa)\")"


target2 = "(1,2,3,4)"
output = pp.OneOrMore(entry).parseString(target)
#output = (struct_array).parseString(target)
p = output.asList()

def dump(r,d):
    for i in r:
        if i.__class__ == list:
            dump(i, d+1)
        else:
            print " "*d + i


dump(p,0)






