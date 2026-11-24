import json
{.warning[UnusedImport]:off.}
template consume(args: varargs[untyped]) = discard
var item: JsonNode = %*("s")
consume(item)
