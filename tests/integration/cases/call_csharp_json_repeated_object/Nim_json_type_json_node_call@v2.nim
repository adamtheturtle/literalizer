import json
{.warning[UnusedImport]:off.}
template consume(args: varargs[untyped]) = discard
var shared: JsonNode = %*({
    "value": %*([1, 2])
})
consume(%*({"left": shared, "right": shared}))
