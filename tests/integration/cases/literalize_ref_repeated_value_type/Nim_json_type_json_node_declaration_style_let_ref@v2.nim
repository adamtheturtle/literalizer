import json
let shared: JsonNode = %*(42)
let my_data: JsonNode = %*([
    shared,
    shared
])
