import json
template consume(args: varargs[untyped]) = discard
var shared = %* 42
consume(shared)
