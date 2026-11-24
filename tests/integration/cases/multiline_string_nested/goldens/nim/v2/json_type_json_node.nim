import json
var my_data: JsonNode = %*({
    "outer": %*([%*(["nested first line\n  indented\n\nnested last line\n"])])
})
