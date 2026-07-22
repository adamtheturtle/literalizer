import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["replacement": JSONValue(-1), "present": JSONValue(1)]),
    JSONValue(["replacement": JSONValue(2), "present": JSONValue(3)]),
]);
}
