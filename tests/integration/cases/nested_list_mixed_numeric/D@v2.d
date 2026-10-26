import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue([JSONValue(1)]),
    JSONValue([JSONValue(2.5)]),
]);
}
