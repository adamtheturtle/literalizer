import json
var shared: JsonNode = %*([
    1,
    2
])
var my_data: JsonNode = %*({
    "field": shared
})
my_data = %*({
    "field": shared
})
