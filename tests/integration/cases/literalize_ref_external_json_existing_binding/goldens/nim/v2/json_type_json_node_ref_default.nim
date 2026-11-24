import json
{.warning[UnusedImport]:off.}
template consume_widget(args: varargs[untyped]) = discard
var my_data: JsonNode = %*({
    "a": 0
})
consume_widget(my_data)
my_data = %*({
    "a": 1
})
consume_widget(my_data)
