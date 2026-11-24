import json
{.warning[UnusedImport]:off.}
template consume_widget(args: varargs[untyped]) = discard
var item: JsonNode = %*(nil)
var my_data: JsonNode = %*(nil)
consume_widget(my_data)
my_data = item
consume_widget(my_data)
