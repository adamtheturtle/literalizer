import json
var my_data: JsonNode = %*({
    "$key": "a\"b\tcé #{world} $ident",
    "trailing multi-byte": "café"
})
