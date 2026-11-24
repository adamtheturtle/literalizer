import json
{.warning[UnusedImport]:off.}
template consume(args: varargs[untyped]) = discard
var shared: JsonNode = %*(nil)
consume(%*({"left": shared, "nested": %*([shared])}))
