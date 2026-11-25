import std.json;
void main() {
auto my_data = JSONValue([
    "filled": JSONValue([JSONValue(1), JSONValue("value")]),
    "empty": parseJSON("[]"),
]);
}
