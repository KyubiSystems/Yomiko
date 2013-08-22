from pyparsing import *

enclosed = Forward()
nestedParens = nestedExpr('(', ')', content=enclosed)
nestedBrackets = nestedExpr('[', ']', content=enclosed)
nestedCurlies = nestedExpr('{', '}', content=enclosed)
enclosed << (Word(alphas) | ',' | nestedParens | nestedBrackets | nestedCurlies)

data = "[Null (nyanpoun)] Unnamed [Strike Witches](English)(Trinity Translations).zip"

print enclosed.parseString(data).asList()
