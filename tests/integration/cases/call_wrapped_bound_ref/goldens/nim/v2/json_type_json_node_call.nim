import json
{.warning[UnusedImport]:off.}
template make_widget(args: varargs[untyped]) = discard
var value: JsonNode = %*(1)
make_widget(value)
