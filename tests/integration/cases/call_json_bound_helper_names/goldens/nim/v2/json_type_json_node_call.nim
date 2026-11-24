import json
{.warning[UnusedImport]:off.}
template process(args: varargs[untyped]) = discard
var arena: JsonNode = %*({
    "a": 1
})
var ZVal: JsonNode = %*({
    "a": 1
})
var ZKV: JsonNode = %*({
    "a": 1
})
process(arena)
process(ZVal)
process(ZKV)
