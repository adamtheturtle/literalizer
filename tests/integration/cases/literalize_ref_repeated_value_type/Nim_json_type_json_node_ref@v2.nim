import json
var shared: JsonNode = %*(42)
var my_data: JsonNode = %*([
    shared,
    shared
])
