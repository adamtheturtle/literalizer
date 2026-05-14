import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["key": JSONValue("hello   world"), "value": JSONValue(1)]),
]);
}
