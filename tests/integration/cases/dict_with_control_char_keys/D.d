import std.json;
void _check() {
auto my_data = JSONValue([
    "key\nwith\nnewlines": JSONValue("value1"),
    "key\twith\ttabs": JSONValue("value2"),
    "": JSONValue("value3"),
]);
}
