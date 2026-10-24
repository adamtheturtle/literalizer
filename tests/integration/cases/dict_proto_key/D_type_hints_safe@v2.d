import std.json;
void main() {
auto my_data = JSONValue([
    "__proto__": JSONValue(["x": JSONValue(1)]),
    "n": JSONValue(["__proto__": JSONValue(3)]),
    "y": JSONValue(2),
]);
}
