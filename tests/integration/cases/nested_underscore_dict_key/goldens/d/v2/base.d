import std.json;
void main() {
auto my_data = JSONValue([
    "outer": JSONValue([JSONValue(["_": JSONValue(1)])]),
]);
}
