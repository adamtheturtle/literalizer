import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(["s": JSONValue(1)]),
    JSONValue(["t": JSONValue(3)]),
]);
}
