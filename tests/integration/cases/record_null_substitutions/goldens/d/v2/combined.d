import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue("rows"), JSONValue([JSONValue(["replacement": JSONValue(null), "present": JSONValue(1)]), JSONValue(["replacement": JSONValue(2), "present": JSONValue(3)])])]),
]);
my_data = JSONValue([
    JSONValue([JSONValue("rows"), JSONValue([JSONValue(["replacement": JSONValue(null), "present": JSONValue(1)]), JSONValue(["replacement": JSONValue(2), "present": JSONValue(3)])])]),
]);
}
