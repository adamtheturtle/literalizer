import json
var shared: JsonNode = %*([
    1,
    2
])
var my_data: JsonNode = %*([
    shared,
    42
])
