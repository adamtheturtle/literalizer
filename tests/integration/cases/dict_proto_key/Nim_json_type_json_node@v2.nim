import json
var my_data: JsonNode = %*({
    "__proto__": %*({"x": 1}),
    "n": %*({"__proto__": 3}),
    "y": 2
})
