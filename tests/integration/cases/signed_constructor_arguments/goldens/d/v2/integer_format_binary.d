import std.json;
void main() {
auto my_data = JSONValue([
    JSONValue(-0b101010),
    JSONValue(0b0),
    JSONValue(0b101010),
    JSONValue(-1.25),
    JSONValue(0.0),
    JSONValue(1.25),
]);
}
