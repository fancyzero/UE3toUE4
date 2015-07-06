import pyparsing as pp

delimeter = pp.Keyword(",")

lparen = pp.Suppress("(")
rparen = pp.Suppress(")")

qs = pp.quotedString("\"")

nonBracePrintables = ''.join(c for c in pp.printables if c not in '()')
Word = ~(delimeter ) + pp.Word(nonBracePrintables)("Word")
Phrase = pp.Forward()
Phrase << Word ^ \
        pp.operatorPrecedence(Phrase, [
            (delimeter, 2, pp.opAssoc.LEFT)
        ])
Expression = (
    pp.operatorPrecedence(pp.OneOrMore(Word),
    [
        (delimeter, 2, pp.opAssoc.LEFT)
    ])
)
def test(text):
    output = Expression.parseString(text)
    print output.asXML()


test("a=(c,b,((c,d)))")
