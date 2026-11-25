import json
{.warning[UnusedImport]:off.}
template process(args: varargs[untyped]) = discard
var unknown_value: JsonNode = newJArray()
process(%*([unknown_value]))
