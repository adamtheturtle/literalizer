import std.json;
void main() {
auto my_data = JSONValue([
    "x": JSONValue("\x00"),
    "y": JSONValue("\x001"),
]);
}
