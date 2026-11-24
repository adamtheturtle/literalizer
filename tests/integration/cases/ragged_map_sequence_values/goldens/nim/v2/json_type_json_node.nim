import json
var my_data: JsonNode = %*({
    "a": %*([%*({"item": %*([1])})]),
    "b": %*([%*({"item": %*([2, 3])})])
})
