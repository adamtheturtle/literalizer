import json
{.warning[UnusedImport]:off.}
template consume(args: varargs[untyped]) = discard
var shared: JsonNode = %*([
    1,
    2
])
consume(%*({"field": shared, "nested": %*([shared, newJObject()])}))
