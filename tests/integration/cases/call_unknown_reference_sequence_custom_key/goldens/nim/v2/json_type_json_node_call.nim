import json
{.warning[UnusedImport]:off.}
template process(args: varargs[untyped]) = discard
var untypedValue: JsonNode = newJArray()
process(%*([untypedValue, untypedValue]))
