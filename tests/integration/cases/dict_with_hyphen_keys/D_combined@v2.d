import std.json;
void main() {
auto my_data = JSONValue([
    "my-key": JSONValue("value1"),
    "another-key": JSONValue("value2"),
    "normal_key": JSONValue("value3"),
]);
my_data = JSONValue([
    "my-key": JSONValue("value1"),
    "another-key": JSONValue("value2"),
    "normal_key": JSONValue("value3"),
]);
}
