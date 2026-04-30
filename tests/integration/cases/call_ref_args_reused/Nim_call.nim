import json
template process(args: varargs[untyped]) = discard
var shared = %* 1
var other = %* 2
process(shared, 1)
process(other, 0)
process(shared, 8)
