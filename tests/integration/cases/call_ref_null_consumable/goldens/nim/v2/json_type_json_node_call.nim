import json
{.warning[UnusedImport]:off.}
template consume(args: varargs[untyped]) = discard
var my_null: JsonNode = %*(nil)
var regular_null: JsonNode = %*(nil)
consume(my_null)
consume(regular_null)
