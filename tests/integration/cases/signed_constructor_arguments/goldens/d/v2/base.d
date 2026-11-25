import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(-42),
    JSONValue(0),
    JSONValue(42),
    JSONValue(-1.25),
    JSONValue(0.0),
    JSONValue(1.25),
]);
}
