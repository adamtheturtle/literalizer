import std.json;
void main() {
auto my_data = JSONValue([
    "deep": JSONValue([JSONValue([JSONValue([JSONValue([JSONValue(1)])])])]),
]);
}
