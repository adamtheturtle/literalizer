import json
{.warning[UnusedImport]:off.}
template consume(args: varargs[untyped]) = discard
var shared: JsonNode = %*(42)
consume(%*([shared, shared]))
