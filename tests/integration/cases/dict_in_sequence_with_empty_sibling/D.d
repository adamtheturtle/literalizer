import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["a": JSONValue(1)]),
    parseJSON("[]"),
]);
}
