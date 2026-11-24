import json
template consume(args: varargs[untyped]) = discard
var my_null = %* nil
var regular_null = %* nil
consume(my_null)
consume(regular_null)
