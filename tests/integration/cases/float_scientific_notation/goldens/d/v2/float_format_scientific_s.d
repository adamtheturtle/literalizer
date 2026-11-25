import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(0.0),
    JSONValue(1.0),
    JSONValue(1.5e3),
    JSONValue(1.0e-3),
    JSONValue(1.0e16),
]);
}
