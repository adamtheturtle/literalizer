import std.json;
void _check() {
auto my_data = JSONValue([
    "my-key": JSONValue("value1"),
    "another-key": JSONValue("value2"),
    "normal_key": JSONValue("value3"),
]);
}
