import json
let shared: JsonNode = %*([
    1,
    2
])
let my_data: JsonNode = %*([
    shared,
    42
])
