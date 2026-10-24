import std.json;
void main() {
auto my_data = JSONValue([
    "a": JSONValue(0b1),
    "b": JSONValue(2.5),
    "c": JSONValue(0b11),
]);
}
