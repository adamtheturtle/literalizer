import json
var my_data: JsonNode = %*({
    "test": %*([5, %*(["compile", "test"])]),
    "package": %*([7, %*(["link", "test"])])
})
