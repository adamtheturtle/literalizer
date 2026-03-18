import std.json;

void _check() {
auto my_data = JSONValue([
    "key\nwith\nnewlines": JSONValue("value1"),
    "key	with	tabs": JSONValue("value2"),
]);
my_data = JSONValue([
    "key\nwith\nnewlines": JSONValue("value1"),
    "key	with	tabs": JSONValue("value2"),
]);
}
