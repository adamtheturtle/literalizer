import std.json;
void main() {
auto my_data = JSONValue([
    "key\nwith\nnewlines": JSONValue("value1"),
    "key\twith\ttabs": JSONValue("value2"),
    "": JSONValue("value3"),
]);
my_data = JSONValue([
    "key\nwith\nnewlines": JSONValue("value1"),
    "key\twith\ttabs": JSONValue("value2"),
    "": JSONValue("value3"),
]);
}
