import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue("__proto__"), JSONValue(["x": JSONValue(1)])]),
    JSONValue([JSONValue("ordinary"), JSONValue(2)]),
]);
}
