import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["missing": JSONValue(-1), "present": JSONValue(1)]),
    JSONValue(["missing": JSONValue(2), "present": JSONValue(3)]),
]);
}
