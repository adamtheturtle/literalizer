import std.json;
void main() {
auto existing = JSONValue(1);
auto my_data = JSONValue([
    JSONValue(0),
    JSONValue([JSONValue([existing])]),
]);
}
