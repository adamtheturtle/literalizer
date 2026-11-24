import json
{.warning[UnusedImport]:off.}
template consume_widget(args: varargs[untyped]) = discard
var shared: JsonNode = %*([
    1,
    2
])
var my_data = shared
consume_widget(my_data)
