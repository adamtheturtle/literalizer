import json
template consume(args: varargs[untyped]) = discard
let shared = %* 42
consume(shared)
